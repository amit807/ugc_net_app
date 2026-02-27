import streamlit as st
import random
import pandas as pd

st.set_page_config(page_title="UGC NET Master Platform", layout="wide")

st.title("🚀 UGC NET Personal Master Platform")

# ----------- SYLLABUS -----------

syllabus = {
    "Paper 1": {
        "Teaching Aptitude": ["Nature of Teaching"],
    },
    "Economics": {
        "Microeconomics": ["Demand & Supply"],
    }
}

# ----------- QUESTION BANK -----------

import pandas as pd

# ----------- LOAD QUESTION DATABASE -----------

df_questions = pd.read_csv("ugc_questions.csv")
df_questions.columns = df_questions.columns.str.strip().str.lower()

# ----------- SESSION STORAGE -----------

if "performance" not in st.session_state:
    st.session_state.performance = []

# ----------- SIDEBAR -----------

st.sidebar.header("Test Setup")

# Paper dropdown
selected_paper = st.sidebar.selectbox(
    "Paper",
    df_questions["paper"].unique()
)

# Unit dropdown (filtered by selected paper)
selected_unit = st.sidebar.selectbox(
    "Unit",
    df_questions[df_questions["paper"] == selected_paper]["unit"].unique()
)

# Subtopic dropdown (filtered by selected unit)
selected_subtopic = st.sidebar.selectbox(
    "Subtopic",
    df_questions[
        (df_questions["paper"] == selected_paper) &
        (df_questions["unit"] == selected_unit)
    ]["subtopic"].unique()
)

# Test type
test_type = st.sidebar.radio(
    "Test Type",
    ["Daily (15)", "Medium (50)", "Full (100)", "Weak Topic Test"]
)
# ----------- FILTER QUESTIONS -----------

filtered_questions = df_questions[
    (df_questions["paper"] == selected_paper) &
    (df_questions["unit"] == selected_unit) &
    (df_questions["subtopic"] == selected_subtopic)
]

if test_type == "Daily (15)":
    filtered_questions = filtered_questions[filtered_questions["marks_type"] == 15]
elif test_type == "Medium (50)":
    filtered_questions = filtered_questions[filtered_questions["marks_type"] == 50]
elif test_type == "Full (100)":

    # Pull all questions from selected paper (ignore subtopic filter)
    filtered_questions = df_questions[
        df_questions["paper"] == selected_paper
    ]

    if filtered_questions.empty:
        st.warning("No questions available for this paper.")
        st.stop()

    num_questions = min(20, len(filtered_questions))  # change later if needed
    # Full test pulls all difficulties
    pass
elif test_type == "Weak Topic Test":
    # Weak logic already handled earlier
    pass
if filtered_questions.empty:
    st.warning("No questions available.")
    st.stop()

questions = filtered_questions.sample(
    min(len(filtered_questions), 5)
).to_dict("records")

# ----------- WEAK TOPIC TEST LOGIC -----------

if test_type == "Weak Topic Test":
    weak_topics = get_weak_topics = []

    if st.session_state.performance:
        df = pd.DataFrame(st.session_state.performance)
        topic_accuracy = df.groupby("subtopic")["correct"].mean()

        weak_topics = topic_accuracy[topic_accuracy < 0.6].index.tolist()

    filtered_questions = [q for q in question_bank if q["subtopic"] in weak_topics]

    if filtered_questions.empty:
        st.warning("No weak topics yet. Give some tests first.")
        st.stop()

# ----------- DETERMINE QUESTION COUNT -----------

if test_type == "Daily (15)":
    num_questions = min(3, len(filtered_questions))
elif test_type == "Medium (50)":
    num_questions = min(5, len(filtered_questions))
else:
    num_questions = min(10, len(filtered_questions))

if filtered_questions.empty:
    st.warning("No questions available.")
    st.stop()

if "test_started" not in st.session_state:
    st.session_state.test_started = False

if st.button("Start Test", key="start_test"):

    st.session_state.test_started = True

    st.session_state.questions = filtered_questions.sample(
        min(num_questions, len(filtered_questions))
    ).to_dict("records")

    st.session_state.current_question_index = 0
    st.session_state.answers = {}

if st.session_state.test_started:

    st.header("📝 Test")

    if st.session_state.test_started:

        questions = st.session_state.questions
        index = st.session_state.current_question_index
        q = questions[index]

    st.subheader(f"Question {index+1} of {len(questions)}")

    selected = st.radio(
        q["question"],
        [q["option1"], q["option2"], q["option3"], q["option4"]],
        key=f"q_{index}"
    )

    st.session_state.answers[index] = selected
    
     # -------- Navigation Buttons --------
    col1, col2, col3 = st.columns(3)

    with col1:
        if st.button("Previous", key="prev_btn"):
            if st.session_state.current_question_index > 0:
                st.session_state.current_question_index -= 1

    with col2:
        if st.button("Next", key="next_btn"):
            if st.session_state.current_question_index < len(questions) - 1:
                st.session_state.current_question_index += 1

    with col3:
        if st.button("Submit Test"):
            score = 0

            for i, q in enumerate(questions):

                user_ans = st.session_state.answers.get(i, None)

                if user_ans is not None and user_ans == q["correct_answer"]:
                    score += 1

            st.success(f"Your Score: {score} / {len(questions)}")
            st.session_state.test_started = False
    
     # -------- Step 4: Question Palette (ADD HERE) --------
    st.markdown("### Question Palette")

    cols = st.columns(5)

    for i in range(len(questions)):

        with cols[i % 5]:

            if i in st.session_state.answers:
                label = f"🟢 {i+1}"
            else:
                label = f"{i+1}"

            if st.button(label, key=f"palette_{i}"):
                st.session_state.current_question_index = i
    
    user_ans = st.session_state.answers.get(i)

    if user_ans is None:
        correct = False
    else:
        correct = user_ans == q["correct_answer"]

    if st.button("Submit Test", key="submit_exam"):

        score = 0

        for i, q in enumerate(st.session_state.questions):

            user_ans = st.session_state.answers.get(i, None)

            if user_ans is not None and user_ans == q["correct_answer"]:
                score += 1

        st.success(f"Your Score: {score} / {len(st.session_state.questions)}")

        st.session_state.test_started = False

# ----------- DASHBOARD -----------

st.header("📊 Performance Dashboard")

if st.session_state.performance:

    df = pd.DataFrame(st.session_state.performance)

    topic_accuracy = df.groupby("subtopic")["correct"].mean() * 100

    st.subheader("Subtopic Accuracy %")
    st.dataframe(topic_accuracy)

    # Classification
    weak_topics = topic_accuracy[topic_accuracy < 60]
    moderate_topics = topic_accuracy[(topic_accuracy >= 60) & (topic_accuracy < 80)]
    strong_topics = topic_accuracy[topic_accuracy >= 80]

    st.subheader("🧠 Topic Strength Analysis")

    st.write("🔴 Weak Topics (<60%)")
    st.write(list(weak_topics.index) if not weak_topics.empty else "None")

    st.write("🟡 Moderate Topics (60–80%)")
    st.write(list(moderate_topics.index) if not moderate_topics.empty else "None")

    st.write("🟢 Strong Topics (>80%)")
    st.write(list(strong_topics.index) if not strong_topics.empty else "None")

    # Weekly Summary
    st.subheader("📅 Weekly Summary")

    total_attempts = len(df)
    avg_accuracy = df["correct"].mean() * 100

    st.write(f"Total Questions Attempted: {total_attempts}")
    st.write(f"Average Accuracy: {round(avg_accuracy,2)}%")

    if not weak_topics.empty:
        most_weak = weak_topics.idxmin()
        st.write(f"Most Weak Subtopic: {most_weak}")

    if not strong_topics.empty:
        most_strong = strong_topics.idxmax()
        st.write(f"Strongest Subtopic: {most_strong}")

    # AI Coach Recommendation
    st.subheader("🤖 AI Coach Recommendation")

    if avg_accuracy < 60:
        st.warning("Focus on Daily Tests for weak subtopics.")
    elif avg_accuracy < 80:
        st.info("Do Medium Tests and revise weak areas.")
    else:
        st.success("You are ready for Full Mock Simulation.")

else:
    st.info("No performance data yet.")
    
    
