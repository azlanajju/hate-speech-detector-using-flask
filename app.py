from flask import Flask, request, render_template
import pandas as pd

app = Flask(__name__)

data = {'class': [0, 1, 1, 0, 1],
        'text': ['This is a neutral text', 'That word is offensive: fuck', 'No offensive language here', 'Another neutral example', 'Watch your language: bitch black boy']}
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

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        text_to_classify = request.form['text']
        result = classify_word(text_to_classify)
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
