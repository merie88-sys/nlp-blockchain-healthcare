# simulate_smart_contract.py
# Simulates a basic blockchain smart contract that verifies off-chain hash
# and validates the consistency between off-chain and on-chain data

import hashlib
import json
from datetime import datetime


# Simulated smart contract address
CONTRACT_ADDRESS = "0x1234567890abcdef1234567890abcdef12345678"

# Simulated on-chain storage
on_chain_data = {}


def verify_hash(data_off_chain, stored_hash):
    """
    Compares the hash of the off-chain data with the one stored on-chain
    """
    input_str = json.dumps(data_off_chain, sort_keys=True).encode('utf-8')
    calculated_hash = hashlib.sha256(input_str).hexdigest()

    print(f"\n🔗 Off-chain hash : {calculated_hash}")
    print(f"📦 On-chain hash  : {stored_hash}")

    if calculated_hash == stored_hash:
        print("✅ Hash match : Data is consistent between off-chain and on-chain.")
        return True
    else:
        print("❌ Hash mismatch : Data integrity compromised.")
        return False


def execute_smart_contract(data_off_chain, stored_hash):
    """
    Simulates the execution of a smart contract that:
    - Verifies data consistency
    - Triggers a conditional action (e.g., reimbursement)
    """
    print("\n📜 Smart Contract Execution Started...\n")

    # Step 1: Verify hash
    if not verify_hash(data_off_chain, stored_hash):
        print("🚫 Smart contract execution halted. Data mismatch detected.")
        return False

    # Step 2: Apply business logic
    print("🔍 Analyzing data for conditional execution...")

    drugs = [ent["text"].lower() for ent in data_off_chain["valid_entities"] if ent["label"] == "DRUG"]
    symptoms = [ent["text"].lower() for ent in data_off_chain["valid_entities"] if ent["label"] == "SYMPTOM"]

    # Check if any variation of headache or pain is present
    headache_keywords = ["headache", "headaches", "pain", "migraine"]
    drug_keywords = ["ibuprofen", "paracetamol", "aspirin"]

    has_headache = any(symptom in symptoms for symptom in headache_keywords)
    has_drug = any(drug in drugs for drug in drug_keywords)

    if has_headache and has_drug:
        matched_headache = next((k for k in headache_keywords if k in symptoms), None)
        matched_drug = next((d for d in drug_keywords if d in drugs), None)

        print(f"💊 Condition matched: '{matched_headache}' + '{matched_drug}'")
        print("💰 Triggering reimbursement process...")
        return True
    else:
        print("⚠️ No matching condition found. No action triggered.")
        return False


def store_on_chain(data_off_chain):
    """
    Simulates storing the hash of off-chain data on-chain
    """
    input_str = json.dumps(data_off_chain, sort_keys=True).encode('utf-8')
    stored_hash = hashlib.sha256(input_str).hexdigest()

    on_chain_data["hash"] = stored_hash
    on_chain_data["timestamp"] = str(datetime.now())
    on_chain_data["status"] = "Data hash stored on-chain"
    on_chain_data["contract_address"] = CONTRACT_ADDRESS

    print("\n📦 Data stored on-chain:")
    from pprint import pprint
    pprint(on_chain_data)

    return stored_hash


# Example off-chain data from your AI Oracle
off_chain_data = {
    "valid_entities": [
        {"text": "headaches", "label": "SYMPTOM", "confidence": 0.90},
        {"text": "fatigue", "label": "SYMPTOM", "confidence": 0.90},
        {"text": "ibuprofen", "label": "DRUG", "confidence": 0.95}
    ],
    "timestamp": "2025-07-14T12:34:56Z",
    "institution": "CHU Alger",
    "patient_id": "PAT_123456",
    "status": "Oracle validation passed"
}


# Simulate the full process
if __name__ == "__main__":
    print("🚀 Starting Smart Contract Simulation")

    # Step 1: Store the off-chain data hash on-chain
    stored_hash = store_on_chain(off_chain_data)

    # Step 2: Smart contract execution
    result = execute_smart_contract(off_chain_data, stored_hash)

    if result:
        print("\n✅ Smart contract executed successfully.")
    else:
        print("\n❌ Smart contract did not trigger any action.")
