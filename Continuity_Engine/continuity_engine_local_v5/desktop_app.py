from __future__ import annotations

import json
import socket
import sys
from copy import deepcopy
from pathlib import Path

import matplotlib
matplotlib.use('QtAgg')
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QComboBox,
    QFileDialog,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QPlainTextEdit,
    QSplitter,
    QTabWidget,
    QVBoxLayout,
    QWidget,
)

from continuity_engine.models import CaseInput
from continuity_engine.resolver import evaluate_case
from continuity_engine.exporter import save_json, save_pdf
from continuity_engine.topology import build_graph


BASE_DIR = Path(__file__).parent
SAMPLE_PATH = BASE_DIR / "sample_cases" / "healthcare_case.json"
TEMPLATES_DIR = BASE_DIR / "templates"
OUTPUTS_DIR = BASE_DIR / "outputs"
OUTPUTS_DIR.mkdir(exist_ok=True)


def detect_connection() -> str:
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=1.0).close()
        return "online"
    except OSError:
        return "offline"


class GraphCanvas(FigureCanvas):
    def __init__(self) -> None:
        self.fig, self.ax = plt.subplots(figsize=(7, 5))
        super().__init__(self.fig)
        self.fig.tight_layout()

    def draw_case_graph(self, case: CaseInput) -> None:
        self.ax.clear()
        graph = build_graph(case)
        pos = nx.spring_layout(graph, seed=7)
        node_colors = []
        for _, data in graph.nodes(data=True):
            if (not data.get("reachable", True)) or (data.get("availability", 1.0) < 0.4) or (not data.get("verifiable", True)):
                node_colors.append("#ef4444")
            elif data.get("availability", 1.0) < 0.7:
                node_colors.append("#f59e0b")
            else:
                node_colors.append("#22c55e")
        edge_colors = []
        for _, _, data in graph.edges(data=True):
            edge_colors.append("#ef4444" if data.get("criticality", 0.5) >= 0.8 and not data.get("fallback_exists", False) else "#64748b")
        nx.draw_networkx(
            graph,
            pos=pos,
            ax=self.ax,
            with_labels=True,
            node_color=node_colors,
            edge_color=edge_colors,
            node_size=1800,
            font_size=8,
            arrows=True,
        )
        self.ax.set_axis_off()
        self.draw()


class ContinuityEngineDesktop(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("Continuity Engine v6 — Native Desktop")
        self.resize(1480, 920)
        self.current_case: CaseInput | None = None
        self.current_result = None
        self.template_map = {
            "sample_healthcare": SAMPLE_PATH,
            **{p.stem: p for p in sorted(TEMPLATES_DIR.glob("*.json"))},
        }
        self._build_ui()
        self.load_selected_template()

    def _build_ui(self) -> None:
        root = QWidget()
        self.setCentralWidget(root)
        main_layout = QVBoxLayout(root)

        header = QLabel("Continuity Engine v6 — Native UI + Portable + Installer Pack")
        header.setStyleSheet("font-size: 22px; font-weight: 700;")
        main_layout.addWidget(header)
        sub = QLabel("Offline-first Recoverability Compiler + IAF + certificate-aware fallback runtime")
        sub.setStyleSheet("color: #475569;")
        main_layout.addWidget(sub)

        splitter = QSplitter(Qt.Horizontal)
        main_layout.addWidget(splitter, 1)

        left = QWidget()
        left_layout = QVBoxLayout(left)
        splitter.addWidget(left)

        # Controls
        controls_group = QGroupBox("Controls")
        controls_layout = QFormLayout(controls_group)
        self.template_combo = QComboBox()
        self.template_combo.addItems(self.template_map.keys())
        self.template_combo.currentIndexChanged.connect(self.load_selected_template)
        controls_layout.addRow("Template", self.template_combo)

        btn_row = QHBoxLayout()
        self.open_btn = QPushButton("Open JSON")
        self.open_btn.clicked.connect(self.open_json)
        self.save_case_btn = QPushButton("Save JSON")
        self.save_case_btn.clicked.connect(self.save_case_json)
        self.run_btn = QPushButton("Run Continuity Engine")
        self.run_btn.clicked.connect(self.run_engine)
        btn_row.addWidget(self.open_btn)
        btn_row.addWidget(self.save_case_btn)
        btn_row.addWidget(self.run_btn)
        controls_layout.addRow(btn_row)
        left_layout.addWidget(controls_group)

        options_group = QGroupBox("Connection, certificates, and fallback")
        options_layout = QGridLayout(options_group)
        self.connection_combo = QComboBox()
        self.connection_combo.addItems(["auto", "offline", "degraded", "online"])
        self.fallback_local = QCheckBox("Fallback local mode available")
        self.fallback_local.setChecked(True)
        self.network_required_primary = QCheckBox("Primary path requires network")
        self.network_required_local = QCheckBox("Local use requires network")
        self.remote_sync_enabled = QCheckBox("Remote sync enabled")
        self.require_remote_cert = QCheckBox("Require remote/API certificate")
        self.remote_cert_status = QComboBox()
        self.remote_cert_status.addItems(["valid", "missing", "expired", "revoked", "unreachable", "unknown"])
        self.require_local_cert = QCheckBox("Require local execution certificate")
        self.local_cert_status = QComboBox()
        self.local_cert_status.addItems(["valid", "missing", "expired", "revoked", "unreachable", "unknown"])
        self.truth_break = QCheckBox("Force truth failure")
        self.authority_break = QCheckBox("Force authority unreachable")

        rows = [
            (QLabel("Connection state"), self.connection_combo),
            (self.fallback_local, QLabel("")),
            (self.network_required_primary, QLabel("")),
            (self.network_required_local, QLabel("")),
            (self.remote_sync_enabled, QLabel("")),
            (self.require_remote_cert, self.remote_cert_status),
            (self.require_local_cert, self.local_cert_status),
            (self.truth_break, QLabel("")),
            (self.authority_break, QLabel("")),
        ]
        for i, (a, b) in enumerate(rows):
            options_layout.addWidget(a, i, 0)
            options_layout.addWidget(b, i, 1)
        left_layout.addWidget(options_group)

        self.case_editor = QPlainTextEdit()
        self.case_editor.setPlaceholderText("Case JSON")
        left_layout.addWidget(self.case_editor, 1)

        right = QWidget()
        right_layout = QVBoxLayout(right)
        splitter.addWidget(right)

        self.status_label = QLabel("Status: not run")
        self.status_label.setStyleSheet("font-size: 18px; font-weight: 700;")
        right_layout.addWidget(self.status_label)

        self.metrics_grid = QGridLayout()
        self.metric_labels = {}
        metric_names = [
            "Class",
            "Timing margin (minutes)",
            "Recovery reachable",
            "Viable recovery paths",
            "Blocked recovery paths",
            "Last admissible action",
            "Connection mode",
            "Offline fallback",
            "Local execution",
            "Valid certificates",
            "Broken certificates",
            "Network execution",
        ]
        for idx, name in enumerate(metric_names):
            title = QLabel(name)
            title.setStyleSheet("font-weight: 600;")
            value = QLabel("-")
            value.setWordWrap(True)
            self.metric_labels[name] = value
            r, c = divmod(idx, 4)
            box = QGroupBox()
            box_layout = QVBoxLayout(box)
            box_layout.addWidget(title)
            box_layout.addWidget(value)
            self.metrics_grid.addWidget(box, r, c)
        right_layout.addLayout(self.metrics_grid)

        self.tabs = QTabWidget()
        self.reasons_list = QListWidget()
        self.actions_list = QListWidget()
        self.proof_list = QListWidget()
        self.trajectories_list = QListWidget()
        self.connectivity_list = QListWidget()
        self.raw_output = QPlainTextEdit()
        self.raw_output.setReadOnly(True)
        self.graph_canvas = GraphCanvas()

        self.tabs.addTab(self.reasons_list, "Reasons")
        self.tabs.addTab(self.actions_list, "Actions")
        self.tabs.addTab(self.proof_list, "Proof")
        self.tabs.addTab(self.trajectories_list, "Trajectories")
        self.tabs.addTab(self.graph_canvas, "Graph")
        self.tabs.addTab(self.connectivity_list, "Connectivity")
        self.tabs.addTab(self.raw_output, "Raw IAF")
        right_layout.addWidget(self.tabs, 1)

        exports = QHBoxLayout()
        self.export_json_btn = QPushButton("Export Result JSON")
        self.export_json_btn.clicked.connect(self.export_json)
        self.export_pdf_btn = QPushButton("Export Result PDF")
        self.export_pdf_btn.clicked.connect(self.export_pdf)
        exports.addWidget(self.export_json_btn)
        exports.addWidget(self.export_pdf_btn)
        right_layout.addLayout(exports)

        splitter.setSizes([600, 880])

    def load_selected_template(self) -> None:
        path = self.template_map.get(self.template_combo.currentText())
        if path and path.exists():
            self.case_editor.setPlainText(path.read_text(encoding="utf-8"))

    def open_json(self) -> None:
        path, _ = QFileDialog.getOpenFileName(self, "Open case JSON", str(BASE_DIR), "JSON Files (*.json)")
        if path:
            self.case_editor.setPlainText(Path(path).read_text(encoding="utf-8"))

    def save_case_json(self) -> None:
        path, _ = QFileDialog.getSaveFileName(self, "Save case JSON", str(OUTPUTS_DIR / "case.json"), "JSON Files (*.json)")
        if path:
            Path(path).write_text(self.case_editor.toPlainText(), encoding="utf-8")

    def _patched_case_payload(self) -> dict:
        raw = json.loads(self.case_editor.toPlainText())
        sim_raw = deepcopy(raw)
        selected_connection = detect_connection() if self.connection_combo.currentText() == "auto" else self.connection_combo.currentText()
        sim_raw.setdefault("connectivity", {})
        sim_raw["connectivity"]["mode"] = selected_connection
        sim_raw["connectivity"]["fallback_local_mode_available"] = self.fallback_local.isChecked()
        sim_raw["connectivity"]["network_required_for_primary_path"] = self.network_required_primary.isChecked()
        sim_raw["connectivity"]["network_required_for_local_use"] = self.network_required_local.isChecked()
        sim_raw["connectivity"]["remote_sync_enabled"] = self.remote_sync_enabled.isChecked()

        certs = []
        if self.require_remote_cert.isChecked():
            certs.append(
                {
                    "name": "remote_access_cert",
                    "required_for": "remote_api",
                    "status": self.remote_cert_status.currentText(),
                    "renewable_in_time": False,
                    "fallback_exists": self.fallback_local.isChecked(),
                    "continuity_critical": True,
                }
            )
        if self.require_local_cert.isChecked():
            certs.append(
                {
                    "name": "local_execution_cert",
                    "required_for": "local_execution",
                    "status": self.local_cert_status.currentText(),
                    "renewable_in_time": False,
                    "fallback_exists": False,
                    "continuity_critical": True,
                }
            )
        if certs:
            sim_raw["connectivity"]["certificate_dependencies"] = certs
        elif "certificate_dependencies" in sim_raw["connectivity"]:
            sim_raw["connectivity"]["certificate_dependencies"] = []

        if self.truth_break.isChecked():
            sim_raw.setdefault("signal_sources", []).append(
                {
                    "name": "forced_truth_break",
                    "source": "desktop_simulation",
                    "current_value": "unknown",
                    "verifiable": False,
                    "stale": True,
                    "conflicted": True,
                    "observed_minutes_ago": 999,
                    "max_age_minutes": 15,
                }
            )
        if self.authority_break.isChecked():
            for entity in sim_raw.get("entities", []):
                if entity.get("type") in {"team", "institution", "interface"}:
                    entity["reachable"] = False
                    entity["availability"] = min(float(entity.get("availability", 1.0)), 0.4)
        return sim_raw

    def run_engine(self) -> None:
        try:
            payload = self._patched_case_payload()
            case = CaseInput.model_validate(payload)
            result = evaluate_case(case)
        except Exception as exc:  # noqa: BLE001
            QMessageBox.critical(self, "Run failed", str(exc))
            return

        self.current_case = case
        self.current_result = result
        self.status_label.setText(f"Status: {result.admissibility_class}")
        color = {
            "admissible": "#15803d",
            "degraded": "#ca8a04",
            "restricted": "#c2410c",
            "containment-required": "#b91c1c",
            "halt-required": "#7f1d1d",
            "restore-required": "#7c3aed",
            "non-executable": "#991b1b",
            "uncertifiable": "#334155",
        }.get(result.admissibility_class, "#334155")
        self.status_label.setStyleSheet(f"font-size: 18px; font-weight: 700; color: {color};")

        values = {
            "Class": result.admissibility_class,
            "Timing margin (minutes)": f"{result.timing_margin_minutes:.2f}",
            "Recovery reachable": "Yes" if result.recovery_reachable else "No",
            "Viable recovery paths": str(result.iaf.viable_recovery_path_count),
            "Blocked recovery paths": str(result.iaf.blocked_recovery_path_count),
            "Last admissible action": result.iaf.last_admissible_action,
            "Connection mode": case.connectivity.mode,
            "Offline fallback": "Engaged" if result.iaf.offline_mode_engaged else "Not engaged",
            "Local execution": "Yes" if result.iaf.local_execution_admissible else "No",
            "Valid certificates": str(result.iaf.valid_certificates),
            "Broken certificates": str(result.iaf.broken_certificates),
            "Network execution": "Yes" if result.iaf.network_dependent_execution_admissible else "No",
        }
        for key, value in values.items():
            self.metric_labels[key].setText(value)

        self.reasons_list.clear()
        self.actions_list.clear()
        self.proof_list.clear()
        self.trajectories_list.clear()
        self.connectivity_list.clear()

        self.reasons_list.addItems(result.reasons)
        self.actions_list.addItems(result.required_actions)
        self.proof_list.addItems(result.iaf.proof_lines)
        for path in result.iaf.path_evaluations:
            blockers = " | ".join(path.blockers) if path.blockers else "none"
            self.trajectories_list.addItem(
                f"{path.name} | valid={path.valid} | minutes={path.bounded_minutes} | margin={path.margin_minutes:.2f} | point_of_no_return={path.point_of_no_return_minutes:.2f} | blockers={blockers}"
            )
        self.connectivity_list.addItems(
            [
                result.iaf.connection_reason,
                result.iaf.certificate_reason,
                result.iaf.authority_reason,
                *result.iaf.propagated_failures,
            ]
        )
        self.raw_output.setPlainText(result.model_dump_json(indent=2))
        self.graph_canvas.draw_case_graph(case)

    def export_json(self) -> None:
        if not self.current_result:
            QMessageBox.information(self, "Nothing to export", "Run the engine first.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Export result JSON", str(OUTPUTS_DIR / "continuity_engine_result.json"), "JSON Files (*.json)")
        if path:
            save_json(self.current_result, path)
            QMessageBox.information(self, "Export complete", f"Saved to {path}")

    def export_pdf(self) -> None:
        if not self.current_result:
            QMessageBox.information(self, "Nothing to export", "Run the engine first.")
            return
        path, _ = QFileDialog.getSaveFileName(self, "Export result PDF", str(OUTPUTS_DIR / "continuity_engine_report.pdf"), "PDF Files (*.pdf)")
        if path:
            save_pdf(self.current_result, path)
            QMessageBox.information(self, "Export complete", f"Saved to {path}")


def main() -> int:
    app = QApplication(sys.argv)
    app.setApplicationName("Continuity Engine v5")
    window = ContinuityEngineDesktop()
    window.show()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
