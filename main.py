from groq import Groq
from flask import Flask, render_template, request
import markdown
from dotenv import load_dotenv
import os
import random

load_dotenv()
api_key = os.getenv("API_KEY")
client = Groq(api_key=api_key)
journal_questions = [
    "What were the main things I did today?",
    "What moment stood out the most, and why?",
    "What made me feel happy or satisfied today?",
    "What challenged or frustrated me today?",
    "How did I respond to those challenges?",
    "Did I learn anything new today?",
    "What did I do well today?",
    "What could I have handled better?",
    "Did I spend my time in a way that aligns with my priorities?",
    "Who did I interact with, and how did those interactions affect me?",
    "Did anything surprise me today?",
    "What am I grateful for today?",
    "What drained my energy, and what gave me energy?",
    "Did I take care of my physical and mental well-being? How?",
    "What small wins did I achieve today?",
    "What thoughts kept coming back to me today?",
    "If I could relive one moment, what would I change?",
    "What is one thing I want to improve tomorrow?",
    "How would I summarize today in one sentence?"
]



app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        statement_1 = request.form.get('statement_1')
        statement_2 = request.form.get('statement_2')
        statement_3 = request.form.get('statement_3')
        statement_4 = request.form.get('statement_4')

        q1 = request.form.get('q1')
        q2 = request.form.get('q2')
        q3 = request.form.get('q3')

        prompt = (
            f"Create 3 or 4 short journaling ideas based on these:\n"
            f"{q1} {statement_1}\n"
            f"{q2} {statement_2}\n"
            f"{q3} {statement_3}\n"
            f"My mood is {statement_4}"
        )

        # print(prompt)
        completion_ai = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user",
                       "content": prompt
                       }]
        )

        journaling_idea_raw = completion_ai.choices[0].message.content
        journaling_idea = markdown.markdown(journaling_idea_raw)
        # print(journaling_idea)
        return render_template('index.html', journaling_idea=journaling_idea)
    selected_questions = random.sample(journal_questions, 3)
    return render_template('index.html', selected_questions=selected_questions)

if __name__ == '__main__':
    app.run(debug=False)


