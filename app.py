from flask import Flask, render_template, request, jsonify
import language_tool_python # HIER IST DIE KORREKTUR

# Flask-App initialisieren
app = Flask(__name__)

# LanguageTool-Prüfer initialisieren (Deutsch)
try:
    tool = language_tool_python.LanguageTool('de-DE') # UND HIER
except Exception as e:
    print(f"Fehler beim Laden von LanguageTool: {e}")
    tool = None

@app.route('/')
def index():
    """Rendert die Hauptseite mit dem Eingabeformular."""
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_text():
    """API-Endpunkt, der den Text prüft und Fehler zurückgibt."""
    if not tool:
        return jsonify({'error': 'Der Prüfdienst ist nicht verfügbar.'}), 500

    if not request.json or 'text' not in request.json:
        return jsonify({'error': 'Kein Text im Anfrage-Body gefunden.'}), 400

    text = request.json['text']

    try:
        matches = tool.check(text)

        errors = []
        for match in matches:
            errors.append({
                'message': match.message,
                'short_message': match.ruleId,
                'offset': match.offset,
                'length': match.errorLength,
                'replacements': match.replacements,
                'context': match.context,
                'rule_type': match.ruleIssueType,
                'url': match.ruleUrl
            })

        return jsonify({'errors': errors})
    except Exception as e:
        print(f"Ein unerwarteter Fehler ist aufgetreten: {e}")
        return jsonify({'error': f'Ein unerwarteter Fehler ist aufgetreten: {e}'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)