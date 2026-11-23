import unittest

from bidi_audit import audit


class BidiTests(unittest.TestCase):
    def test_balanced_isolate(self):
        self.assertEqual(audit("اختبار \u2066AB-123\u2069"), [])

    def test_unclosed_isolate_and_orphan_pop(self):
        self.assertEqual(
            [(row["kind"], row["column"]) for row in audit("\u2069a\u2066b")],
            [("unmatched-closer", 1), ("unclosed-opener", 3)],
        )

    def test_override_warning_and_implicit_end(self):
        self.assertEqual(
            [row["kind"] for row in audit("\u2067\u202eAB\u2069")],
            ["override", "unclosed-opener"],
        )
