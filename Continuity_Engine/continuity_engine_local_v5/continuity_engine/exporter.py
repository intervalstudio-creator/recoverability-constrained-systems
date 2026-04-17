from __future__ import annotations

from pathlib import Path
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from .models import EvaluationResult


def save_json(result: EvaluationResult, output_path: str) -> str:
    path = Path(output_path)
    path.write_text(result.model_dump_json(indent=2), encoding="utf-8")
    return str(path)


def save_pdf(result: EvaluationResult, output_path: str) -> str:
    path = Path(output_path)
    c = canvas.Canvas(str(path), pagesize=A4)
    width, height = A4
    y = height - 50

    def line(text: str, step: int = 16):
        nonlocal y
        c.drawString(40, y, text[:110])
        y -= step
        if y < 60:
            c.showPage()
            y = height - 50

    line("Continuity Engine v5 Report", 22)
    line(f"Case: {result.case_title}")
    line(f"Domain: {result.domain}")
    line(f"Admissibility: {result.admissibility_class}")
    line(f"Recovery reachable: {result.recovery_reachable}")
    line(f"Timing margin (minutes): {result.timing_margin_minutes:.2f}")
    line(f"Last admissible action: {result.iaf.last_admissible_action}")
    line(f"Point-of-no-return offset (minutes): {result.iaf.point_of_no_return_minutes:.2f}")
    line("")
    line("Proof:")
    for proof in result.iaf.proof_lines:
        line(f"- {proof}")
    line("")
    line("Reasons:")
    for reason in result.reasons:
        line(f"- {reason}")
    line("")
    line("Required actions:")
    for action in result.required_actions:
        line(f"- {action}")
    c.save()
    return str(path)
