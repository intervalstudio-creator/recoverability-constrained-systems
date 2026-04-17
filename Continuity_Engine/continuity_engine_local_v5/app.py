from __future__ import annotations

import json
import socket
from copy import deepcopy
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd
import streamlit as st

from continuity_engine.models import CaseInput
from continuity_engine.resolver import evaluate_case
from continuity_engine.exporter import save_json, save_pdf
from continuity_engine.topology import build_graph


def detect_connection() -> str:
    try:
        socket.create_connection(("1.1.1.1", 53), timeout=1.0).close()
        return "online"
    except OSError:
        return "offline"


st.set_page_config(page_title="Continuity Engine v4", layout="wide")
st.title("Continuity Engine v4")
st.caption("Offline-first Recoverability Compiler + IAF + certificate-aware fallback runtime")

base_dir = Path(__file__).parent
sample_path = base_dir / "sample_cases" / "healthcare_case.json"
default_text = sample_path.read_text(encoding="utf-8") if sample_path.exists() else "{}"

templates = {
    p.stem: p.read_text(encoding="utf-8")
    for p in (base_dir / "templates").glob("*.json")
}

auto_connection = detect_connection()

with st.sidebar:
    st.header("Input")
    uploaded = st.file_uploader("Upload case JSON", type=["json"])
    template_name = st.selectbox("Template", options=["sample_healthcare"] + sorted(templates.keys()))
    use_sample = st.checkbox("Load selected template", value=not uploaded)
    st.divider()
    st.subheader("Connection & fallback")
    connection_mode = st.selectbox("Connection state", options=["auto", "offline", "degraded", "online"], index=0)
    fallback_local = st.checkbox("Fallback local mode available", value=True)
    network_required_primary = st.checkbox("Primary path requires network", value=False)
    network_required_local = st.checkbox("Local use requires network", value=False)
    remote_sync_enabled = st.checkbox("Remote sync enabled", value=False)
    require_remote_cert = st.checkbox("Require remote/API certificate", value=False)
    remote_cert_status = st.selectbox("Remote certificate status", options=["valid", "missing", "expired", "revoked", "unreachable", "unknown"], index=0)
    require_local_cert = st.checkbox("Require local execution certificate", value=False)
    local_cert_status = st.selectbox("Local certificate status", options=["valid", "missing", "expired", "revoked", "unreachable", "unknown"], index=0)
    st.divider()
    st.subheader("Live simulation")
    sim_delay = st.slider("Add delay to all intervals (minutes)", 0, 180, 0, 5)
    sim_pressure = st.slider("Override pressure", 0.0, 1.0, 0.0, 0.05)
    sim_resonance = st.slider("Override resonance", 0.0, 1.0, 0.0, 0.05)
    truth_break = st.checkbox("Force truth failure")
    authority_break = st.checkbox("Force authority unreachable")

if uploaded:
    initial_text = uploaded.read().decode("utf-8")
elif use_sample:
    initial_text = default_text if template_name == "sample_healthcare" else templates.get(template_name, default_text)
else:
    initial_text = default_text

json_text = st.text_area("Case JSON", value=initial_text, height=360)

run = st.button("Run Continuity Engine", type="primary")
if run:
    try:
        raw = json.loads(json_text)
        sim_raw = deepcopy(raw)

        selected_connection = auto_connection if connection_mode == "auto" else connection_mode
        sim_raw.setdefault("connectivity", {})
        sim_raw["connectivity"]["mode"] = selected_connection
        sim_raw["connectivity"]["fallback_local_mode_available"] = fallback_local
        sim_raw["connectivity"]["network_required_for_primary_path"] = network_required_primary
        sim_raw["connectivity"]["network_required_for_local_use"] = network_required_local
        sim_raw["connectivity"]["remote_sync_enabled"] = remote_sync_enabled

        certs = []
        if require_remote_cert:
            certs.append(
                {
                    "name": "remote_access_cert",
                    "required_for": "remote_api",
                    "status": remote_cert_status,
                    "renewable_in_time": False,
                    "fallback_exists": fallback_local,
                    "continuity_critical": True,
                }
            )
        if require_local_cert:
            certs.append(
                {
                    "name": "local_execution_cert",
                    "required_for": "local_execution",
                    "status": local_cert_status,
                    "renewable_in_time": False,
                    "fallback_exists": False,
                    "continuity_critical": True,
                }
            )
        if certs:
            sim_raw["connectivity"]["certificate_dependencies"] = certs

        if sim_delay:
            for interval in sim_raw.get("intervals", []):
                interval["current_minutes"] = float(interval["current_minutes"]) + float(sim_delay)
        if sim_pressure > 0:
            sim_raw["pressure"] = sim_pressure
        if sim_resonance > 0:
            sim_raw["resonance"] = sim_resonance
        if truth_break:
            sim_raw.setdefault("signal_sources", []).append(
                {
                    "name": "forced_truth_break",
                    "source": "simulation",
                    "current_value": "unknown",
                    "verifiable": False,
                    "stale": True,
                    "conflicted": True,
                    "observed_minutes_ago": 999,
                    "max_age_minutes": 15,
                }
            )
        if authority_break:
            for entity in sim_raw.get("entities", []):
                if entity.get("type") in {"team", "institution", "interface"}:
                    entity["reachable"] = False
                    entity["availability"] = min(float(entity.get("availability", 1.0)), 0.4)

        case = CaseInput.model_validate(sim_raw)
        result = evaluate_case(case)
        graph = build_graph(case)

        c1, c2, c3, c4 = st.columns([1, 1, 1, 1])
        with c1:
            st.subheader("Admissibility")
            st.metric("Class", result.admissibility_class)
            st.metric("Timing margin (minutes)", f"{result.timing_margin_minutes:.2f}")
            st.metric("Recovery reachable", "Yes" if result.recovery_reachable else "No")
        with c2:
            st.subheader("Trajectory state")
            st.metric("Viable recovery paths", result.iaf.viable_recovery_path_count)
            st.metric("Blocked recovery paths", result.iaf.blocked_recovery_path_count)
            st.metric("Last admissible action", result.iaf.last_admissible_action)
        with c3:
            st.subheader("Connection state")
            st.metric("Mode", case.connectivity.mode)
            st.metric("Offline fallback", "Engaged" if result.iaf.offline_mode_engaged else "Not engaged")
            st.metric("Local execution", "Yes" if result.iaf.local_execution_admissible else "No")
        with c4:
            st.subheader("Certificate state")
            st.metric("Valid certificates", result.iaf.valid_certificates)
            st.metric("Broken certificates", result.iaf.broken_certificates)
            st.metric("Network execution", "Yes" if result.iaf.network_dependent_execution_admissible else "No")

        tabs = st.tabs(["Reasons", "Actions", "Proof", "Trajectories", "Graph", "Connectivity", "Raw IAF"])
        with tabs[0]:
            for reason in result.reasons:
                st.write(f"- {reason}")
        with tabs[1]:
            for action in result.required_actions:
                st.write(f"- {action}")
            if result.iaf.propagated_failures:
                st.markdown("**Propagation**")
                for line in result.iaf.propagated_failures:
                    st.write(f"- {line}")
        with tabs[2]:
            for line in result.iaf.proof_lines:
                st.write(f"- {line}")
            st.info(result.iaf.authority_reason)
        with tabs[3]:
            path_rows = []
            for path in result.iaf.path_evaluations:
                path_rows.append(
                    {
                        "Path": path.name,
                        "Valid": path.valid,
                        "Minutes": path.bounded_minutes,
                        "Margin": round(path.margin_minutes, 2),
                        "Degraded Mode": path.degraded_mode_valid,
                        "Last admissible action offset": round(path.last_admissible_action_minutes, 2),
                        "Point-of-no-return offset": round(path.point_of_no_return_minutes, 2),
                        "Blockers": " | ".join(path.blockers),
                    }
                )
            st.dataframe(pd.DataFrame(path_rows), use_container_width=True)
        with tabs[4]:
            fig, ax = plt.subplots(figsize=(10, 6))
            pos = nx.spring_layout(graph, seed=7)
            node_colors = []
            for _, data in graph.nodes(data=True):
                if not data.get("reachable", True) or data.get("availability", 1.0) < 0.4 or not data.get("verifiable", True):
                    node_colors.append("#ef4444")
                elif data.get("availability", 1.0) < 0.7:
                    node_colors.append("#f59e0b")
                else:
                    node_colors.append("#22c55e")
            edge_colors = []
            for _, _, data in graph.edges(data=True):
                is_red = data.get("criticality", 0.5) >= 0.8 and not data.get("fallback_exists", False)
                edge_colors.append("#ef4444" if is_red else "#64748b")
            nx.draw_networkx(
                graph,
                pos=pos,
                ax=ax,
                with_labels=True,
                node_color=node_colors,
                edge_color=edge_colors,
                node_size=1800,
                font_size=9,
                arrows=True,
            )
            ax.axis("off")
            st.pyplot(fig)
            plt.close(fig)
        with tabs[5]:
            st.write(f"- Connection reason: {result.iaf.connection_reason}")
            st.write(f"- Certificate reason: {result.iaf.certificate_reason}")
            st.write(f"- Auto-detected host state: {auto_connection}")
            st.json(case.connectivity.model_dump())
        with tabs[6]:
            st.json(result.iaf.model_dump())

        out_dir = base_dir / "outputs"
        out_dir.mkdir(exist_ok=True)
        json_file = save_json(result, str(out_dir / "latest_report.json"))
        pdf_file = save_pdf(result, str(out_dir / "latest_report.pdf"))

        st.success("Evaluation complete")
        with open(json_file, "rb") as f:
            st.download_button("Download JSON report", f, file_name="continuity_engine_v4_report.json")
        with open(pdf_file, "rb") as f:
            st.download_button("Download PDF report", f, file_name="continuity_engine_v4_report.pdf")

    except Exception as exc:
        st.error(f"Failed to evaluate case: {exc}")

st.markdown("### Expected JSON shape")
st.code(default_text, language="json")
