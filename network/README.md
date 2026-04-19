# Network Layer

This directory contains the live distributed network layer of the Recoverability-Constrained Systems framework.

It enables real-time coordination between multiple nodes operating under the same admissibility condition.

---

## Purpose

To extend the system from isolated execution into a distributed environment where:

- nodes discover each other  
- state propagates across the network  
- decisions are synchronized  
- continuation is evaluated collectively  

---

## Core Components

### Bootstrap Service
Handles:

- node registration  
- peer discovery  
- network entry point  

### Continuity Nodes
Each node:

- runs a local execution environment  
- exchanges messages with peers  
- synchronizes state  
- enforces admissibility locally  

---

## Execution Principle

A system may act only while recoverability can be established in time under real conditions.

If this cannot be established:

→ continuation is non-admissible  
→ execution does not occur  

This condition applies at both:

- node level  
- network level  

---

## Network Behavior

- Local-first operation (works without connectivity)  
- Synchronization extends continuity, it does not define it  
- No central authority controls continuation  
- Each node enforces the same boundary condition  

---

## Current Version

v6 — Live Network Core

This is the first implementation of:

- multi-node coordination  
- real-time propagation  
- distributed enforcement  

---

## Usage

See:

- `Bootstrap_Service_v6/`
- `Continuity_Node_v6/`

for execution and deployment instructions.
