"""
Neural Network Weight Engine for Valuation Method Ensemble.
Implements a Multi-Layer Perceptron (MLP) neural network that trains on
sector and financial metrics to calculate defensible, normalized method weights
(summing to 1.0) for each sector and company profile.
"""

import numpy as np
import math
import uuid
import csv
import io
import logging
from typing import Dict, Any, List, Tuple, Optional
from datetime import datetime

from src.database import (
    save_trained_weights, get_latest_trained_weights,
    save_training_run, get_latest_training_run
)

logger = logging.getLogger("neural_weight_engine")

VALUATION_METHODS = [
    "FCFF DCF",
    "P/E",
    "P/B",
    "EV/EBITDA",
    "EV/EBIT",
    "Residual Income",
    "DDM"
]

SECTOR_LIST = [
    "Banks & NBFCs",
    "IT Services",
    "FMCG / Consumer",
    "Manufacturing / Auto",
    "Infrastructure / EPC",
    "Pharmaceuticals"
]

SECTOR_ELIGIBLE_METHODS = {
    "Banks & NBFCs": ["P/B", "Residual Income", "DDM", "P/E"],
    "IT Services": ["FCFF DCF", "P/E", "EV/EBIT"],
    "FMCG / Consumer": ["FCFF DCF", "P/E", "EV/EBITDA"],
    "Manufacturing / Auto": ["FCFF DCF", "P/E", "EV/EBITDA"],
    "Infrastructure / EPC": ["FCFF DCF", "EV/EBITDA", "P/E"],
    "Pharmaceuticals": ["FCFF DCF", "P/E", "EV/EBITDA"],
}

DEFAULT_SECTOR_WEIGHTS = {
    "Banks & NBFCs": {
        "P/B": 0.40,
        "Residual Income": 0.35,
        "DDM": 0.15,
        "P/E": 0.10
    },
    "IT Services": {
        "FCFF DCF": 0.45,
        "P/E": 0.35,
        "EV/EBIT": 0.20
    },
    "FMCG / Consumer": {
        "FCFF DCF": 0.40,
        "P/E": 0.35,
        "EV/EBITDA": 0.25
    },
    "Manufacturing / Auto": {
        "FCFF DCF": 0.35,
        "EV/EBITDA": 0.35,
        "P/E": 0.30
    },
    "Infrastructure / EPC": {
        "FCFF DCF": 0.40,
        "EV/EBITDA": 0.35,
        "P/E": 0.25
    },
    "Pharmaceuticals": {
        "FCFF DCF": 0.40,
        "P/E": 0.35,
        "EV/EBITDA": 0.25
    },
}

class NeuralWeightOptimizer:
    """
    Feedforward Neural Network with Softmax Method Masking.
    Architecture:
    Input [Sector One-Hot (6) + Features (6) = 12 dims]
    -> Layer 1: Dense (32) + ReLU
    -> Layer 2: Dense (16) + ReLU
    -> Output Layer: Dense (7 methods) + Sector Mask + Softmax
    """
    def __init__(self, seed: int = 42):
        np.random.seed(seed)
        self.input_dim = len(SECTOR_LIST) + 6  # sector + 6 normalized metrics
        self.h1_dim = 32
        self.h2_dim = 16
        self.out_dim = len(VALUATION_METHODS)

        # He initialization
        self.W1 = np.random.randn(self.input_dim, self.h1_dim) * np.sqrt(2.0 / self.input_dim)
        self.b1 = np.zeros((1, self.h1_dim))

        self.W2 = np.random.randn(self.h1_dim, self.h2_dim) * np.sqrt(2.0 / self.h1_dim)
        self.b2 = np.zeros((1, self.h2_dim))

        self.W3 = np.random.randn(self.h2_dim, self.out_dim) * np.sqrt(2.0 / self.h2_dim)
        self.b3 = np.zeros((1, self.out_dim))

    def _softmax_masked(self, logits: np.ndarray, sector: str) -> np.ndarray:
        """
        Masks out non-eligible methods for the sector with -infinity and applies softmax.
        """
        eligible = SECTOR_ELIGIBLE_METHODS.get(sector, VALUATION_METHODS)
        masked = logits.copy()
        for i, m in enumerate(VALUATION_METHODS):
            if m not in eligible:
                masked[0, i] = -1e9

        shift_logits = masked - np.max(masked)
        exps = np.exp(shift_logits)
        weights = exps / np.sum(exps)
        return weights

    def forward(self, x: np.ndarray, sector: str) -> Tuple[np.ndarray, Dict[str, np.ndarray]]:
        """
        Forward propagation.
        """
        z1 = np.dot(x, self.W1) + self.b1
        a1 = np.maximum(0, z1)  # ReLU

        z2 = np.dot(a1, self.W2) + self.b2
        a2 = np.maximum(0, z2)  # ReLU

        logits = np.dot(a2, self.W3) + self.b3
        weights = self._softmax_masked(logits, sector)

        cache = {
            "x": x, "z1": z1, "a1": a1,
            "z2": z2, "a2": a2, "logits": logits, "weights": weights
        }
        return weights, cache

    def train_on_dataset(
        self,
        samples: List[Dict[str, Any]],
        epochs: int = 60,
        learning_rate: float = 0.015
    ) -> List[float]:
        """
        Trains the neural network to minimize weighted valuation error vs target fair values.
        Uses Adam gradient descent.
        """
        if not samples:
            return []

        # Adam optimizer state variables
        mW1, vW1 = np.zeros_like(self.W1), np.zeros_like(self.W1)
        mb1, vb1 = np.zeros_like(self.b1), np.zeros_like(self.b1)
        mW2, vW2 = np.zeros_like(self.W2), np.zeros_like(self.W2)
        mb2, vb2 = np.zeros_like(self.b2), np.zeros_like(self.b2)
        mW3, vW3 = np.zeros_like(self.W3), np.zeros_like(self.W3)
        mb3, vb3 = np.zeros_like(self.b3), np.zeros_like(self.b3)

        beta1, beta2, eps = 0.9, 0.999, 1e-8
        t = 0
        loss_history = []

        for ep in range(1, epochs + 1):
            epoch_loss = 0.0
            dW1 = np.zeros_like(self.W1)
            db1 = np.zeros_like(self.b1)
            dW2 = np.zeros_like(self.W2)
            db2 = np.zeros_like(self.b2)
            dW3 = np.zeros_like(self.W3)
            db3 = np.zeros_like(self.b3)

            for s in samples:
                x = s["features"]
                sector = s["sector"]
                target_val = s["target_fair_value"]
                method_vals = s["method_values"]

                weights, cache = self.forward(x, sector)

                # Predicted fair value = sum_i (w_i * V_i)
                pred_val = float(np.sum(weights[0] * method_vals))
                diff = (pred_val - target_val) / max(target_val, 1.0)
                loss = 0.5 * (diff ** 2)
                epoch_loss += loss

                # Backprop: dLoss/dWeights
                d_pred = diff / max(target_val, 1.0)
                d_weights = d_pred * method_vals

                # Softmax derivative: dLoss/dLogits
                # For softmax: dL/dz_i = w_i * (dL/dw_i - sum_j(w_j * dL/dw_j))
                w = weights[0]
                dot_w_dw = np.sum(w * d_weights)
                d_logits = w * (d_weights - dot_w_dw)
                d_logits = d_logits.reshape(1, -1)

                # Gradient through Layer 3
                dW3 += np.dot(cache["a2"].T, d_logits)
                db3 += d_logits

                # Gradient through Layer 2
                da2 = np.dot(d_logits, self.W3.T)
                dz2 = da2 * (cache["z2"] > 0)
                dW2 += np.dot(cache["a1"].T, dz2)
                db2 += dz2

                # Gradient through Layer 1
                da1 = np.dot(dz2, self.W2.T)
                dz1 = da1 * (cache["z1"] > 0)
                dW1 += np.dot(cache["x"].T, dz1)
                db1 += dz1

            # Average gradients
            N = len(samples)
            epoch_loss /= N
            loss_history.append(float(epoch_loss))

            # Weight regularization (L2)
            l2 = 0.001
            dW1 = (dW1 / N) + l2 * self.W1
            db1 = (db1 / N)
            dW2 = (dW2 / N) + l2 * self.W2
            db2 = (db2 / N)
            dW3 = (dW3 / N) + l2 * self.W3
            db3 = (db3 / N)

            # Adam update step
            t += 1
            for param, grad, m, v in [
                (self.W1, dW1, mW1, vW1), (self.b1, db1, mb1, vb1),
                (self.W2, dW2, mW2, vW2), (self.b2, db2, mb2, vb2),
                (self.W3, dW3, mW3, vW3), (self.b3, db3, mb3, vb3)
            ]:
                m[:] = beta1 * m + (1 - beta1) * grad
                v[:] = beta2 * v + (1 - beta2) * (grad ** 2)
                m_hat = m / (1.0 - beta1 ** t)
                v_hat = v / (1.0 - beta2 ** t)
                param -= learning_rate * m_hat / (np.sqrt(v_hat) + eps)

        return loss_history

def parse_and_prepare_training_samples(csv_content: str) -> List[Dict[str, Any]]:
    """
    Parses uploaded or default CSV and generates feature vectors and synthetic/approx method values
    for training the neural network.
    """
    reader = csv.DictReader(io.StringIO(csv_content.strip()))
    samples = []

    for row in reader:
        try:
            sector = row.get("sector", "").strip()
            if not sector:
                continue

            # Read numerical features
            growth = float(row.get("revenue_growth", 0.10) or 0.10)
            margin = float(row.get("operating_margin", 0.20) or 0.20)
            roe = float(row.get("roe", 0.15) or 0.15)
            debt_eq = float(row.get("debt_to_equity", 0.5) or 0.5)
            pe = float(row.get("pe_ratio", 20.0) or 20.0)
            pb = float(row.get("pb_ratio", 3.0) or 3.0)
            market_price = float(row.get("market_price", 1000.0) or 1000.0)
            actual_fair_value = float(row.get("actual_fair_value", market_price * 1.05) or (market_price * 1.05))

            # Feature vector: Sector one-hot + normalized metrics
            sec_one_hot = [1.0 if s == sector else 0.0 for s in SECTOR_LIST]
            metrics = [
                max(-1.0, min(growth / 0.5, 2.0)),
                max(-0.5, min(margin / 0.5, 2.0)),
                max(-0.5, min(roe / 0.5, 2.0)),
                max(0.0, min(debt_eq / 3.0, 3.0)),
                max(0.0, min(pe / 60.0, 3.0)),
                max(0.0, min(pb / 15.0, 3.0)),
            ]
            feature_vec = np.array([sec_one_hot + metrics], dtype=np.float32)

            # Generate approximate/synthetic method fair values based on financial physics
            # Method index matching VALUATION_METHODS:
            # 0: FCFF DCF, 1: P/E, 2: P/B, 3: EV/EBITDA, 4: EV/EBIT, 5: Residual Income, 6: DDM
            method_vals = np.zeros(len(VALUATION_METHODS), dtype=np.float32)

            # DCF (favors high growth & margin)
            method_vals[0] = actual_fair_value * (1.0 + (growth - 0.10) * 0.5)
            # P/E
            method_vals[1] = actual_fair_value * (1.0 + (roe - 0.15) * 0.4)
            # P/B
            method_vals[2] = actual_fair_value * (1.0 - (pb - 3.0) * 0.05)
            # EV/EBITDA
            method_vals[3] = actual_fair_value * (1.0 + (margin - 0.20) * 0.4 - debt_eq * 0.05)
            # EV/EBIT
            method_vals[4] = actual_fair_value * (1.0 + (margin - 0.18) * 0.3)
            # Residual Income (favors high ROE)
            method_vals[5] = actual_fair_value * (1.0 + (roe - 0.14) * 0.6)
            # DDM
            method_vals[6] = actual_fair_value * 0.98

            samples.append({
                "company_id": row.get("company_id", ""),
                "sector": sector,
                "features": feature_vec,
                "target_fair_value": actual_fair_value,
                "method_values": method_vals
            })
        except Exception as e:
            logger.warning(f"Skipping malformed row: {e}")

    return samples

def train_neural_weights_from_csv(csv_text: str, epochs: int = 70) -> Dict[str, Any]:
    """
    Main entry point for model training:
    1. Parses CSV data
    2. Instantiates NeuralWeightOptimizer
    3. Trains across epochs
    4. Computes learned weights per sector
    5. Stores weights in SQLite trained_weights table and logs run
    6. Returns metrics & weight breakdown
    """
    samples = parse_and_prepare_training_samples(csv_text)
    if not samples:
        raise ValueError("CSV contains no valid company records for training")

    optimizer = NeuralWeightOptimizer(seed=42)
    loss_history = optimizer.train_on_dataset(samples, epochs=epochs, learning_rate=0.018)

    # Extract sector weights using sector centroids
    learned_weights: Dict[str, Dict[str, float]] = {}

    for sec in SECTOR_LIST:
        sec_samples = [s for s in samples if s["sector"] == sec]
        if sec_samples:
            avg_x = np.mean([s["features"] for s in sec_samples], axis=0)
        else:
            # Default centroid if sector not in samples
            sec_one_hot = [1.0 if s == sec else 0.0 for s in SECTOR_LIST]
            avg_x = np.array([sec_one_hot + [0.3, 0.4, 0.3, 0.3, 0.4, 0.3]], dtype=np.float32)

        weights, _ = optimizer.forward(avg_x, sec)
        w_vec = weights[0]

        eligible = SECTOR_ELIGIBLE_METHODS.get(sec, VALUATION_METHODS)
        sec_dict = {}
        for i, m in enumerate(VALUATION_METHODS):
            if m in eligible:
                sec_dict[m] = float(w_vec[i])

        # Normalize to exactly 1.0
        tot = sum(sec_dict.values())
        if tot > 0:
            for k in sec_dict:
                sec_dict[k] = round(sec_dict[k] / tot, 4)
        else:
            sec_dict = DEFAULT_SECTOR_WEIGHTS.get(sec, {})

        learned_weights[sec] = sec_dict

    # Save to SQLite database
    model_version = "v1.0"
    save_trained_weights(learned_weights, model_version=model_version)

    # Log training run
    run_id = f"run_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{uuid.uuid4().hex[:6]}"
    final_loss = loss_history[-1] if loss_history else 0.0
    initial_loss = loss_history[0] if loss_history else 0.0
    loss_improvement = ((initial_loss - final_loss) / max(initial_loss, 1e-6)) * 100.0

    # Sample epoch points for Chart.js display (e.g. 15 points)
    step = max(1, len(loss_history) // 15)
    sampled_loss_curve = [
        {"epoch": idx + 1, "loss": round(float(l), 6)}
        for idx, l in enumerate(loss_history) if idx % step == 0 or idx == len(loss_history) - 1
    ]

    metrics = {
        "initial_loss": round(initial_loss, 6),
        "final_loss": round(final_loss, 6),
        "loss_improvement_pct": round(loss_improvement, 2),
        "loss_curve": sampled_loss_curve,
        "sample_count": len(samples),
        "sectors_trained": list(learned_weights.keys()),
        "trained_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    save_training_run(
        run_id=run_id,
        num_samples=len(samples),
        epochs=epochs,
        final_loss=final_loss,
        metrics=metrics
    )

    return {
        "status": "Success",
        "run_id": run_id,
        "epochs": epochs,
        "sample_count": len(samples),
        "final_loss": round(final_loss, 6),
        "loss_improvement_pct": round(loss_improvement, 2),
        "loss_curve": sampled_loss_curve,
        "weights": learned_weights
    }

def get_current_model_weights() -> Dict[str, Dict[str, float]]:
    """
    Returns active trained weights from SQLite, falling back to defaults if not yet trained.
    """
    db_weights = get_latest_trained_weights(model_version="v1.0")
    if db_weights and len(db_weights) >= 3:
        return db_weights
    return DEFAULT_SECTOR_WEIGHTS
