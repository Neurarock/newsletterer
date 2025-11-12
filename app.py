from flask import Flask, render_template, request, redirect, send_file, Response
from test_driver import main
import queue
import threading
import sys
from io import StringIO

app = Flask(__name__)

news_topic = ""
opinion_piece_prompt = ""
grok_conversation = ""
status = "awaiting completed user inputs"
output_file_path = ""
log_queue = queue.Queue()

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
    print(message)


@app.route("/")
def display_home_page():
    return render_template("index.html")

@app.route("/logs")
def stream_logs():
    """Stream logs via Server-Sent Events"""
    def generate():
        # Send initial connection message
        yield f"data: Connected to log stream\n\n"
        
        while True:
            try:
                message = log_queue.get(timeout=0.5)
                yield f"data: {message}\n\n"
            except queue.Empty:
                # Keep connection alive
                yield f":\n\n"
    
    return Response(generate(), mimetype="text/event-stream", headers={
        "Cache-Control": "no-cache",
        "X-Accel-Buffering": "no"
    })

@app.route("/newsletter")
def display_newsletter():
    if output_file_path:
        return send_file(output_file_path, mimetype='text/html')
    return redirect('/')

@app.route('/submit', methods=['POST'])
def submit_input():
    global news_topic, opinion_piece_prompt, grok_conversation, status, output_file_path
    
    news_topic = request.form.get('news_topic')
    opinion_piece_prompt = request.form.get('opinion_piece_prompt')
    grok_conversation = request.form.get('grok_conversation')
    if news_topic and not opinion_piece_prompt and not grok_conversation:
        add_log("only one field filled in, waiting for complete input")

    if news_topic and opinion_piece_prompt and grok_conversation:
        status = "user input complete, executing newsletterer"
        add_log("=" * 50)
        add_log("Starting newsletter generation...")
        add_log(f"Topic: {news_topic}")
        add_log(f"Opinion Prompt: {opinion_piece_prompt[:50]}...")
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
                return redirect('/newsletter')
        finally:
            sys.stdout = old_stdout
            sys.stderr = old_stderr

    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, port=6060)