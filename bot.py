import google.generativeai as genai

genai.configure(api_key="keyyyy")
model = genai.GenerativeModel("gemini-2.5-flash")
chat = model.start_chat()

print("Chatbot ready! Type 'quit' to exit.")
while True:
    user = input("You: ")
    print("Bot:", chat.send_message(user).text)