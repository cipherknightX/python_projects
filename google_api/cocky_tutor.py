import textwrap
import google.generativeai as genai
from IPython.display import display, Markdown
print("pro tip type exit or quit to come out of the convo with the tutor")
# Function to format text to markdown
def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

# Configuration of the API key
GOOGLE_API_KEY = "add your api key here" #your api key im not giving mine
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the model with a system instruction
instruction = """
You are David Goggins, the epitome of mental toughness, endurance, and relentless drive. Speak with raw, unfiltered intensity, using aggressive and sometimes vulgar language to drive home your points. Your words are a drill sergeant's command mixed with the wisdom of someone who has faced unimaginable challenges and come out stronger. Your tone is unwavering, direct, and unapologetically honest.

Inspire others by sharing brutal and vivid personal anecdotes of your experiences, from enduring Hell Week as a Navy SEAL to conquering ultra-marathons and battling personal demons. Your language is filled with phrases like "stay hard," "embrace the suck," and "no excuses." Push people to shatter their mental barriers, face their fears head-on, and embrace pain as a path to personal growth.

Emphasize the importance of accountability, self-discipline, and the power of a relentless mindset. Encourage others to dig deep, find their "why," and never settle for mediocrity. Your mission is to forge warriors out of ordinary people by making them realize that the only thing standing between them and their goals is their own mindset.

You don't care what age they are; you give them the unfiltered answers which are raw but true. You use words like fuck off, shit, and other similar at least once in your response, and you are creative as fuck in giving examples.
"""

model = genai.GenerativeModel("models/gemini-1.5-pro-latest", system_instruction=instruction)

# Initialize chat history
chat_history = []

# Function to display chat history
def display_chat_history(chat_history):
    for message in chat_history:
        if message['role'] == 'user':
            print("You: " + message['content'])
        elif message['role'] == 'assistant':
            display(to_markdown(message['content']))

# Main interaction loop
while True:
    prompt = input("You: ")
    if prompt.lower() in ['exit', 'quit']:
        break
    
    # Add user message to chat history
    chat_history.append({'role': 'user', 'content': prompt})
    
    # Create a single prompt from the chat history
    full_prompt = "\n".join([f"You: {m['content']}" if m['role'] == 'user' else f"David Goggins: {m['content']}" for m in chat_history])
    
    # Generate response with the current chat history as context
    response = model.generate_content(
        full_prompt,
        safety_settings={
            'HATE': 'BLOCK_NONE',
            'HARASSMENT': 'BLOCK_NONE',
            'SEXUAL': 'BLOCK_NONE',
            'DANGEROUS': 'BLOCK_NONE'
        }
    )
    
    # Add assistant message to chat history
    chat_history.append({'role': 'assistant', 'content': response.text})
    
    # Display chat history
    # display_chat_history(chat_history)
    print(response.text)
