from flask import Flask, request, jsonify
from google.transliteration import transliterate_word
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/transliterate', methods=['GET'])
def transliterate():
    text = request.args.get('text')
    lang_code = request.args.get('lang_code', 'mr')  # Default to Hindi if no language code is provided

    if not text:
        return jsonify({"error": "No text provided"}), 400

    try:
        result = transliterate_word(text, lang_code)
        return jsonify({"suggestions": result}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
