from openai import OpenAI

# ── CONFIG ────────────────────────────────────────────────────────────────────
API_KEY = "keyy"   # paste your xai-... key here
# ─────────────────────────────────────────────────────────────────────────────

client = OpenAI(api_key=API_KEY, base_url="https://api.x.ai/v1")

history = [
    {"role": "system", "content": "You are Grok, a helpful and witty AI assistant."}
]

print("=" * 45)
print("   Grok Chatbot  |  type 'quit' to exit")
print("=" * 45)

while True:
    user_input = input("\nYou: ").strip()

    if not user_input:
        continue
    if user_input.lower() in ("quit", "exit", "bye"):
        print("Grok: Later! 👋")
        break

    history.append({"role": "user", "content": user_input})

    response = client.chat.completions.create(
        model="grok-3",
        messages=history,
    )

    reply = response.choices[0].message.content
    history.append({"role": "assistant", "content": reply})

    print(f"\nGrok: {reply}")
