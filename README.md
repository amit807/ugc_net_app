# 🚀 UGC NET Personal Exam Engine (Pre-AI Version)

## 📌 Overview

This is a custom-built UGC NET preparation platform created using
Python + Streamlit.

This version includes:

-   CSV-based question database
-   Dynamic Paper → Unit → Subtopic filtering
-   15 / 50 / 100 mark test modes
-   NTA-style question navigation
-   Question palette
-   Performance tracking
-   Weak topic detection
-   Full exam simulation mode

This version does NOT include AI-based dynamic question generation yet.
It runs entirely from a structured CSV question bank.

------------------------------------------------------------------------

## 🧠 System Architecture

### 1️⃣ Question Database (CSV Driven)

All questions are stored in:

ugc_questions.csv

Required format:

paper,unit,subtopic,difficulty,marks_type,question,option1,option2,option3,option4,correct_answer

The UI dynamically reads values from this file.

------------------------------------------------------------------------

### 2️⃣ Sidebar Structure

The sidebar allows selection of:

-   Paper
-   Unit
-   Subtopic
-   Test Type (Daily / Medium / Full / Weak Topic)

Dropdown values are dynamically generated from the CSV file.

------------------------------------------------------------------------

### 3️⃣ Test Modes

🟢 Daily (15) → marks_type = 15\
🟡 Medium (50) → marks_type = 50\
🔴 Full (100) → marks_type = 100\
⚫ Weak Topic Test → Accuracy \< 60%

------------------------------------------------------------------------

### 4️⃣ NTA-Style Navigation

-   One question at a time
-   Next / Previous buttons
-   Question palette
-   Attempted questions highlighted
-   Submit button calculates score

------------------------------------------------------------------------

### 5️⃣ Performance Tracking

Tracks:

-   Subtopic-wise accuracy
-   Weak topics
-   Strong topics
-   Average performance

All stored in Streamlit session state.

------------------------------------------------------------------------

## ⚙️ How To Run

1.  Install requirements:

pip install streamlit pandas

2.  Place files in same folder:

-   ugc_net_app.py
-   ugc_questions.csv

3.  Run:

streamlit run ugc_net_app.py

------------------------------------------------------------------------

## 📂 Project Structure

UGC_NET/ │ ├── ugc_net_app.py ├── ugc_questions.csv └── README.md

------------------------------------------------------------------------

## 🎯 Future Upgrades

-   AI question generator
-   Adaptive difficulty system
-   Analytics graphs
-   Weekly study planner
-   Timer-based real exam simulation

------------------------------------------------------------------------

## 👩‍🎓 Built For

UGC NET aspirants who want structured, exam-style preparation.

This is the stable version before AI integration.
