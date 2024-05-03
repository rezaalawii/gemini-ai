import os

from flask import Flask, render_template, request

import vertexai
from vertexai.generative_models import GenerativeModel

import vertexai.preview.generative_models as generative_models

# pylint: disable=C0103
app = Flask(__name__)

def generate(user_input):
    vertexai.init(project="gothic-context-420907", location="us-central1")
    model = GenerativeModel("gemini-1.0-pro-002")
    responses = model.generate_content(
        user_input,
        generation_config=generation_config,
        safety_settings=safety_settings,
        stream=True,
    )
    generated_text = ""
    for response in responses:
        generated_text += response.text

    return generated_text

generation_config = {
    "max_output_tokens": 2048,
    "temperature": 1,
    "top_p": 1,
}

safety_settings = {
    generative_models.HarmCategory.HARM_CATEGORY_HATE_SPEECH: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    generative_models.HarmCategory.HARM_CATEGORY_HARASSMENT: generative_models.HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
}

@app.route('/', methods=['GET', 'POST'])
def chat():
    if request.method == 'POST':
        user_input = request.form.get("user_input")
        generated_text = generate(user_input)
        return render_template('chat.html', generated_text=generated_text)
    else:
        return render_template('chat.html')

@app.route('/hello')
def hello():
    """Return a friendly HTTP greeting."""
    message = "It's running!"

    """Get Cloud Run environment variables."""
    service = os.environ.get('K_SERVICE', 'Unknown service')
    revision = os.environ.get('K_REVISION', 'Unknown revision')

    return render_template('index.html',
        message=message,
        Service=service,
        Revision=revision)

if __name__ == '__main__':
    server_port = os.environ.get('PORT', '8080')
    app.run(debug=False, port=int(server_port), host='0.0.0.0')
