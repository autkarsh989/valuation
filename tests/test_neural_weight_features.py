"""
Automated unit & integration tests for the Neural Network Weight Training & Replica AI-Valuation portal.
"""

import os
import unittest
from fastapi.testclient import TestClient

from app.main import app
from src.database import init_db, get_latest_trained_weights, get_latest_training_run
from src.neural_weight_engine import (
    train_neural_weights_from_csv,
    get_current_model_weights,
    SECTOR_LIST
)

class TestNeuralWeightFeatures(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.client = TestClient(app)
        init_db()

    def test_database_init_and_tables(self):
        weights = get_latest_trained_weights()
        self.assertIsInstance(weights, dict)

    def test_sample_csv_exists_and_download_endpoint(self):
        response = self.client.get("/api/train/sample-csv")
        self.assertEqual(response.status_code, 200)
        self.assertIn("company_id,legal_name,sector", response.text)
        self.assertGreaterEqual(len(response.text.splitlines()), 20)

    def test_neural_training_from_csv(self):
        csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_sector_training_data.csv")
        with open(csv_path, "r", encoding="utf-8") as f:
            csv_text = f.read()

        result = train_neural_weights_from_csv(csv_text, epochs=25)
        self.assertEqual(result["status"], "Success")
        self.assertGreaterEqual(result["sample_count"], 20)
        self.assertIn("weights", result)
        self.assertIn("loss_curve", result)
        self.assertGreater(len(result["loss_curve"]), 0)

        weights = result["weights"]
        for sec in SECTOR_LIST:
            self.assertIn(sec, weights)
            sec_weights = weights[sec]
            tot = sum(sec_weights.values())
            self.assertAlmostEqual(tot, 1.0, places=2)

    def test_endpoints_availability(self):
        # 1. Main index
        r1 = self.client.get("/")
        self.assertEqual(r1.status_code, 200)
        self.assertIn("Standard Valuation", r1.text)

        # 2. Train page
        r2 = self.client.get("/train")
        self.assertEqual(r2.status_code, 200)
        self.assertIn("Neural Weight Training Portal", r2.text)
        self.assertIn("Download Sample CSV", r2.text)

        # 3. Model-Valuation Replica page
        r3 = self.client.get("/model-valuation")
        self.assertEqual(r3.status_code, 200)
        self.assertIn("AI Model-Weighted Valuation", r3.text)

        # 4. Train Status API
        r4 = self.client.get("/api/train/status")
        self.assertEqual(r4.status_code, 200)
        data = r4.json()
        self.assertIn("current_weights", data)

        # 5. Model Companies API
        r5 = self.client.get("/api/companies/model-valuation")
        self.assertEqual(r5.status_code, 200)
        data5 = r5.json()
        self.assertIn("companies", data5)
        self.assertGreater(len(data5["companies"]), 0)

        # 6. Single Model Company API
        r6 = self.client.get("/api/company/HDFCBANK.NS/model-valuation")
        self.assertEqual(r6.status_code, 200)
        data6 = r6.json()
        self.assertEqual(data6["company"]["company_id"], "HDFCBANK.NS")
        self.assertIn("weights_applied", data6["valuation"])

    def test_upload_csv_and_train_api(self):
        csv_path = os.path.join(os.path.dirname(__file__), "..", "data", "sample_sector_training_data.csv")
        with open(csv_path, "rb") as f:
            r = self.client.post(
                "/api/train/upload",
                files={"file": ("training_data.csv", f, "text/csv")}
            )
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(data["status"], "Success")
        self.assertIn("weights", data)
        self.assertIn("Banks & NBFCs", data["weights"])
        self.assertIn("loss_curve", data)

if __name__ == "__main__":
    unittest.main()

