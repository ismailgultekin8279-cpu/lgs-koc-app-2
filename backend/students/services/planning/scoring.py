from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime, timezone
from math import exp
from typing import Any, Dict, Optional


def _clamp(x: float, lo: float = 0.0, hi: float = 1.0) -> float:
    return max(lo, min(hi, x))


def _days_since(last_practiced_at: Optional[datetime], plan_date: date) -> int:
    if not last_practiced_at:
        return 999
    if isinstance(last_practiced_at, datetime):
        dt = last_practiced_at
        if dt.tzinfo is not None:
            dt = dt.astimezone(timezone.utc).replace(tzinfo=None)
        return (plan_date - dt.date()).days
    return 999


@dataclass(frozen=True)
class TopicScore:
    score: int  # 0..100
    meta: Dict[str, Any]


def compute_topic_score(
    *,
    correct: int,
    wrong: int,
    blank: int,
    last_practiced_at: Optional[datetime],
    plan_date: date,
) -> TopicScore:
    """
    V1: açıklanabilir, deterministik skor.
    Öncelik: zayıflık + aralık (recency). Yeni konulara küçük bonus.
    """
    correct = int(correct or 0)
    wrong = int(wrong or 0)
    blank = int(blank or 0)

    total = correct + wrong + blank
    denom = max(1, total)

    accuracy = correct / denom
    wrong_rate = wrong / denom
    blank_rate = blank / denom

    days = _days_since(last_practiced_at, plan_date)

    weak = _clamp(0.7 * wrong_rate + 1.0 * blank_rate + 0.4 * (1.0 - accuracy))
    rec = _clamp(1.0 - exp(-days / 7.0))
    new_bonus = 0.4 if total == 0 else 0.0

    raw = _clamp(0.75 * weak + 0.20 * rec + 0.05 * new_bonus)
    score = int(round(100 * raw))

    meta = {
        "total": total,
        "accuracy": round(accuracy, 4),
        "wrong_rate": round(wrong_rate, 4),
        "blank_rate": round(blank_rate, 4),
        "days_since": days,
        "weak": round(weak, 4),
        "recency": round(rec, 4),
        "new_bonus": new_bonus,
        "raw": round(raw, 4),
    }
    return TopicScore(score=score, meta=meta)

