# Translation Module Design

## 1. Overview
The Translation Module is the core intelligence layer of the
Garhwali–Kumaoni Voice-Enabled Assistant. It converts regional language
input into Hindi and English to enable cross-language communication
for elderly users and tourists.

---

## 2. Problem Context
Garhwali and Kumaoni are low-resource regional languages with:
- No standardized grammar rules
- Very limited digital datasets
- High dialect and pronunciation variation

Due to these constraints, fully trained neural translation models
are not readily available for direct deployment.

---

## 3. Current Prototype Approach (Round-2)
For Round-2, a **phrase-level rule-based NLP approach** is used to:

- Demonstrate translation feasibility
- Validate system integration
- Enable offline and low-connectivity usage

### Key Features
- Keyword-based language detection
- Phrase-level semantic mapping
- Hindi and English output
- Confidence score simulation

This approach represents an **early-stage NLP system** and is
intentionally designed to be replaceable.

---

## 4. Why This Module Is Critical
The translation module is the central component of the system.

Without accurate semantic translation:
- Voice input has no practical value
- Elderly users cannot communicate with non-local professionals
- Tourists cannot interact with local residents

This module is isolated behind a clean interface so that
future ML models can be integrated without changing other system components.

---

## 5. Limitations
- Limited vocabulary coverage
- No grammatical sentence restructuring
- Confidence scores are simulated
- Dialect variations not fully handled

These limitations are acceptable for prototype validation.

---

## 6. Future Improvements
- Community-driven data collection
- Fine-tuning transformer-based translation models
- Phonetic similarity matching
- Context-aware translation using embeddings
- Real confidence estimation using model probabilities

---

## 7. Scalability Considerations
- New languages can be added by extending phrase datasets
- Translation logic can be replaced with trained ML models
- Backend services remain unchanged due to modular design
