import ollama

def generate_response(prompt):
    response = ollama.chat(
        model="deepseek-r1:14b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    return response["message"]["content"]


prompt = "What is the capital of France?"

actual_output = generate_response(prompt)

print("Prompt:")
print(prompt)

print("\nDeepSeek Response:")
print(actual_output)