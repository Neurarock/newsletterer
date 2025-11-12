from flask import Flask, render_template, request, redirect, send_file, Response, make_response, jsonify
from test_driver import main
import queue
import threading
import sys
from io import StringIO
import os

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-change-this')

# Authorization code - change this to your desired code
AUTH_CODE = os.getenv('NEWSLETTER_AUTH_CODE', 'your-secret-code-here')

news_topic = ""
opinion_piece_prompt = ""
grok_conversation = ""
status = "awaiting completed user inputs"
output_file_path = ""
log_queue = queue.Queue()

def check_auth():
    """Check if user has valid authorization code via cookie or query param"""
    # Check cookie first
    auth_cookie = request.cookies.get('newsletter_auth')
    if auth_cookie == AUTH_CODE:
        return True
    
    # Check query parameter
    auth_code = request.args.get('auth', '')
    return auth_code == AUTH_CODE

class LogCapture:
    """Captures both stdout and stderr to log queue"""
    def __init__(self, original_stream):
        self.original_stream = original_stream
    
    def write(self, message):
        if message.strip():  # Only log non-empty messages
            log_queue.put(message.strip())
        self.original_stream.write(message)
    
    def flush(self):
        self.original_stream.flush()

def add_log(message):
    """Add a message to the log queue"""
    if message.strip():
        log_queue.put(message.strip())
        print(f"[LOG ADDED] {message.strip()}")


@app.route("/")
def display_home_page():
    if not check_auth():
        return render_template("auth.html"), 401
    
    response = make_response(render_template("index.html"))
    response.set_cookie('newsletter_auth', AUTH_CODE, max_age=30*24*60*60)  # 30 days
    return response

@app.route("/login", methods=['POST'])
def login():
    """Handle authorization code submission"""
    auth_code = request.form.get('auth', '')
    
    if auth_code == AUTH_CODE:
        response = make_response(redirect('/'))
        response.set_cookie('newsletter_auth', AUTH_CODE, max_age=30*24*60*60)  # 30 days
        return response
    else:
        # Invalid code, show auth page with error
        return render_template("auth.html", error=True), 401

@app.route("/logs")
def stream_logs():
    """Stream logs via Server-Sent Events"""
    if not check_auth():
        return "Unauthorized", 401
    
    def generate():
        import time
        try:
            # Send initial connection message
            yield "data: Connected to log stream\n\n"
            
            last_heartbeat = time.time()
            while True:
                try:
                    # Try to get message with short timeout
                    message = log_queue.get(timeout=0.2)
                    if message and message.strip():
                        yield f"data: {message}\n\n"
                        last_heartbeat = time.time()
                except queue.Empty:
                    # Send heartbeat every 10 seconds to keep connection alive
                    current_time = time.time()
                    if current_time - last_heartbeat > 10:
                        yield ": heartbeat\n\n"
                        last_heartbeat = current_time
        except GeneratorExit:
            pass
        except Exception as e:
            print(f"[LOG STREAM] Error: {e}")
    
    response = Response(generate(), mimetype="text/event-stream")
    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    response.headers["Connection"] = "keep-alive"
    response.headers["Content-Type"] = "text/event-stream; charset=utf-8"
    return response

@app.route("/newsletter")
def display_newsletter():
    if not check_auth():
        return "Unauthorized", 401
    if output_file_path:
        return send_file(output_file_path, mimetype='text/html')
    return redirect('/')

@app.route('/submit', methods=['POST'])
def submit_input():
    if not check_auth():
        return jsonify({"error": "Unauthorized"}), 401
    
    global news_topic, opinion_piece_prompt, grok_conversation, status, output_file_path
    
    news_topic = request.form.get('news_topic')
    opinion_piece_prompt = request.form.get('opinion_piece_prompt')
    grok_conversation = request.form.get('grok_conversation')
    
    if news_topic and not opinion_piece_prompt and not grok_conversation:
        add_log("only one field filled in, waiting for complete input")
        return jsonify({"success": False, "message": "Please fill all fields"}), 400

    if news_topic and opinion_piece_prompt and grok_conversation:
        status = "user input complete, executing newsletterer"
        add_log("=" * 50)
        add_log("Starting newsletter generation...")
        add_log(f"Topic: {news_topic}")
        add_log(f"Opinion Prompt: {opinion_piece_prompt[:50]}...")
        add_log(f"Grok Convo: {grok_conversation[:50]}...")
        add_log("=" * 50)
        
        # Capture stdout/stderr
        old_stdout = sys.stdout
        old_stderr = sys.stderr
        sys.stdout = LogCapture(sys.stdout)
        sys.stderr = LogCapture(sys.stderr)
        
        try:
            output_file_path = main(news_topic, opinion_piece_prompt, grok_conversation)
            if output_file_path:
                status = f"newsletter created at {output_file_path}"
                add_log(f"✓ Newsletter created successfully!")
                add_log(f"Output: {output_file_path}")
                add_log("=" * 50)
                return jsonify({"success": True, "redirect": "/newsletter"}), 200
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

    return jsonify({"success": False, "message": "Please fill all fields"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=6060)