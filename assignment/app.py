import json
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load questions from JSON file
with open('data/sorting_questions.json', 'r') as file:
    questions = json.load(file)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask_question():
    data = request.get_json()
    question_id = str(data.get('question_id'))
    user_answer = data.get('answer')

    if question_id in questions:
        if user_answer is None:  # Start of the lesson, return the first question
            return jsonify({"question": questions[question_id]["question"]})
        else:
            correct_answer = questions[question_id]["answer"]
            if user_answer.strip().lower() == correct_answer.lower():
                next_question_id = int(question_id) + 1
                if str(next_question_id) in questions:
                    return jsonify({"result": "Correct!", "next_question": next_question_id, "question": questions[str(next_question_id)]["question"]})
                else:
                    return jsonify({"result": "Correct! No more questions!"})
            else:
                return jsonify({"result": "Incorrect, try again!"})

    return jsonify({"error": "Question not found!"})

if __name__ == '__main__':
    app.run(debug=True)
