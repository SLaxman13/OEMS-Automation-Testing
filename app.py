import time
import random
from flask import Flask, render_template_string, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "oems_secret_key"

STUDENTS = {"student101": {"name": "Laxman S", "password": "pass"}}

QUESTION_BANK = [
    {"id": 1, "type": "MCQ", "question": "Which protocol is used for real-time web proctoring?", "options": ["HTTP/2", "WebRTC", "FTP", "SMTP"]},
    {"id": 2, "type": "MCQ", "question": "Main objective of load testing?", "options": ["Verify styling", "Measure concurrent user handling", "Check spelling"]},
    {"id": 3, "type": "DESCRIPTIVE", "question": "Explain how tab-switch detection improves online exam integrity."}
]

HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>OEMS - Exam Portal</title>
    <style>
        body { font-family: Arial, sans-serif; margin: 30px; }
        .container { max-width: 700px; margin: auto; padding: 20px; border: 1px solid #ccc; border-radius: 8px; }
        .warning { background-color: #f8d7da; color: #721c24; padding: 10px; display: none; margin-bottom: 15px; }
        .badge { background: #e2e3e5; padding: 4px 8px; border-radius: 4px; font-size: 0.8rem; }
    </style>
</head>
<body>
<div class="container">
    {% if not session.get('user') %}
        <h2>OEMS Student Login</h2>
        <form action="/login" method="POST">
            <p>Student ID: <br><input type="text" id="username" name="username" value="student101" required></p>
            <p>Password: <br><input type="password" id="password" name="password" value="pass" required></p>
            <button type="submit" id="login-btn">Login</button>
        </form>
    {% else %}
        <h2>Exam Portal - {{ session['user_name'] }} <span id="save-status" class="badge">Ready</span></h2>
        <div id="timer">Time Remaining: <span id="time-display">10:00</span></div>
        <br>
        <div id="warning-box" class="warning">
            Tab switch detected! Warnings: <span id="warning-count">0</span>/3.
        </div>

        <form id="exam-form">
            {% for q in questions %}
                <div style="margin-bottom: 15px;">
                    <h4>Q{{ loop.index }}: {{ q.question }}</h4>
                    {% if q.type == 'MCQ' %}
                        {% for opt in q.options %}
                            <label style="display:block;">
                                <input type="radio" name="q_{{ q.id }}" value="{{ opt }}" onchange="triggerAutoSave()"> {{ opt }}
                            </label>
                        {% endfor %}
                    {% else %}
                        <textarea name="q_{{ q.id }}" rows="3" style="width:100%;" oninput="triggerAutoSave()"></textarea>
                    {% endif %}
                </div>
            {% endfor %}
        </form>
    {% endif %}
</div>

{% if session.get('user') %}
<script>
    let warnings = 0;
    // Tab Switch Detection
    window.addEventListener('blur', function() {
        warnings++;
        document.getElementById('warning-box').style.display = 'block';
        document.getElementById('warning-count').innerText = warnings;
    });

    // Auto Save
    function triggerAutoSave() {
        document.getElementById('save-status').innerText = 'Saving...';
        setTimeout(() => {
            document.getElementById('save-status').innerText = 'All changes saved';
        }, 1000);
    }
</script>
{% endif %}
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML_TEMPLATE, questions=session.get("questions", []))

@app.route("/login", methods=["POST"])
def login():
    username = request.form.get("username")
    password = request.form.get("password")
    if username in STUDENTS and STUDENTS[username]["password"] == password:
        session["user"] = username
        session["user_name"] = STUDENTS[username]["name"]
        session["questions"] = QUESTION_BANK
        return redirect(url_for("index"))
    return "Invalid", 401

if __name__ == "__main__":
    app.run(port=5000, debug=True)