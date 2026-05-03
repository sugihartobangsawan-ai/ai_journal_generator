from groq import Groq
from flask import Flask, render_template, request
import markdown
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
client = Groq(api_key=api_key)


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        statement_1 = request.form.get('statement_1')
        statement_2 = request.form.get('statement_2')
        statement_3 = request.form.get('statement_3')
        completion_ai = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "user",
                       "content": f"Create 3 or 4 short journaling idea based on these:"
                                  f"best part of my day is {statement_1} and {statement_2} is keeping me busy and {statement_3} for today "
                       }]
        )
        journaling_idea_raw = completion_ai.choices[0].message.content
        journaling_idea = markdown.markdown(journaling_idea_raw)
        # print(journaling_idea)
        return render_template('index.html', journaling_idea=journaling_idea)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=False)


