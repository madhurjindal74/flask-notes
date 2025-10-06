# Small Flask app to create and delete simple text notes stored in a JSON file.

from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)
NOTES_FILE = 'notes.json'  # JSON file used to persist notes between runs

def load_notes():
    """Load and return the list of notes from NOTES_FILE.
    Returns an empty list if the file does not exist or is empty."""
    if os.path.exists(NOTES_FILE):
        with open(NOTES_FILE, 'r') as f:
            return json.load(f)
    return []

def save_notes(notes):   #it saves notes to a json file
    """Save the provided list of notes to NOTES_FILE in JSON format."""
    with open(NOTES_FILE, 'w') as f:
        json.dump(notes, f)

@app.route('/', methods=['GET', 'POST'])
def index():
    """Display the list of notes and handle creation of a new note.
    - GET: render the index template with current notes
    - POST: read 'note' from form, append to notes, persist, and redirect"""
    notes = load_notes()
    if request.method == 'POST':
        note = request.form['note']
        notes.append(note)
        save_notes(notes)
        return redirect(url_for('index'))
    return render_template('index.html', notes=notes)

@app.route('/delete/<int:note_id>')
def delete(note_id):
    """Delete the note at the given index (note_id) if it exists, then redirect.
    note_id is validated to be within the current list bounds."""
    notes = load_notes()
    if 0 <= note_id < len(notes):
        notes.pop(note_id)
        save_notes(notes)
    return redirect(url_for('index'))

if __name__ == '__main__':
    # Run the app in debug mode for development; disable debug in production.
    app.run(debug=True)
