# medical_nlp_extractor.py
# This script simulates the extraction of medical entities from free-text reports using spaCy,
# and enhances detection with custom keyword matching for drugs, symptoms, and tests

import spacy
from datetime import datetime

def main():
    print("🚀 Starting NLP processing for medical data simulation...\n")

    # Load spaCy English model
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        print("❌ Error: spaCy model 'en_core_web_sm' not found.")
        print("👉 Please install it with: python -m spacy download en_core_web_sm\n")
        return

    # Sample medical report
    text = """
    The patient underwent an MRI scan due to persistent headaches and fatigue.
    No critical condition was detected. The doctor prescribed ibuprofen 400mg twice daily for pain relief.
    """

    print("📄 Input Medical Report:")
    print(text)
    print("\n🔍 Starting NLP pipeline...\n")

    # Apply NLP pipeline
    doc = nlp(text)

    # Display entities recognized by spaCy
    print("🧾 Entities Extracted by spaCy:")
    if doc.ents:
        for ent in doc.ents:
            print(f"{ent.text:20} → {ent.label_}")
    else:
        print("⚠️ No named entities recognized by spaCy.")

    print()

    # Custom lists for manual recognition
    custom_drugs = ["ibuprofen", "paracetamol", "aspirin", "naproxen"]
    custom_symptoms = ["headache", "fatigue", "pain", "fever", "cough"]
    custom_tests = ["MRI", "CT", "X-ray", "ultrasound", "scan"]

    # Drug detection
    print("💊 Custom Drug Detection:")
    detected_drugs = [drug for drug in custom_drugs if drug.lower() in doc.text.lower()]
    if detected_drugs:
        for drug in detected_drugs:
            print(f" - '{drug}' detected manually")
    else:
        print(" - No drug keywords found")

    # Symptom detection
    print("\n🩺 Custom Symptom Detection:")
    detected_symptoms = [symptom for symptom in custom_symptoms if symptom.lower() in doc.text.lower()]
    if detected_symptoms:
        for symptom in detected_symptoms:
            print(f" - '{symptom}' detected manually")
    else:
        print(" - No symptom keywords found")

    # Test/exam detection
    print("\n🔬 Custom Medical Test Detection:")
    detected_tests = [test for test in custom_tests if test.lower() in doc.text.lower()]
    if detected_tests:
        for test in detected_tests:
            print(f" - '{test}' detected manually")
    else:
        print(" - No medical test keywords found")

    # Create structured output
    print("\n📊 Structured Output (JSON format):")

    structured_data = {
        "raw_text": text.strip(),
        "spacy_entities": [{"text": ent.text, "label": ent.label_} for ent in doc.ents],
        "custom_drug_matches": detected_drugs,
        "custom_symptom_matches": detected_symptoms,
        "custom_test_matches": detected_tests,
        "timestamp": str(datetime.now()),
        "status": "NLP extraction completed"
    }

    # Print JSON-like structure
    from pprint import pprint
    pprint(structured_data)

if __name__ == "__main__":
    main()
