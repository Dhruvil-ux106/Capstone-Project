import gradio as gr
import requests
import re
import os
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
HISTORY_FILE = "history.csv"


# -----------------------------
# Helpers
# -----------------------------
def extract(text, label):
    match = re.search(rf"{label}[^0-9]*(\d+)", text, re.I)
    return int(match.group(1)) if match else 0


def extract_text(text, label):
    match = re.search(rf"{label}:\s*(.*)", text, re.I)
    return match.group(1).strip() if match else "N/A"


# -----------------------------
# Save Submission History
# -----------------------------
def save_submission(student, grammar, structure, clarity, argument, tone, final_score):
    new_row = pd.DataFrame([{
        "Student": student,
        "Grammar": grammar,
        "Structure": structure,
        "Clarity": clarity,
        "Argument": argument,
        "Tone": tone,
        "FinalScore": final_score
    }])

    if os.path.exists(HISTORY_FILE):
        old = pd.read_csv(HISTORY_FILE)
        new_row = pd.concat([old, new_row], ignore_index=True)

    new_row.to_csv(HISTORY_FILE, index=False)


# -----------------------------
# AI Essay Analysis
# -----------------------------
def analyze_essay(student, essay):
    try:
        if not essay.strip():
            return (
                0, 0, 0, 0, 0, 0,
                "No Essay",
                "Please enter an essay.",
                "Provide essay input."
            )

        prompt = f"""
You are an academic writing evaluator.
Score the essay STRICTLY out of 100 for each category.
Return ONLY integer scores between 0 and 100.
Analyze the essay and identify the MOST IMPORTANT writing weakness.
Choose ONLY the most relevant weakness from:
- Weak Thesis Statement
- Poor Structure
- Repetitive Vocabulary
- Weak Argument Development
- Poor Paragraph Transitions
- Informal Tone
- Grammar Issues
- Weak Conclusion
Return EXACTLY in this format:
Grammar: [0-100]
Structure: [0-100]
Clarity: [0-100]
Argument: [0-100]
Tone: [0-100]
Weakness: [single weakness]
Analysis: [1 sentence]
Feedback: [1 suggestion]
Essay:
{essay}
"""

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "llama-3.3-70b-versatile",
                "messages": [{"role": "user", "content": prompt}]
            }
        )

        if response.status_code != 200:
            raise Exception(response.text)

        text = response.json()["choices"][0]["message"]["content"]

        grammar = float(extract(text, "Grammar"))
        structure = float(extract(text, "Structure"))
        clarity = float(extract(text, "Clarity"))
        argument = float(extract(text, "Argument"))
        tone = float(extract(text, "Tone"))

        if grammar <= 10: grammar *= 10
        if structure <= 10: structure *= 10
        if clarity <= 10: clarity *= 10
        if argument <= 10: argument *= 10
        if tone <= 10: tone *= 10

        weakness = extract_text(text, "Weakness")
        analysis = extract_text(text, "Analysis")
        feedback = extract_text(text, "Feedback")

        final_score = round(
            grammar * 0.30 +
            structure * 0.25 +
            clarity * 0.20 +
            argument * 0.15 +
            tone * 0.10,
            2
        )

        save_submission(
            student,
            grammar,
            structure,
            clarity,
            argument,
            tone,
            final_score
        )

        return (
            grammar,
            structure,
            clarity,
            argument,
            tone,
            final_score,
            weakness,
            analysis,
            feedback
        )

    except Exception as e:
        return (
            0, 0, 0, 0, 0, 0,
            "Backend Error",
            str(e),
            "Check terminal logs"
        )


# -----------------------------
# Dashboard Graphs
# -----------------------------
def generate_bar_chart(grammar, structure, clarity, argument, tone):
    categories = ["Grammar", "Structure", "Clarity", "Argument", "Tone"]
    scores = [grammar, structure, clarity, argument, tone]

    fig, ax = plt.subplots(figsize=(7, 4))
    ax.bar(categories, scores)
    ax.set_ylim(0, 100)
    ax.set_title("Score Breakdown")

    return fig


def generate_pie_chart(grammar, structure, clarity, argument, tone):
    labels = ["Grammar", "Structure", "Clarity", "Argument", "Tone"]
    scores = [grammar, structure, clarity, argument, tone]

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(scores, labels=labels, autopct="%1.1f%%")
    ax.set_title("Relative Score Distribution")

    return fig


def compare_history(student):
    if not os.path.exists(HISTORY_FILE):
        return "No historical data found."

    df = pd.read_csv(HISTORY_FILE)
    student_data = df[df["Student"] == student]

    if student_data.empty:
        return "No past essays found for this student."

    avg = student_data[
        ["Grammar", "Structure", "Clarity", "Argument", "Tone", "FinalScore"]
    ].mean()

    return f"""
Historical Performance for {student}
Average Grammar: {avg['Grammar']:.2f}
Average Structure: {avg['Structure']:.2f}
Average Clarity: {avg['Clarity']:.2f}
Average Argument: {avg['Argument']:.2f}
Average Tone: {avg['Tone']:.2f}
Average Final Score: {avg['FinalScore']:.2f}
"""


# -----------------------------
# UI
# -----------------------------
with gr.Blocks(theme=gr.themes.Soft()) as demo:

    gr.Markdown("# AI Essay Evaluation + Analytics Dashboard")

    with gr.Tab("Essay Evaluator"):

        student_name = gr.Textbox(label="Student Name")

        essay_input = gr.Textbox(
            lines=15,
            placeholder="Paste essay here...",
            label="Essay Input"
        )

        submit_btn = gr.Button("Analyze Essay")

        grammar = gr.Number(label="Grammar")
        structure = gr.Number(label="Structure")
        clarity = gr.Number(label="Clarity")
        argument = gr.Number(label="Argument")
        tone = gr.Number(label="Tone")
        final_score = gr.Number(label="Final Score")

        weakness = gr.Textbox(label="Weakness")
        analysis = gr.Textbox(label="Analysis")
        feedback = gr.Textbox(label="Feedback")

    with gr.Tab("Analytics Dashboard"):

        bar_chart = gr.Plot(label="Bar Chart")
        pie_chart = gr.Plot(label="Pie Chart")

        history_box = gr.Textbox(
            label="Historical Comparison",
            lines=8
        )

        dashboard_btn = gr.Button("Generate Dashboard")

    submit_btn.click(
        fn=analyze_essay,
        inputs=[student_name, essay_input],
        outputs=[
            grammar,
            structure,
            clarity,
            argument,
            tone,
            final_score,
            weakness,
            analysis,
            feedback
        ]
    )

    dashboard_btn.click(
        fn=generate_bar_chart,
        inputs=[grammar, structure, clarity, argument, tone],
        outputs=bar_chart
    )

    dashboard_btn.click(
        fn=generate_pie_chart,
        inputs=[grammar, structure, clarity, argument, tone],
        outputs=pie_chart
    )

    dashboard_btn.click(
        fn=compare_history,
        inputs=student_name,
        outputs=history_box
    )


demo.launch(server_name="0.0.0.0", server_port=7860)
