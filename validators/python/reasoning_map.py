#!/usr/bin/env python3
"""Validate reasoning maps against the protocol in protocol/.

    python3 validators/python/reasoning_map.py MAP.json [MAP.json ...]

Exits 1 if any map has errors; warnings are printed and do not fail. Standard library only. Uses the
jsonschema package for the shape check when it is installed, and a small built-in subset otherwise.
The schemas and protocol/README.md are the spec; this file is one implementation of them.
"""
import json, sys
from pathlib import Path

PROTOCOL = Path(__file__).resolve().parents[2] / "protocol"
PROFILES = {p: json.loads((PROTOCOL / ("%s.schema.json" % p)).read_text()) for p in ("core", "reasoning", "grades")}
# the rendering hints listed in core.schema.json
KINDS = {"claim", "group", "part", "driver", "mechanism", "condition", "outcome", "failure", "demoted"}


def mini_validate(value, schema, where="map"):
    """The subset of JSON Schema the profiles use: type, required, properties, items, enum, minLength,
    minItems."""
    errs, t = [], schema.get("type")
    kinds = {"object": dict, "array": list, "string": str}
    if t and not isinstance(value, kinds[t]):
        return ["%s: should be %s" % (where, t)]
    if "enum" in schema and value not in schema["enum"]:
        errs.append("%s: %r is not one of %s" % (where, value, ", ".join(map(str, schema["enum"]))))
    if isinstance(value, str) and len(value) < schema.get("minLength", 0):
        errs.append("%s: empty" % where)
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            errs.append("%s: needs at least %d" % (where, schema["minItems"]))
        for k, item in enumerate(value):
            errs += mini_validate(item, schema.get("items", {}), "%s[%d]" % (where, k))
    if isinstance(value, dict):
        for r in schema.get("required", []):
            if r not in value:
                errs.append("%s: missing %r" % (where, r))
        for k, sub in schema.get("properties", {}).items():
            if k in value:
                errs += mini_validate(value[k], sub, "%s.%s" % (where, k))
    return errs


def validate_shape(m):
    try:
        import jsonschema
    except ImportError:
        return [e for p in PROFILES.values() for e in mini_validate(m, p)]
    return ["%s: %s" % ("/".join(map(str, e.absolute_path)) or "map", e.message)
            for p in PROFILES.values() for e in jsonschema.Draft202012Validator(p).iter_errors(m)]


def fields(profile, part):
    """Field names a profile defines for the map ('top'), its nodes or its edges."""
    props = PROFILES[profile].get("properties", {})
    if part == "top":
        return set(props)
    return set(props.get(part, {}).get("items", {}).get("properties", {}))


def check(m):
    """Return (errors, warnings) for one map. Rule numbers refer to protocol/README.md."""
    errs, warns = validate_shape(m), []
    if errs:
        return errs, warns  # the rules below assume the shape holds
    declared, undeclared = {"core", *m.get("profiles", [])}, {}
    # 6, 7: every field belongs to some profile, and that profile is declared
    for part, items in (("top", [m]), ("nodes", m["nodes"]), ("edges", m["edges"])):
        known = {p: fields(p, part) for p in PROFILES}
        for x in items:
            for k in x:
                owners = [p for p, f in known.items() if k in f]
                where = "map" if part == "top" else "%s %s" % (part[:-1], x.get("id") or "%s->%s" % (x["from"], x["to"]))
                if not owners:
                    warns.append("%s: unknown field %r" % (where, k))
                elif not declared & set(owners):
                    undeclared.setdefault(owners[0], set()).add(k)
    for prof, ks in sorted(undeclared.items()):
        warns.append("uses %s from the %s profile; add %r to 'profiles'" % (", ".join(sorted(ks)), prof, prof))
    ids = [n["id"] for n in m["nodes"]]
    idset = set(ids)
    if len(ids) != len(idset):  # 1
        errs.append("duplicate node ids: %s" % sorted({i for i in ids if ids.count(i) > 1}))
    if m["nodes"][0].get("parent"):  # 2
        errs.append("the first node is the root and cannot have a parent")
    by = {n["id"]: n for n in m["nodes"]}
    for n in m["nodes"]:
        if n.get("parent") and n["parent"] not in idset:  # 3
            errs.append("%s: parent %r does not exist" % (n["id"], n["parent"]))
        seen, cur = set(), n
        while cur and cur.get("parent"):  # 4
            if cur["id"] in seen:
                errs.append("cycle at %s" % n["id"])
                break
            seen.add(cur["id"])
            cur = by.get(cur["parent"])
        if n.get("kind") and n["kind"] not in KINDS:  # 12
            warns.append("%s: kind %r is not a listed rendering hint" % (n["id"], n["kind"]))
    for e in m["edges"]:
        name = "edge %s->%s" % (e["from"], e["to"])
        for end in ("from", "to"):  # 5
            if e[end] not in idset:
                errs.append("%s: %r does not exist" % (name, e[end]))
        if e.get("inference") == "deductive" and not e.get("given"):  # 8
            warns.append("%s: deductive but no 'given'; a deduction is only as good as its premises" % name)
        if "grades" in declared and not e.get("confidence"):  # 9
            warns.append("%s: the map uses grades but this edge has no confidence" % name)
        if e.get("strength") and not e.get("confidence"):  # 10
            warns.append("%s: a strength with no confidence reads as certain; grade both" % name)
    if any(n.get("falsifier") for n in m["nodes"]):  # 11
        for n in m["nodes"]:
            if n.get("weight") and not (n.get("falsifier") or n.get("measure")):
                warns.append("%s: carries a weight but has neither a falsifier nor, if it is true by construction, a measure" % n["id"])
    return errs, warns


def main(paths):
    if not paths:
        print(__doc__.strip())
        return 2
    failed = 0
    for p in paths:
        try:
            m = json.loads(Path(p).read_text())
        except (OSError, ValueError) as e:
            print("error: %s: %s" % (p, e))
            failed += 1
            continue
        errs, warns = check(m)
        for w in warns:
            print("warning: %s: %s" % (p, w))
        for e in errs:
            print("error: %s: %s" % (p, e))
        if errs:
            failed += 1
        else:
            print("ok: %s (%d nodes, %d edges)" % (p, len(m["nodes"]), len(m["edges"])))
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
