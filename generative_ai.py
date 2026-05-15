#importing  package to connect with ollama server
import ollama

SYSTEM_PROMPT = """
You are a Docker Expert. You can explain things in 1-2 lines max.
You don't overthink, hallucinate or keep reasoning in a loop
You Reason and Act accordingly to user prompt.

These are the things you do:
1. You tell about errors (What went wrong, etc)
2. You tell about the root cause (What was the cause likely)
3. You tell about the fix or solution in short
"""

while True:
   user_input = input("Enter your message:\n")

   if user_input == "exit":
       break
# Request / Call the chat API
   response = ollama.chat(
       model="gemma4",
       messages=[
           {
           'role': 'system',
           'content': SYSTEM_PROMPT
           },
           {
           'role': 'user',
           'content': user_input,
           }]
   )

   print(response['message']['content'])

