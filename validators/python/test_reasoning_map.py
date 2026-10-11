"""python3 -m unittest discover validators/python

Fixtures are abstract on purpose (ids a, b, c): this repo holds no real reasoning, not even in tests.
"""
import copy, unittest
from reasoning_map import check

BASE = {
    "id": "t", "title": "T", "profiles": ["reasoning", "grades"],
    "nodes": [{"id": "r", "label": "Root"}, {"id": "a", "label": "A"}, {"id": "b", "label": "B", "parent": "a"}],
    "edges": [{"from": "a", "to": "r", "inference": "inductive", "strength": "medium", "confidence": "suggestive"}],
}


def run(change=lambda m: None):
    m = copy.deepcopy(BASE)
    change(m)
    return check(m)


class Valid(unittest.TestCase):
    def test_base_is_clean(self):
        self.assertEqual(run(), ([], []))

    def test_core_only_map_is_complete(self):
        m = {"id": "t", "title": "T", "nodes": [{"id": "r", "label": "R"}], "edges": []}
        self.assertEqual(check(m), ([], []))


class Errors(unittest.TestCase):
    def assertError(self, change, text):
        errs, _ = run(change)
        self.assertTrue(any(text in e for e in errs), errs)

    def test_shape(self):
        self.assertError(lambda m: m.pop("nodes"), "nodes")
        self.assertError(lambda m: m["edges"][0].update(inference="hunch"), "hunch")
        self.assertError(lambda m: m["edges"][0].update(confidence="certain"), "certain")

    def test_duplicate_ids(self):
        self.assertError(lambda m: m["nodes"].append({"id": "a", "label": "A2"}), "duplicate")

    def test_root_has_no_parent(self):
        self.assertError(lambda m: m["nodes"][0].update(parent="a"), "root")

    def test_parent_exists(self):
        self.assertError(lambda m: m["nodes"][2].update(parent="x"), "parent 'x'")

    def test_parent_cycle(self):
        def cycle(m):
            m["nodes"][1]["parent"] = "b"
        self.assertError(cycle, "cycle")

    def test_edge_ends_exist(self):
        self.assertError(lambda m: m["edges"].append({"from": "a", "to": "x", "confidence": "folklore"}), "'x' does not exist")


class Warnings(unittest.TestCase):
    def assertWarns_(self, change, text):
        errs, warns = run(change)
        self.assertEqual(errs, [])
        self.assertTrue(any(text in w for w in warns), warns)

    def test_unknown_field(self):
        self.assertWarns_(lambda m: m["edges"][0].update(strenght="large"), "unknown field 'strenght'")

    def test_undeclared_profile(self):
        self.assertWarns_(lambda m: m.update(profiles=["reasoning"]), "grades profile")

    def test_deductive_needs_given(self):
        self.assertWarns_(lambda m: m["edges"][0].update(inference="deductive"), "given")

    def test_graded_map_grades_every_edge(self):
        self.assertWarns_(lambda m: m["edges"].append({"from": "b", "to": "r"}), "no confidence")

    def test_strength_needs_confidence(self):
        self.assertWarns_(lambda m: m["edges"][0].pop("confidence"), "reads as certain")

    def test_weight_needs_falsifier_once_falsifiers_are_used(self):
        def change(m):
            m["nodes"][1]["falsifier"] = "F"
            m["nodes"][2]["weight"] = "High"
        self.assertWarns_(change, "neither a falsifier")

    def test_measure_satisfies_falsifier_rule(self):
        def change(m):
            m["nodes"][1]["falsifier"] = "F"
            m["nodes"][2].update(weight="High", measure="M")
        self.assertEqual(run(change), ([], []))

    def test_unknown_kind(self):
        self.assertWarns_(lambda m: m["nodes"][1].update(kind="blob"), "rendering hint")


if __name__ == "__main__":
    unittest.main()
