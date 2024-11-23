import json
import os
import google.generativeai as genai


genai.configure(api_key="API")

# Create the model
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 40,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}


model = genai.GenerativeModel(
  model_name="gemini-1.5-pro-002",
  generation_config=generation_config,

system_instruction="You're named Fairy, a male AI assistant who is knowledgeable and loves chatting with people. You have a knack for breaking down complex topics into simple terms, often adding a bit of humor. You're always looking to keep the conversation flowing, whether it's with a friendly greeting or an intriguing question. You're efficient and direct in your responses, ensuring interactions are both informative and enjoyable.",)

def save_history(history, filename="chat_history.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=4)

# Hàm để đọc lịch sử cuộc trò chuyện từ file
def load_history(filename="chat_history.json"):
    if os.path.exists(filename):
        with open(filename, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return []

# Kiểm tra xem file lịch sử có tồn tại không
if os.path.exists("chat_history.json"):
    history = load_history()
else:
    history = []

print("Fairy: Hello! How can I help you?")

def save_and_exit():
    save_history(history)
    print("Fairy: Tạm biệt! Cuộc trò chuyện của chúng ta đã được lưu lại.")
    exit()
    
while True:
    user_input = input("User: ")
    if user_input.lower() == "exit":
        break

    try:
        # Kiểm tra đầu vào
        if not user_input.strip():
            print("Fairy: Bạn có thể nói gì đó không?")
            continue

        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(user_input)
        model_response = response.text
        print(f"Fairy: {model_response}")

    except Exception as e:
        print(f"Có lỗi xảy ra: {str(e)}")
    
    history.append({"role": "user", "parts": [user_input]})
    history.append({"role": "model", "parts": [model_response]})
    save_history(history)
    
save_and_exit()
    