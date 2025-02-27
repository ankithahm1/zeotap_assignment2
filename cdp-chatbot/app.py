import json
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load the documentation JSON files into memory
DATA_PATH = "data/"
CDP_DATA = {}

# Load all JSON files into memory
for filename in os.listdir(DATA_PATH):
    if filename.endswith(".json"):
        cdp_name = filename.replace(".json", "")
        with open(os.path.join(DATA_PATH, filename), "r", encoding="utf-8") as file:
            CDP_DATA[cdp_name] = json.load(file)["content"]

@app.route('/ask', methods=['POST'])
def ask_question():
    user_question = request.json.get("question", "").lower()

    if not user_question:
        return jsonify({"answer": "Please ask a valid question."}), 400  # Handle empty questions

    # Determine which CDP the question is about
    matched_cdp = None
    for cdp in CDP_DATA.keys():
        if cdp in user_question:
            matched_cdp = cdp
            break

    if not matched_cdp:
        return jsonify({"answer": "I can only answer questions related to Segment, mParticle, Lytics, and Zeotap."})

    # Find relevant content
    documentation = CDP_DATA.get(matched_cdp, "")
    relevant_info = find_relevant_answer(user_question, documentation)

    return jsonify({"answer": relevant_info})

def find_relevant_answer(question, documentation):
    """Simple search: return the most relevant part of the documentation."""
    if not documentation:
        return "Sorry, I couldn't find any information on this topic."

    sentences = documentation.split("\n")
    relevant_sentences = [sentence for sentence in sentences if question in sentence.lower()]
    
    if relevant_sentences:
        return " ".join(relevant_sentences[:3])  # Return the first 3 relevant sentences

    return "I couldn't find an exact answer, but you can check the official documentation."

    """Simple search: return the most relevant part of the documentation."""
    if not documentation:
        return "Sorry, I couldn't find any information on this topic."

    sentences = documentation.split("\n")
    for sentence in sentences:
        if question in sentence.lower():
            return sentence  # Return the first matching sentence

    return "I couldn't find an exact answer, but you can check the official documentation."

if __name__ == '__main__':
    app.run(debug=True)
