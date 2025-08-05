# simulate_oracle_with_custom_lists.py
# Simulates an AI oracle that validates NLP results before blockchain transmission

import spacy
from datetime import datetime
import hashlib
import json

# ✅ Define your custom medical term lists here
custom_drugs = ["ibuprofen", "paracetamol", "aspirin", "naproxen", "penicillin"]
custom_symptoms = ["headache", "fever", "cough", "fatigue", "nausea"]


def validate_nlp_entities(doc, confidence_threshold=0.7):
    """
    Validates and enriches entities extracted by spaCy,
    using custom medical dictionaries for drug and symptom detection.
    """

    print("\n🔍 Oracle Validation Started...\n")

    validated_entities = []

    # Check each token against custom lists
    for token in doc:
        lower_text = token.text.lower()

        if any(drug in lower_text for drug in custom_drugs):
            label = "DRUG"
            confidence = 0.95
            validated_entities.append({
                "text": token.text,
                "label": label,
                "confidence": confidence
            })
            print(f"💊 '{token.text}' → {label} | Confidence: {confidence:.2f}")

        elif any(symptom in lower_text for symptom in custom_symptoms):
            label = "SYMPTOM"
            confidence = 0.90
            validated_entities.append({
                "text": token.text,
                "label": label,
                "confidence": confidence
            })
            print(f"🩺 '{token.text}' → {label} | Confidence: {confidence:.2f}")

        # Also check spaCy's standard entities
        elif token.ent_type_:
            label = token.ent_type_
            confidence = 0.85
            if confidence >= confidence_threshold:
                validated_entities.append({
                    "text": token.text,
                    "label": label,
                    "confidence": confidence
                })
                print(f"🧾 '{token.text}' → {label} | Confidence: {confidence:.2f}")

    return validated_entities


def enrich_with_metadata(validated_entities):
    """
    Adds metadata such as timestamp, source, institution, patient ID
    """
    enriched_data = {
        "raw_entities": validated_entities,
        "timestamp": str(datetime.now()),
        "institution": "CHU Alger",
        "patient_id": "PAT_123456",
        "status": "Oracle validation passed"
    }
    return enriched_data


def generate_hash(data):
    """
    Generates SHA-256 hash for data integrity verification
    """
    input_str = json.dumps(data, sort_keys=True).encode('utf-8')
    return hashlib.sha256(input_str).hexdigest()


def main():
    print("🚀 Starting NLP + AI Oracle Simulation\n")

    # Load spaCy model
    try:
        nlp = spacy.load("en_core_web_sm")
    except Exception as e:
        print("❌ Error: Could not load spaCy model.")
        print("👉 Run: python -m spacy download en_core_web_sm")
        raise e

    # Sample text
    text = """
    The patient underwent an MRI scan due to persistent headaches and fatigue.
    No critical condition was found. The doctor prescribed ibuprofen 400mg twice daily for pain relief.
    """

    print("📄 Input Medical Report:")
    print(text)

    # Apply NLP pipeline
    doc = nlp(text)

    print("\n🧾 Tokens & Labels from spaCy:")
    for token in doc:
        if token.ent_type_ or any(token.text.lower() in lst for lst in [custom_drugs, custom_symptoms]):
            print(f"{token.text:15} → {token.ent_type_ or 'Custom'}")

    # Validate using AI oracle logic
    validated_entities = validate_nlp_entities(doc)

    if not validated_entities:
        print("\n⚠️ No valid entities found. Oracle validation failed.")
        return

    # Enrich with metadata
    enriched_data = enrich_with_metadata(validated_entities)

    # Generate hash for secure transmission
    hash_value = generate_hash(enriched_data)
    enriched_data["hash"] = hash_value

    # Print structured output
    print("\n📦 Data Ready for Blockchain Transmission:")
    from pprint import pprint
    pprint(enriched_data)

    # Save to JSON
    with open("data_for_blockchain.json", "w") as f:
        json.dump(enriched_data, f, indent=2)
    print("\n✅ Data saved to 'data_for_blockchain.json'")


if __name__ == "__main__":
    main()
