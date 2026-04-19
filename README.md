# Recoverability-Constrained Systems  
## Execution Layer and Live Admissibility Engine

---

## Entry Points

- **Live Execution (Demo)**  
  https://intervalstudio-creator.github.io/recoverability-constrained-systems/

- **Authoritative Master Index (DOI)**  
  https://doi.org/10.5281/zenodo.19583410  

- **Documented Real Case (NHS Transport Failure)**  
  https://zenodo.org/records/19600917  

- **Website**  
  https://intervalstudio.org  

---

## System Definition

A system may act only while recoverability can be established, in time and under real conditions, as sufficient to prevent irreversible transition.

If this cannot be established:

- continuation is non-admissible  
- execution does not occur  

This condition applies to all domains, all actors, and all paths of continuation, including known, unknown, missing, latent, emergent, adversarial, and future conditions.

---

## System Layers

The system operates as a unified, non-fragmentable architecture:

1. **Invariant Layer**  
   Defines admissibility condition (recoverability constraint)  

2. **Structural Layer**  
   Master Index and formal system definition  

3. **Execution Layer**  
   Runtime systems enforcing admissibility  

4. **Interface Layer**  
   Live demo, tools, and interaction surfaces  

5. **Domain Layer**  
   Real-world implementations (healthcare, infrastructure, legal, identity, etc.)  

6. **Preservation Layer**  
   Redundant copies ensuring continuity and non-loss  

No layer may contradict or override the invariant.

---

## Live Recoverability Boundary Engine

This repository includes a deployed execution surface:

https://intervalstudio-creator.github.io/recoverability-constrained-systems/

### Capabilities

- multi-case evaluation (NHS, offshore, legal, identity)  
- timeline simulation against recoverability window  
- visual boundary condition diagram  
- decision output: **CONTINUE / STOP / NON-EXECUTABLE**  
- reason codes and decision trace  
- audit output for real-world evaluation  

---

## Documented Real-World Case

NHS transport-related continuity failure:

https://zenodo.org/records/19600917

This case demonstrates non-admissible continuation after loss of recoverability under real conditions.

---

## Repository Role

This repository serves as an **execution and deployment surface** for Recoverability-Constrained Systems.

It provides:

- runtime evaluation tools  
- deployable system components  
- real-world case testing environments  
- integration reference for operational deployment  

It is not a standalone definition of the system.

All components are valid only insofar as they preserve identical admissibility outcomes under the invariant defined in the Master Index.

---

## Core Principle

No distinction is permitted between representation and execution.

Any condition that cannot be:

- detected  
- verified  
- interpreted  
- enforced  
- and executed  

in time under real conditions is treated as absent.

---

## Usage

The live engine can be used to:

1. evaluate real-world failure scenarios  
2. demonstrate loss of admissibility under delay or constraint  
3. identify the exact point where recoverability collapses  
4. determine required system response (restriction, escalation, halt)  

---

## Deployment

The system is deployed via GitHub Pages.

To deploy or replicate:

1. ensure `index.html` is in the repository root  
2. go to **Settings → Pages**  
3. select **Deploy from branch**  
4. choose `main` branch and `/ (root)`  
5. save  

---

## System Architecture (Top-Level)

The repository is organized as a single system:

- **Core Definition**  
  `Master_Documents/` — authoritative system definition  

- **Execution Layer**  
  `index.html` — live admissibility engine  

- **Runtime Systems**  
  `Continuity_Engine/` — execution components  

- **Domain Implementations**  
  `RCCS/` — applied systems and cases  

- **Preservation Layer**  
  `Preserved_Source_Bundles/` — continuity-preserving archives  

- **Operational Interfaces**  
  `INSTALL_AND_RUN.md`, `DEPLOYMENT_CHECKLIST.md`  

---

## Authority and Scope

The authoritative definition of the system is the Master Index:

https://doi.org/10.5281/zenodo.19583410  

This repository does not override or redefine the system.

All implementations, demonstrations, and derived artifacts must preserve identical admissibility outcomes under the invariant.

---

## Continuity Condition

If any required condition, path, dependency, or recovery mechanism cannot be established in time under real conditions:

→ admissibility cannot be established  
→ continuation is non-admissible  
→ execution does not occur  

No further condition applies.
