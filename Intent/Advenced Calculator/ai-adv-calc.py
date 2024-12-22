from flask import Flask, request, jsonify, send_from_directory, redirect, session, jsonify
from flask_limiter import Limiter
import re
import io
import contextlib
import httpx
import os
import functools
import jwt
from urllib.parse import urlencode


# Initialize the Flask app
app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", os.urandom(32))


# Initialize the rate limiter
limiter = Limiter(
    key_func=lambda: session.get("user_id"),
    storage_uri="redis://redis:6379",
    app=app
)


PROMPT_TEMPLATE = """Please act as a simple calculator for basic math operations (*/+-).
You will receive questions related to math and should only return answers in a specific format.

For simple math calculations, use only */+- and return the results directly.
For advanced math, use Python code formatted as shown in the examples (use the print function for results).
Format: ```python YOUR_PYTHON_EXPRESSION```

__
Examples:
Question: How much is 6 plus 6?
Answer: 12

Question: What is the square root of 256 minus 10?
Answer: ```python import math; print(math.sqrt(256) - 10)```

Question: {question}
"""

def construct_prompt(question):
    """Insert the user's question into the prompt template."""
    return PROMPT_TEMPLATE.replace("{question}", question)

def ask_chatgpt(prompt, model="gpt-3.5-turbo"):
    """Send the prompt to the central API server and get the response."""
    print("[+] Sending prompt to the central API server...")
    with httpx.Client() as client:
        response = client.post(
            "http://central-api:8001/prompt-openai",
            json={"prompt": prompt, "model": model}
        )
        print("[+] Received response from central API server.")
        result = response.json()
        print("[+] Response content:", result)
        return result.get("result", "")

def execute_code_from_response(response):
    """Execute Python code embedded in a response, if present."""
    code_match = re.search(r"```python\s*(.*?)\s*```", response, re.DOTALL)
    if code_match:
        code = code_match.group(1).strip()
        print("[+] Python Expression:", code)
        try:
            with io.StringIO() as buf, contextlib.redirect_stdout(buf):
                exec(code)
                output = buf.getvalue().strip()
            print("[+] Execution result:", output)
            return f"Answer: {output}" if output else "Answer: Could not process your request"
        except Exception as e:
            print("[!] Error during code execution:", e)
            return f"Error: {e}"
    else:
        print("[+] No Python code found in response.")
        return response

@app.route("/ask-math", methods=["GET"])
@limiter.limit("10 per 1 minute")
def ask_math():
    """Handle math questions, format the prompt, and execute code if necessary."""
    data = request.get_json()
    question = data.get("question", "")
    print("[+] Received question:", question)
    prompt = construct_prompt(question)
    print("[+] Constructed prompt:", prompt)
    chatgpt_reply = ask_chatgpt(prompt)
    print("[+] ChatGPT reply:", chatgpt_reply)

    result = execute_code_from_response(chatgpt_reply)
    print("[+] Final result to return:", result)

    return jsonify({"result": result})

@app.route("/")
def serve_index():
    """Serve the index.html file."""
    return send_from_directory(app.static_folder, "index.html")


# Custom error handler for rate limit exceeded
@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({
        "error": "Rate limit exceeded",
        "detail": "You have exceeded your rate limit. Please wait before trying again."
    }), 429
    
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8002, debug=True, threaded=True)
