from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer


def generate_pdf(record, filename):
    doc = SimpleDocTemplate(filename)
    styles = getSampleStyleSheet()
    content = [Paragraph("RECOVS Institutional Report", styles["Title"]), Spacer(1, 12)]

    for key, value in record.items():
        content.append(Paragraph(f"<b>{key}</b>: {value}", styles["Normal"]))
        content.append(Spacer(1, 6))

    doc.build(content)
    return filename
