# Python validator

Optional. One implementation of [the protocol](../../protocol/); the schemas and the rules in protocol/README.md are the spec, not this code.

```
python3 validators/python/reasoning_map.py my-map.json
```

Standard library only, Python 3.8+. If the `jsonschema` package is installed it is used for the shape check; otherwise a small built-in checker covers the subset of JSON Schema the profiles use. Exits 1 on errors; warnings print but do not fail.

As a library:

```python
from reasoning_map import check
errors, warnings = check(json.load(open("my-map.json")))
```

Tests: `python3 -m unittest discover validators/python`
