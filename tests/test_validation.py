import unittest

from fastcharge.validation import validate_reason, validate_registration


class ValidationTests(unittest.TestCase):
    def test_valid_registration(self):
        self.assertEqual(
            validate_registration("Mario Rossi", "mario@example.com", "Riunione"),
            [],
        )

    def test_all_required_fields(self):
        errors = validate_registration("", "non valida", "")
        self.assertEqual(len(errors), 3)

    def test_reason_length(self):
        self.assertIsNotNone(validate_reason(""))
        self.assertIsNotNone(validate_reason("x" * 301))


if __name__ == "__main__":
    unittest.main()
