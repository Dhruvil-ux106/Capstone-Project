# 📝 AI Essay Evaluation & Analytics System

An AI-powered web application that evaluates student essays, provides structured feedback, and tracks writing performance over time using analytics dashboards.

---

## 🚀 Features

* ✍️ **Automated Essay Evaluation**

  * Grammar
  * Structure
  * Clarity
  * Argument
  * Tone

* 🧠 **AI-Powered Feedback**

  * Detects the most critical writing weakness
  * Provides concise analysis
  * Suggests actionable improvements

* 📊 **Analytics Dashboard**

  * Bar chart of score breakdown
  * Pie chart showing score distribution
  * Historical comparison of student performance

* 📈 **Performance Tracking**

  * Stores past submissions
  * Compares current essay with historical averages
  * Enables personalized insights

---

## 🛠️ Tech Stack

* **Frontend & UI:** Gradio
* **Backend:** Python
* **AI Model API:** Groq (LLM inference)
* **Data Handling:** Pandas
* **Visualization:** Matplotlib

---

## 📂 Project Structure

```
.
├── app.py              # Main application
├── requirements.txt   # Dependencies
├── history.csv        # Stored student data (auto-generated)
├── .env               # API keys (NOT pushed to GitHub)
└── README.md
```

---

## ⚙️ Setup & Installation

### 1. Clone Repository

```bash
git clone https://github.com/YOUR_USERNAME/essay-evaluator.git
cd essay-evaluator
```

---

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

---

### 3. Add Environment Variable

Create a `.env` file:

```env
GROQ_API_KEY=your_api_key_here
```

---

### 4. Run Application

```bash
python app.py
```

---

## 🌐 Deployment

This project is deployed on Hugging Face Spaces.

👉 **Live Demo:**
https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME

---

## 📊 How It Works

1. User enters student name and essay
2. AI evaluates essay using LLM
3. Scores + feedback are generated
4. Data is stored in `history.csv`
5. Dashboard visualizes:

   * Current performance
   * Score distribution
   * Historical comparison

---

## 🎯 Use Cases

* Educational platforms
* Writing skill assessment
* Student performance tracking
* AI-assisted grading systems

---

## 🔒 Security Note

* API keys are stored securely using environment variables
* `.env` file is excluded from version control

---

## 🧪 Future Improvements

* 📈 Trend graphs (progress over time)
* 🧠 Advanced rubric-based scoring
* 🗂️ Database integration (Firebase / SQL)
* 👥 Multi-user login system

