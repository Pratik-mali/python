from flask import Flask, request, jsonify
from flask_cors import CORS
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
import pandas as pd

app = Flask(__name__)
CORS(app)

# Load the dataset of Marathi words
try:
    df = pd.read_csv('marathi_words.csv')
    marathi_words = df['word'].tolist()
except FileNotFoundError:
    marathi_words = []
    print("Error: 'marathi_words.csv' not found.")
except pd.errors.EmptyDataError:
    marathi_words = []
    print("Error: 'marathi_words.csv' is empty.")
except Exception as e:
    marathi_words = []
    print(f"An error occurred while reading 'marathi_words.csv': {e}")


def generate_suggestions(input_text):
    transliterated_input = transliterate(input_text, sanscript.ITRANS, sanscript.DEVANAGARI)

    # Generate variations of the input_text
    variations = [input_text]
    if 'a' in input_text:
        variations.append(input_text.replace('a', 'aa'))
    if 'M' in input_text:
        variations.append(input_text.replace('M', 'm'))
    if 'am' in input_text:
        variations.append(input_text.replace('am', 'aM'))

    # Generate suggestions for all variations
    suggestions = set()
    for var in variations:
        transliterated_var = transliterate(var, sanscript.ITRANS, sanscript.DEVANAGARI)
        for word in marathi_words:
            if word.startswith(transliterated_var):
                suggestions.add(word)

    return list(suggestions)[:10]


@app.route('/transliterate', methods=['POST'])
def transliterate_text():
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    marathi_text = transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI)
    return jsonify({'marathi_text': marathi_text})


@app.route('/suggestions', methods=['POST'])
def get_suggestions():
    data = request.json
    text = data.get('text', '')
    if not text:
        return jsonify({'error': 'No text provided'}), 400
    suggestions = generate_suggestions(text)
    marathi_text = transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI)
    if marathi_text not in suggestions:
        suggestions.append(marathi_text)
    return jsonify({'top_suggestion': suggestions[0] if suggestions else marathi_text, 'suggestions': suggestions})


if __name__ == '__main__':
    app.run(debug=True)
