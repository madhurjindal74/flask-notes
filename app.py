from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
NOTES_FILE = 'notes.json'

def load_notes():
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_notes(notes):
    with open(NOTES_FILE, 'w') as f:
        json.dump(notes, f)

@app.route('/', methods=['GET', 'POST'])
def index():
    notes = load_notes()
    if request.method == 'POST':
        note = request.form['note']
        notes.append(note)
        save_notes(notes)
        return redirect(url_for('index'))
    return render_template('index.html', notes=notes)

@app.route('/delete/<int:note_id>')
def delete(note_id):
    notes = load_notes()
    if 0 <= note_id < len(notes):
        notes.pop(note_id)
        save_notes(notes)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
