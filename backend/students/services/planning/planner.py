from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Dict, List

from django.db import transaction
from django.db.models import QuerySet

from curriculum.models import Topic
from students.models import StudyTask, TopicPerformance, Student

from .allocator import TopicCandidate, allocate_subject_slots, build_topic_plan, compute_task_count
from .scoring import compute_topic_score


@dataclass(frozen=True)
class PlanResult:
    created_count: int
    total_questions: int
    task_count: int


def _topk_avg(nums: List[int], k: int = 3) -> int:
    if not nums:
        return 0
    nums = sorted(nums, reverse=True)[:k]
    return int(round(sum(nums) / len(nums)))


def generate_daily_plan(
    *,
    student_id: int,
    plan_date: date,
    target_questions: int,
    chunk_size: int,
    force: bool = False,
    min_per_subject: int = 1,
    max_per_topic: int = 2,
    seconds_per_question: int = 60,
) -> PlanResult:
    """
    V1 Plan Motoru:
    - Öncelik: soru sayısı (target_questions)
    - Subject bazlı slot dağıtımı (min_per_subject)
    - Topic selection: score desc + cooldown + daily cap (max_per_topic)
    - Süre sadece recommended_seconds
    - order alanı ile görev sırası korunur
    """
    if target_questions <= 0:
        return PlanResult(created_count=0, total_questions=0, task_count=0)
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")

    student = Student.objects.get(id=student_id)

    # idempotency
    existing_qs = StudyTask.objects.filter(student=student, date=plan_date)
    if existing_qs.exists():
        if not force:
            return PlanResult(created_count=0, total_questions=0, task_count=0)
        existing_qs.delete()

    # TopicPerformance map
    perf_qs = TopicPerformance.objects.filter(student=student).select_related("topic")
    perf_by_topic_id: Dict[int, TopicPerformance] = {p.topic_id: p for p in perf_qs}

    # All topics from curriculum
    topics: QuerySet[Topic] = Topic.objects.all().order_by("subject", "order", "id")

    # Build candidates grouped by subject
    candidates_by_subject: Dict[str, List[TopicCandidate]] = {}
    topic_scores_by_subject: Dict[str, List[int]] = {}

    for t in topics:
        subject = str(t.subject)

        p = perf_by_topic_id.get(t.id)
        correct = p.correct if p else 0
        wrong = p.wrong if p else 0
        blank = p.blank if p else 0
        last_practiced_at = p.last_practiced_at if p else None

        ts = compute_topic_score(
            correct=correct,
            wrong=wrong,
            blank=blank,
            last_practiced_at=last_practiced_at,
            plan_date=plan_date,
        )

        cand = TopicCandidate(topic_id=t.id, subject=subject, score=ts.score)
        candidates_by_subject.setdefault(subject, []).append(cand)
        topic_scores_by_subject.setdefault(subject, []).append(ts.score)

    # Sort candidates within each subject by score desc, then by topic_id for determinism
    for subject, lst in candidates_by_subject.items():
        lst.sort(key=lambda c: (c.score, -c.topic_id), reverse=True)

    # Subject scores: top3 avg
    subject_scores: Dict[str, int] = {s: _topk_avg(scores, k=3) for s, scores in topic_scores_by_subject.items()}

    task_count = compute_task_count(target_questions, chunk_size)
    slots = allocate_subject_slots(subject_scores, task_count, min_per_subject=min_per_subject)
    topic_plan = build_topic_plan(slots=slots, candidates_by_subject=candidates_by_subject, max_per_topic=max_per_topic)

    # Allocate question counts across tasks
    remaining = target_questions
    tasks: List[StudyTask] = []
    order = 1

    for topic_id in topic_plan:
        if remaining <= 0:
            break

        q = chunk_size if remaining >= chunk_size else remaining
        remaining -= q

        tasks.append(
            StudyTask(
                student=student,
                date=plan_date,
                topic_id=topic_id,
                task_type="practice",
                question_count=q,
                recommended_seconds=int(q * seconds_per_question),
                status="todo",
                order=order,
            )
        )
        order += 1

    with transaction.atomic():
        StudyTask.objects.bulk_create(tasks)

    created_total_questions = sum(t.question_count for t in tasks)
    return PlanResult(created_count=len(tasks), total_questions=created_total_questions, task_count=task_count)
