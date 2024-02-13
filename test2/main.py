from flask import Flask, request, jsonify
import pandas as pd
from flask_cors import CORS
import json

app = Flask(__name__)
CORS(app) 

# Load data from JSON file
with open('data.json', 'r') as f:
    data = json.load(f)

df = pd.DataFrame(data)

df['labels'] = df['class'].map({0: "Hate Speech Detected", 1: "Offensive language detected", 3: "No hate and Offensive Speech"})

offensive_words = ['fuck', 'bitch']
hate_speech_words = ['black boy','bad boy']

df['offensive_word'] = df['text'].str.contains('|'.join(offensive_words), case=False)
df['hate_speech'] = df['text'].str.contains('|'.join(hate_speech_words), case=False)

def classify_word(word):
    offensive_words = ['fuck', 'bitch']
    hate_speech_words = ['black boy','bad boy']

    is_offensive = any(offensive_word in word.lower() for offensive_word in offensive_words)
    is_hate_speech = any(hate_speech_word in word.lower() for hate_speech_word in hate_speech_words)

    if is_hate_speech:
        return "Hate Speech Detected"
    elif is_offensive:
        return "Offensive word"
    else:
        return "Neither"

@app.route('/classify', methods=['GET', 'POST'])
def classify_text():
    if request.method == 'POST':
        text_to_classify = request.form['text']
        result = classify_word(text_to_classify)
        return jsonify({'result': result})
    else:
        return 'Only POST requests are allowed for this endpoint', 405

if __name__ == '__main__':
    app.run(debug=True)
