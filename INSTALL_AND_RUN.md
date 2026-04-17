# INSTALL AND RUN

This package is intended to reduce fragmentation and preserve a single execution path.

## 1. Read first
Open:

- `README_FINAL_START_HERE.md`
- `Master_Documents/Recoverability-Constrained_Systems_Master_Index.pdf`
- `Master_Documents/Recoverability-Constrained_Systems_Minimal_Execution_Pack.pdf`

## 2. RCCS
Open:

- `RCCS/README.md`
- `RCCS/execution_engine/README.md`

Run the RCCS execution engine from the `execution_engine` folder:

```bash
python runtime_loop.py
```

If import paths need adjustment in your environment, run from within the `execution_engine` directory.

## 3. Continuity Engine
Open the `Continuity_Engine/` folder and follow the installer/package instructions included there.

## 4. Operational rule
If recoverability cannot be established in time under real conditions:

- do not continue
- interrupt execution where already running
- escalate or contain as required

## 5. Before live use
Complete:

- adversarial testing
- domain-specific deployment checklist
- authority mapping
- maintenance/update checks
