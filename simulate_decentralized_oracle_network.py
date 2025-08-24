# simulate_decentralized_oracle_network.py
# Simulates a decentralized oracle network with consensus and HITL fallback

import spacy
from datetime import datetime
import hashlib
import json
import random
from typing import List, Dict, Optional

# 🔹 Custom medical term lists
CUSTOM_DRUGS = ["ibuprofen", "paracetamol", "aspirin", "naproxen", "penicillin"]
CUSTOM_SYMPTOMS = ["headache", "fever", "cough", "fatigue", "nausea"]

# 🔹 System threshold
CONFIDENCE_THRESHOLD = 0.7


class OracleNode:
    """
    Represents a decentralized oracle node that validates NLP results
    and signs the output with ECDSA-style digital signature (simulated).
    """

    def __init__(self, node_id: str, private_key: str):
        self.node_id = node_id
        self.private_key = private_key  # Simulated private key

    def validate_entities(self, doc, custom_drugs, custom_symptoms) -> List[Dict]:
        """Validates entities using custom logic and returns enriched list."""
        validated = []

        for token in doc:
            lower_text = token.text.lower()

            if any(drug in lower_text for drug in custom_drugs):
                validated.append({
                    "text": token.text,
                    "label": "DRUG",
                    "confidence": 0.95
                })

            elif any(symptom in lower_text for symptom in custom_symptoms):
                validated.append({
                    "text": token.text,
                    "label": "SYMPTOM",
                    "confidence": 0.90
                })

            elif token.ent_type_:
                confidence = 0.85
                if confidence >= CONFIDENCE_THRESHOLD:
                    validated.append({
                        "text": token.text,
                        "label": token.ent_type_,
                        "confidence": confidence
                    })

        return validated

    def enrich_with_metadata(self, validated_entities: List[Dict]) -> Dict:
        """Adds contextual metadata and timestamp."""
        return {
            "entities": validated_entities,
            "timestamp": str(datetime.now()),
            "source": "NLP Module",
            "node_id": self.node_id,
            "status": "validated"
        }

    def generate_hash(self, data: Dict) -> str:
        """Generates SHA-256 hash for integrity."""
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode('utf-8')).hexdigest()

    def sign_hash(self, h: str) -> str:
        """Simulates ECDSA signature using private key."""
        return hashlib.sha256((h + self.private_key).encode('utf-8')).hexdigest()

    def process(self, doc) -> Optional[Dict]:
        """Full oracle processing pipeline."""
        try:
            print(f"\n🔍 Oracle {self.node_id} validating...")

            entities = self.validate_entities(doc, CUSTOM_DRUGS, CUSTOM_SYMPTOMS)
            if not entities:
                print(f"⚠️  Oracle {self.node_id}: No valid entities found.")
                return None

            enriched = self.enrich_with_metadata(entities)
            h = self.generate_hash(enriched)
            signature = self.sign_hash(h)

            result = {
                "node_id": self.node_id,
                "data": enriched,
                "hash": h,
                "signature": signature
            }

            print(f"✅ Oracle {self.node_id} output: {len(entities)} entities validated.")
            return result

        except Exception as e:
            print(f"❌ Oracle {self.node_id} failed: {e}")
            return None


def consensus_mechanism(oracle_outputs: List[Dict], threshold: int = 2) -> Optional[Dict]:
    """
    Performs consensus (e.g., 2-out-of-3 agreement) on validated data.
    Returns the final package if consensus is reached, else None.
    """
    print(f"\n🔐 Running Consensus Mechanism (threshold = {threshold})...")

    if len(oracle_outputs) < threshold:
        print("❌ Not enough oracle responses for consensus.")
        return None

    # For simplicity: check if at least `threshold` nodes agree on non-empty data
    valid_responses = [o for o in oracle_outputs if o is not None]

    if len(valid_responses) >= threshold:
        print(f"✅ Consensus achieved with {len(valid_responses)} valid responses.")
        return {
            "consensus": "success",
            "final_package": valid_responses[0]["data"],  # Simplified: take first
            "aggregated_hashes": [o["hash"] for o in valid_responses],
            "signatures": [o["signature"] for o in valid_responses]
        }
    else:
        print("❌ Consensus failed: not enough valid responses.")
        return None


def trigger_human_in_the_loop(input_text: str, oracle_outputs: List[Dict]):
    """
    Simulates human validation when consensus fails.
    In a real system, this would call a web interface.
    """
    print("\n🚨 Consensus failed. Triggering Human-in-the-Loop (HITL)...")
    print("📝 Original text:", input_text)
    print("🔍 Oracle discrepancies:")
    for o in oracle_outputs:
        if o:
            ents = [f"{e['text']}({e['label']})" for e in o['data']['entities']]
            print(f"  - {o['node_id']}: {', '.join(ents)}")

    print("\n👩‍⚕️ Human validator reviewing...")
    # Simulate correction
    corrected = {
        "entities": [
            {"text": "MRI", "label": "PROCEDURE", "confidence": 0.98},
            {"text": "headache", "label": "SYMPTOM", "confidence": 0.95},
            {"text": "fatigue", "label": "SYMPTOM", "confidence": 0.93},
            {"text": "ibuprofen", "label": "DRUG", "confidence": 0.97}
        ],
        "correction_reason": "Low confidence in NLP extraction for 'MRI'",
        "validator_id": "HITL_001",
        "timestamp": str(datetime.now())
    }
    print("✅ Correction applied by human validator.")
    return corrected


def main():
    print("🚀 Starting Decentralized Oracle Network Simulation\n")

    # Load spaCy model
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("❌ Error: Could not load spaCy model.")
        print("👉 Run: python -m spacy download en_core_web_sm")
        return

    # Sample text
    text = """
    The patient underwent an MRI scan due to persistent headaches and fatigue.
    No critical condition was found. The doctor prescribed ibuprofen 400mg twice daily for pain relief.
    """

    print("📄 Input Medical Report:")
    print(text)

    # Apply NLP
    doc = nlp(text)

    # Initialize 3 oracle nodes (decentralized network)
    oracles = [
        OracleNode("Oracle_A", "priv_key_A_123"),
        OracleNode("Oracle_B", "priv_key_B_456"),
        OracleNode("Oracle_C", "priv_key_C_789")
    ]

    # Each oracle processes the NLP output
    oracle_results = []
    for oracle in oracles:
        result = oracle.process(doc)
        oracle_results.append(result)

    # Consensus
    consensus_result = consensus_mechanism(oracle_results, threshold=2)

    final_data = None
    if consensus_result:
        final_data = consensus_result["final_package"]
        print("\n✅ Data approved by consensus. Ready for blockchain.")
    else:
        # Fallback to HITL
        corrected_data = trigger_human_in_the_loop(text, oracle_results)
        final_data = corrected_data

    # Final hash for blockchain
    final_hash = hashlib.sha256(json.dumps(final_data, sort_keys=True).encode('utf-8')).hexdigest()
    final_data["final_hash"] = final_hash

    # Save for smart contract
    with open("validated_data_for_blockchain.json", "w") as f:
        json.dump(final_data, f, indent=2)

    print(f"\n📦 Final data (hash: {final_hash[:16]}...) saved to 'validated_data_for_blockchain.json'")


if __name__ == "__main__":
    main()
