from __future__ import annotations

from dataclasses import dataclass
from math import ceil
from typing import Dict, List, Optional


@dataclass(frozen=True)
class TopicCandidate:
    topic_id: int
    subject: str
    score: int  # 0..100


def compute_task_count(target_questions: int, chunk_size: int) -> int:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be > 0")
    return int(ceil(target_questions / chunk_size))


def allocate_subject_slots(
    subject_scores: Dict[str, int],
    task_count: int,
    *,
    min_per_subject: int = 1,
) -> List[str]:
    if task_count <= 0:
        return []

    subjects = list(subject_scores.keys())
    if not subjects:
        return []

    subjects_sorted = sorted(subjects, key=lambda s: subject_scores.get(s, 0), reverse=True)

    # slot azsa: en yüksek subjectlerden seç
    if task_count < len(subjects_sorted) * min_per_subject:
        return subjects_sorted[:task_count]

    slots: List[str] = []
    # minimum dağıtım
    for _ in range(min_per_subject):
        for s in subjects_sorted:
            if len(slots) < task_count:
                slots.append(s)

    # kalanları round-robin
    i = 0
    while len(slots) < task_count:
        slots.append(subjects_sorted[i % len(subjects_sorted)])
        i += 1

    return slots[:task_count]


def pick_topic_for_subject(
    subject: str,
    candidates_by_subject: Dict[str, List[TopicCandidate]],
    *,
    last_topic_id: Optional[int],
    used_topic_counts: Dict[int, int],
    max_per_topic: int = 2,
) -> Optional[TopicCandidate]:
    cand_list = candidates_by_subject.get(subject) or []
    for cand in cand_list:
        if last_topic_id is not None and cand.topic_id == last_topic_id:
            continue
        if used_topic_counts.get(cand.topic_id, 0) >= max_per_topic:
            continue
        return cand
    return None


def build_topic_plan(
    *,
    slots: List[str],
    candidates_by_subject: Dict[str, List[TopicCandidate]],
    max_per_topic: int = 2,
) -> List[int]:
    plan: List[int] = []
    used_counts: Dict[int, int] = {}
    last_topic_id: Optional[int] = None

    all_candidates: List[TopicCandidate] = []
    for lst in candidates_by_subject.values():
        all_candidates.extend(lst)
    all_candidates.sort(key=lambda c: c.score, reverse=True)

    for subject in slots:
        cand = pick_topic_for_subject(
            subject,
            candidates_by_subject,
            last_topic_id=last_topic_id,
            used_topic_counts=used_counts,
            max_per_topic=max_per_topic,
        )

        if cand is None:
            # fallback: global en iyi uygun topic
            for fc in all_candidates:
                if last_topic_id is not None and fc.topic_id == last_topic_id:
                    continue
                if used_counts.get(fc.topic_id, 0) >= max_per_topic:
                    continue
                cand = fc
                break

        if cand is None:
            break

        plan.append(cand.topic_id)
        used_counts[cand.topic_id] = used_counts.get(cand.topic_id, 0) + 1
        last_topic_id = cand.topic_id

    return plan
