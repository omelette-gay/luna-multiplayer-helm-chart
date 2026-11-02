#!/usr/bin/env python3
"""Check that an Ingress in rendered chart output (on stdin) points at a Service that is also in the output.

Usage: helm template test ./charts/luna-multiplayer | python3 scripts/check-ingress-backend.py [--expect-no-ingress]
"""
import sys

import yaml

docs = [d for d in yaml.safe_load_all(sys.stdin) if d]
services = {d["metadata"]["name"] for d in docs if d["kind"] == "Service"}
ingresses = [d for d in docs if d["kind"] == "Ingress"]

if "--expect-no-ingress" in sys.argv:
    if ingresses:
        sys.exit("expected no Ingress to be rendered, but found one")
    sys.exit(0)

if not ingresses:
    sys.exit("expected an Ingress to be rendered, but found none")

failed = False
for ingress in ingresses:
    for rule in ingress["spec"].get("rules", []):
        for path in rule["http"]["paths"]:
            backend = path["backend"]["service"]["name"]
            if backend not in services:
                print(f"Ingress {ingress['metadata']['name']} points at Service {backend}, which isn't rendered (Services: {sorted(services)})")
                failed = True
sys.exit(1 if failed else 0)
