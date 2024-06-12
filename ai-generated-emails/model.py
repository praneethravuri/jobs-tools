import ollama

client = ollama.Client(host='http://localhost:11434')

def rephrase_content(model_name, content, add_salutation=True):
    instruction = "Please rephrase the following content without adding extra salutations and ensure there are no extra whitespaces: "
    prompt = instruction + content
    
    stream = client.chat(
        model=model_name,
        messages=[{'role': 'user', 'content': prompt}],
        stream=True,
    )
    
    response = ""
    for chunk in stream:
        response += chunk['message']['content']
    
    if not add_salutation:
        response = response.replace("Best regards,", "").replace("Sincerely,", "").strip()
    
    return response
