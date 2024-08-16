from flask import Flask, request, jsonify, render_template

import requests
import json

app = Flask(__name__)

@app.before_request
def log_start_time():
     print("STARTING...")

@app.get('/')
def dir_root():
     return render_template('index.html')

def test_func():
     return "hello"


@app.route('/prompt', methods=['POST'])
def dir_prompt():
     print("Starting Prompt...")
     gpt_prompt = request.form['input'] # Input from HTML Form

     gpt_messages = []
     gpt_messages.append({"role":"system", "content":"Give me the response to the user input in the voice of a grumpy old northern man"})      
     gpt_messages.append({"role":"user", "content":gpt_prompt})      

     gpt_model = "gpt-3.5-turbo-1106"
     gpt_key = "[KEY]"
     gpt_url = "https://api.openai.com/v1/chat/completions"
     gpt_headers = {"Content-Type":"application/json", "Authorization":"Bearer " + gpt_key}
     gpt_body = {"model":gpt_model, "messages":gpt_messages}
     
     gpt_request = requests.post(gpt_url, json=gpt_body, headers=gpt_headers)
     
     try:
          gpt_response = gpt_request.json()  # Converts JSON to Python dictionary object
          
          if "error" in gpt_response:
               return jsonify({"output": gpt_response['error']['message'], "input": gpt_prompt})

          else:
               return jsonify({"output": gpt_response['choices'][0]['message']['content'], "input": gpt_prompt})

     except ValueError:
          print("Response content is not valid JSON")
          return jsonify({"output": "Failed to Convert to JSON", "input": data})
     
     
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8090)