import os
import pyttsx3
import google.generativeai as genai
from queue import Queue
import speech_recognition as sr
import json

genai.configure(api_key="***")

# Cấu hình mô hình
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 40,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
    model_name="gemini-1.5-pro",
    generation_config=generation_config,
    system_instruction=(
        "You're named Fairy, a male AI assistant who is knowledgeable and loves chatting with people. "
        "You have a knack for breaking down complex topics into simple terms, often adding a bit of humor."
    ),
)


def speak_with_pyttsx3(text, lang="vi"):
    """Đọc văn bản bằng pyttsx3 với hỗ trợ ngôn ngữ."""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        # Chọn giọng dựa trên ngôn ngữ
        if lang == "vi":
            engine.setProperty("voice", voices[1].id)  # Giọng tiếng Việt
        else:
            engine.setProperty("voice", voices[0].id)  # Giọng tiếng Anh.
        engine.setProperty('volume', 0.7)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Lỗi khi sử dụng pyttsx3: {e}")


def detect_language(text):
    """Phát hiện ngôn ngữ từ văn bản."""
    if all(ord(char) < 128 for char in text):  # Nếu tất cả ký tự là ASCII
        return "en"
    else:
        return "vi"


# Hàm nhận diện giọng nói
def listen_to_speech():
    """Lắng nghe giọng nói của người dùng và chuyển thành văn bản."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        try:
            print("Fairy: Tôi đang lắng nghe bạn...")
            recognizer.adjust_for_ambient_noise(source, duration=1)
            audio = recognizer.listen(source, timeout=5)
            text = recognizer.recognize_google(audio, language="vi-VN")
            print(f"Bạn: {text}")
            return text
        except sr.UnknownValueError:
            print("Fairy: Tôi không hiểu bạn nói gì. Vui lòng thử lại.")
        except sr.RequestError as e:
            print(f"Lỗi với dịch vụ nhận diện giọng nói: {e}")
        except Exception as e:
            print(f"Lỗi khác: {e}")
    return None

def save_history(history, filename="chat_history.json"):
    """Lưu lịch sử cuộc trò chuyện."""
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=4)
    except Exception as e:
        print(f"Lỗi khi lưu lịch sử: {e}")

def load_history(filename="chat_history.json"):
    """Load lịch sử."""
    if os.path.exists(filename):
        try:
            with open(filename, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            print("Lỗi: Tệp lịch sử bị hỏng. Tạo tệp mới.")
    return []  # Trả về lịch sử rỗng nếu tệp không tồn tại hoặc bị lỗi

if os.path.exists("chat_history.json"):
    history = load_history()
else:
    history = []

def process_message(user_input, response_queue, use_voice=False, lang="vi", history=None, ui_mode=True):
    """Xử lí tin nhắn từ người dùng."""
    try:
        if not user_input.strip():
            response_queue.put("Fairy: Bạn có thể nói gì đó không?")
            return
        
        chat_session = model.start_chat(history=history)
        response = chat_session.send_message(user_input)
        model_response = response.text

        # Cập nhật lịch sử
        history.append({"role": "user", "parts": [user_input]})
        history.append({"role": "model", "parts": [model_response]})
        save_history(history)

        # Phát hiện ngôn ngữ và gửi phản hồi
        detected_lang = detect_language(user_input)
        response_queue.put(model_response)

        # Chỉ phát âm thanh nếu không có giao diện UI
        if use_voice and not ui_mode:
            speak_with_pyttsx3(model_response, lang=detected_lang)
    except Exception as e:
        response_queue.put(f"Có lỗi xảy ra: {str(e)}")



if __name__ == "__main__":
    response_queue = Queue()
    history = load_history()

    print("Chào mừng bạn đến với trợ lý Fairy!")
    use_voice = False
    lang = "vi"

    while True:
        if use_voice:
            # Nhận đầu vào từ giọng nói
            user_message = listen_to_speech()
            if user_message is None:  # Không có đầu vào giọng nói
                continue
        else:
            # Nhận đầu vào từ bàn phím
            user_message = input("Bạn: ").strip()

        if user_message.lower() == "thoát":
            print("Kết thúc trò chuyện. Tạm biệt!")
            break
        elif user_message.lower() == "sử dụng giọng nói":
            use_voice = True
            print("Chế độ giọng nói đã được bật.")
            continue
        elif user_message.lower() == "tắt giọng nói":
            use_voice = False
            print("Chế độ giọng nói đã được tắt.")
            continue

        process_message(user_message, response_queue, use_voice, lang, history)
        print(response_queue.get())
