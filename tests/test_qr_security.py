from pathlib import Path
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import cv2
import numpy as np

from fastcharge.security import create_token, load_or_create_secret, verify_token
from fastcharge.services.qr import genera_qr_code


class QrSecurityTests(unittest.TestCase):
    def test_signed_token_round_trip_and_tampering(self):
        secret = b"test-secret"
        token = create_token("user-123", secret)
        self.assertEqual(verify_token(token, secret), "user-123")
        self.assertIsNone(verify_token(token.replace("user-123", "user-456"), secret))
        self.assertNotIn("email", token)

    def test_secret_is_persistent(self):
        with TemporaryDirectory() as directory:
            path = Path(directory) / "signing.key"
            first = load_or_create_secret(path)
            second = load_or_create_secret(path)
            self.assertEqual(first, second)
            self.assertEqual(len(first), 32)

    def test_generated_qr_can_be_decoded_by_opencv(self):
        token = create_token("user-123", b"test-secret")
        with TemporaryDirectory() as directory, patch.dict(
            "os.environ", {"FASTCHARGE_DATA_DIR": directory}
        ):
            image = genera_qr_code(token, "user-123", save_path=True).convert("RGB")
            frame = cv2.cvtColor(np.asarray(image), cv2.COLOR_RGB2BGR)
            decoded, _points, _straight = cv2.QRCodeDetector().detectAndDecode(frame)
            self.assertEqual(decoded, token)
            self.assertTrue((Path(directory) / "qr_codes" / "user-123.png").exists())


if __name__ == "__main__":
    unittest.main()
