# Live Attack Simulation Log

This document records a real, reproducible typosquatting attack simulation
performed against a local, isolated npm registry (Verdaccio). No external
systems were affected — everything ran on `localhost`.

## Setup

1. Started a local Verdaccio registry: `verdaccio` (http://localhost:4873)
2. Created a malicious package `expresss` (typosquat of the popular `express`
   package) with a `postinstall` script that writes a proof-of-concept file
   — see `malicious-package-poc/package.json` and `evidence.js`
3. Published it to the local registry: `npm publish --registry http://localhost:4873/`
4. Simulated a victim installing the package:
   `npm install expresss --registry http://localhost:4873/`

## Result: Silent code execution confirmed

Installing `expresss` triggered its `postinstall` script automatically,
without any user confirmation. Proof file generated at
`node_modules/expresss/PROOF_OF_CONCEPT.txt`:

[PoC] This file was created automatically by a 'postinstall' script.
Package: expresss
Timestamp: 2026-07-22T09:32:42.548Z
This demonstrates how a malicious package could execute code silently during 'npm install'.
No harm done — this is a controlled security research demo.

## Result: Detection confirmed

Supply Chain Sentinel's typosquat analyzer was run against the package name
`expresss` and correctly flagged it:

expresss: {'is_suspicious': True, 'reason': "I think this package is
suspicious because its name is very close to the popular package
'express' (edit distance: 1)."}

## How to reproduce

1. Install Verdaccio: `npm install -g verdaccio`
2. Start it: `verdaccio`
3. In a new terminal: `npm adduser --registry http://localhost:4873/`
4. Copy `malicious-package-poc/` to its own folder, `cd` into it,
   run `npm publish --registry http://localhost:4873/`
5. In another empty folder: `npm install expresss --registry http://localhost:4873/`
6. Check `node_modules/expresss/PROOF_OF_CONCEPT.txt`
7. Run `python main.py` from the project root and observe the typosquat
   analyzer flagging `expresss`