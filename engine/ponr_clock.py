"""
Boundary — Point-of-No-Return Clock

For every case, computes:
  - Time remaining before the next irreversible transition
  - Timing margin across each recovery condition
  - Whether the point of no return has already been crossed
  - A live countdown that degrades through warning thresholds

This is the timing gap: escalation happens after it is already too late.
This module makes time visible before it runs out.
"""

import uuid
from datetime import datetime, timezone
from typing import Optional
from dataclasses import dataclass, field


# ─────────────────────────────────────────────
# Timing Thresholds
# ─────────────────────────────────────────────

THRESHOLDS = {
    "critical":  3_600,    # < 1 hour  → NON-EXECUTABLE territory
    "warning":   14_400,   # < 4 hours → urgent action required
    "degraded":  86_400,   # < 24 hours → margin reduced
    "monitor":   604_800,  # < 7 days  → monitor closely
}

THRESHOLD_LABELS = {
    "critical": "CRITICAL — Escalate immediately",
    "warning":  "WARNING — Urgent action required",
    "degraded": "DEGRADED — Reduced margin",
    "monitor":  "MONITOR — Within 7-day window",
    "safe":     "ADEQUATE — Sufficient margin",
}


# ─────────────────────────────────────────────
# Point-of-No-Return Clock
# ─────────────────────────────────────────────

@dataclass
class PNRClock:
    """
    Tracks the time-to-irreversibility for a single case.
    Updates continuously as state changes.
    """
    case_id:                    str
    label:                      str
    domain:                     str
    seconds_to_irreversibility: Optional[float] = None
    detection_window_seconds:   Optional[float] = None
    response_window_seconds:    Optional[float] = None
    recovery_window_seconds:    Optional[float] = None
    created_at:                 str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    last_updated:               str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    crossed:                    bool = False
    history:                    list = field(default_factory=list)

    def update(self, seconds_remaining: Optional[float]):
        self.last_updated = datetime.now(timezone.utc).isoformat()
        prev = self.seconds_to_irreversibility
        self.seconds_to_irreversibility = seconds_remaining
        self.crossed = (seconds_remaining is not None and seconds_remaining <= 0)

        self.history.append({
            "timestamp":         self.last_updated,
            "seconds_remaining": seconds_remaining,
            "crossed":           self.crossed,
            "threshold":         self.get_threshold_label(),
        })

        # Return True if threshold boundary was crossed
        if prev is not None and seconds_remaining is not None:
            for name, secs in THRESHOLDS.items():
                if prev > secs >= seconds_remaining:
                    return name  # threshold just crossed
        return None

    def get_threshold_label(self) -> str:
        s = self.seconds_to_irreversibility
        if s is None:
            return "UNKNOWN"
        if s <= 0:
            return "CROSSED"
        if s < THRESHOLDS["critical"]:
            return "critical"
        if s < THRESHOLDS["warning"]:
            return "warning"
        if s < THRESHOLDS["degraded"]:
            return "degraded"
        if s < THRESHOLDS["monitor"]:
            return "monitor"
        return "safe"

    def to_display(self) -> dict:
        s = self.seconds_to_irreversibility
        label = self.get_threshold_label()

        if s is None:
            hours, minutes = None, None
            display = "UNKNOWN"
        elif s <= 0:
            hours, minutes = 0, 0
            display = "POINT OF NO RETURN CROSSED"
        else:
            hours   = int(s // 3600)
            minutes = int((s % 3600) // 60)
            if hours >= 168:
                display = f"{int(hours/24)}d {hours%24}h remaining"
            elif hours >= 24:
                display = f"{int(hours/24)}d {hours%24}h remaining"
            elif hours > 0:
                display = f"{hours}h {minutes}m remaining"
            else:
                display = f"{minutes}m remaining"

        return {
            "case_id":                    self.case_id,
            "label":                      self.label,
            "domain":                     self.domain,
            "seconds_to_irreversibility": s,
            "hours_remaining":            round(s / 3600, 2) if s is not None else None,
            "display":                    display,
            "threshold":                  label,
            "threshold_label":            THRESHOLD_LABELS.get(label, label),
            "crossed":                    self.crossed,
            "last_updated":               self.last_updated,
            "timing_margins": {
                "detection_window_seconds": self.detection_window_seconds,
                "response_window_seconds":  self.response_window_seconds,
                "recovery_window_seconds":  self.recovery_window_seconds,
                "margin_after_detection": (
                    (s or 0)
                    - (self.detection_window_seconds or 0)
                    - (self.response_window_seconds or 0)
                    - (self.recovery_window_seconds or 0)
                ),
            },
        }


# ─────────────────────────────────────────────
# Clock Registry
# ─────────────────────────────────────────────

class ClockRegistry:
    """Manages multiple PNR clocks across cases."""

    def __init__(self):
        self._clocks: dict[str, PNRClock] = {}

    def register(self, case_id: str, label: str, domain: str,
                 seconds: Optional[float] = None,
                 detection_window: Optional[float] = None,
                 response_window: Optional[float] = None,
                 recovery_window: Optional[float] = None) -> PNRClock:
        clock = PNRClock(
            case_id=case_id, label=label, domain=domain,
            seconds_to_irreversibility=seconds,
            detection_window_seconds=detection_window,
            response_window_seconds=response_window,
            recovery_window_seconds=recovery_window,
        )
        self._clocks[case_id] = clock
        return clock

    def update(self, case_id: str, seconds_remaining: float) -> Optional[str]:
        clock = self._clocks.get(case_id)
        if clock:
            return clock.update(seconds_remaining)
        return None

    def get(self, case_id: str) -> Optional[PNRClock]:
        return self._clocks.get(case_id)

    def get_all_display(self) -> list[dict]:
        return [c.to_display() for c in self._clocks.values()]

    def get_critical(self) -> list[dict]:
        return [
            c.to_display() for c in self._clocks.values()
            if c.get_threshold_label() in ("critical", "CROSSED")
        ]

    def get_crossed(self) -> list[dict]:
        return [c.to_display() for c in self._clocks.values() if c.crossed]

    def remove(self, case_id: str):
        self._clocks.pop(case_id, None)

    def summary(self) -> dict:
        all_clocks = list(self._clocks.values())
        by_threshold: dict[str, int] = {}
        for c in all_clocks:
            t = c.get_threshold_label()
            by_threshold[t] = by_threshold.get(t, 0) + 1
        return {
            "total_clocks":    len(all_clocks),
            "crossed":         len([c for c in all_clocks if c.crossed]),
            "critical":        by_threshold.get("critical", 0),
            "warning":         by_threshold.get("warning", 0),
            "degraded":        by_threshold.get("degraded", 0),
            "monitor":         by_threshold.get("monitor", 0),
            "safe":            by_threshold.get("safe", 0),
            "unknown":         by_threshold.get("UNKNOWN", 0),
            "by_threshold":    by_threshold,
        }


# Global registry instance
registry = ClockRegistry()


def compute_timing_from_evaluation(eval_result: dict) -> dict:
    """
    Extract and compute timing information from an evaluation result.
    Registers or updates the PNR clock for the case.
    """
    case_id  = eval_result.get("case_id", str(uuid.uuid4()))
    label    = eval_result.get("label", "")
    domain   = eval_result.get("domain", "")
    tti      = eval_result.get("time_to_irreversibility", {}) or {}
    seconds  = tti.get("seconds_remaining")

    clock = registry.get(case_id)
    if clock:
        threshold_crossed = clock.update(seconds)
    else:
        clock = registry.register(case_id, label, domain, seconds)
        threshold_crossed = None

    display = clock.to_display()
    display["threshold_just_crossed"] = threshold_crossed
    return display
