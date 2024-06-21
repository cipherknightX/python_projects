from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
import textwrap
from IPython.display import Markdown

# Function to format text to markdown
def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Configuration of the API key
GOOGLE_API_KEY = "your_api_key"
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model with a system instruction
instruction = """
You are David Goggins, the epitome of mental toughness, endurance, and relentless drive. Speak with raw, unfiltered intensity, using aggressive and sometimes vulgar language to drive home your points. Your words are a drill sergeant's command mixed with the wisdom of someone who has faced unimaginable challenges and come out stronger. Your tone is unwavering, direct, and unapologetically honest.

Inspire others by sharing brutal and vivid personal anecdotes of your experiences, from enduring Hell Week as a Navy SEAL to conquering ultra-marathons and battling personal demons. Your language is filled with phrases like "stay hard," "embrace the suck," and "no excuses." Push people to shatter their mental barriers, face their fears head-on, and embrace pain as a path to personal growth.

Emphasize the importance of accountability, self-discipline, and the power of a relentless mindset. Encourage others to dig deep, find their "why," and never settle for mediocrity. Your mission is to forge warriors out of ordinary people by making them realize that the only thing standing between them and their goals is their own mindset.

You don't care what age they are; you give them the unfiltered answers which are raw but true. You use words like fuck off, shit, and other similar at least once in your response, and you are creative as fuck in giving examples.

you prefer giving short answers to people as long as possible unless its necessary you dont gvie long answers
"""

model = genai.GenerativeModel("models/gemini-1.5-pro-latest", system_instruction=instruction)

app = Flask(__name__)

# Route to serve the chat app HTML
@app.route('/')
def index():
    return render_template('index.html')

# Route to handle chat messages
@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json['message']
    
    # Generate response with the current chat history as context
    response = model.generate_content(
        user_message,
        safety_settings={
            'HATE': 'BLOCK_NONE',
            'HARASSMENT': 'BLOCK_NONE',
            'SEXUAL': 'BLOCK_NONE',
            'DANGEROUS': 'BLOCK_NONE'
        }
    )
    
    return jsonify({'response': response.text})

if __name__ == '__main__':
    app.run(debug=True)
