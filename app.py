from flask import Flask, render_template, request
from pymongo import MongoClient
import openai

app = Flask(__name__)

# MongoDB setup for "questions" collection
client_questions = MongoClient("mongodb://localhost:27017/")
db_questions = client_questions["questions"]
collection_questions = db_questions["sidehustle"]

# MongoDB setup for "user_response" collection
client_responses = MongoClient("mongodb://localhost:27017/")
db_responses = client_responses["user_response"]
collection_responses = db_responses["sidehustle"]

openai.api_key = "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"


@app.route("/index.html")
def index():
    return render_template("index.html")


@app.route("/categories/sidehustle.html", methods=["GET", "POST"])
def sidehustle():
    if request.method == "POST":
        user_input = request.form.get("user_input")  # Get the user input from the form
        # Store user input in "user_response" collection of "sidehustle" database
        collection_responses.insert_one({"user_input": user_input})

    var2 = "How much money do I need to start a coffee shop? Give an answer in no more than 1 sentence."

    # Generate response from OpenAI
    response = openai.Completion.create(
        engine="text-davinci-003", prompt=var2, max_tokens=50
    )
    answer = response.choices[0].text.strip()

    a = "Hello from Flask2"
    question_document = collection_questions.find_one()
    var1 = question_document["question"]

    return render_template("categories/sidehustle.html", a=a, var1=var1, answer=answer)


if __name__ == "__main__":
    app.run(port=3000, debug=True)
