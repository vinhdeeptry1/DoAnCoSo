import tkinter as tk
from tkinter import ttk
from auth import login_or_register, load_data, save_data
from Fairy import process_message, listen_to_speech, load_history, save_history, detect_language  # Import logic từ AI.py
from queue import Queue
import threading
import speech_recognition as sr
import pyttsx3

def center_window(window, width, height):
    """Đặt cửa sổ ở giữa màn hình."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

def speak_with_pyttsx3(text, lang="vi"):
    """Đọc văn bản bằng pyttsx3 với hỗ trợ ngôn ngữ."""
    try:
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        
        # Chọn giọng dựa trên ngôn ngữ
        if lang == "vi":
            engine.setProperty("voice", voices[1].id)  # Giọng tiếng Việt
        else:
            engine.setProperty("voice", voices[0].id)  # Giọng tiếng Anh

        engine.setProperty('volume', 0.7)
        engine.say(text)
        engine.runAndWait()
    except Exception as e:
        print(f"Lỗi khi sử dụng pyttsx3: {e}")

def run_ui(current_user):
    """Giao diện chính sau khi đăng nhập."""
    root = tk.Tk()
    root.title("Fairy")
    center_window(root, 1600, 900)
    root.configure(bg="#1e1e2e")  # Màu nền tối
    global use_voice
    use_voice = False  # Biến toàn cục để bật/tắt chế độ giọng nói

    # Nạp lịch sử từ file
    data = load_data()
    chat_history = data["users"][current_user["username"]]["chat_history"]

    # Tùy chỉnh style
    style = ttk.Style()
    style.theme_use("default")
    style.configure(
        "TButton",
        font=("Arial", 12, "bold"),
        foreground="#ffffff",
        background="#5865f2",
        padding=10,
        borderwidth=0,
        relief="flat",
    )
    style.map(
        "TButton",
        background=[("active", "#4854d1")],
        foreground=[("active", "#ffffff")],
    )
    style.configure(
        "TEntry",
        font=("Arial", 12),
        foreground="#ffffff",
        fieldbackground="#40414e",
        padding=5,
    )

    def save_chat_history():
        """Lưu lịch sử chat của người dùng."""
        data["users"][current_user["username"]]["chat_history"] = chat_history
        save_data(data)

    def process_and_display_response(user_input, lang="vi"):
        """Xử lý và hiển thị phản hồi của AI."""
        response_queue = Queue()
        process_message(user_input, response_queue, use_voice=use_voice, lang=lang, history=chat_history, ui_mode=True)
        while not response_queue.empty():
            response = response_queue.get()
            add_message("Fairy", response)
            if use_voice:
                speak_with_pyttsx3(response, lang=lang)

    def on_send(event=None):
        """Xử lý gửi tin nhắn từ người dùng."""
        user_input = textbox.get().strip()
        if user_input:
            add_message("User", user_input)
            threading.Thread(target=process_and_display_response, args=(user_input,)).start()
            textbox.delete(0, tk.END)

    def toggle_voice():
        """Bật hoặc tắt chế độ giọng nói và gửi lệnh tương ứng đến AI."""
        global use_voice
        if use_voice:
            # Tắt giọng nói
            use_voice = False
            add_message("User", "tắt giọng nói")  # Gửi lệnh 'tắt giọng nói' đến AI
            threading.Thread(target=process_and_display_response, args=("tắt giọng nói",)).start()
        else:
            # Bật giọng nói
            use_voice = True
            add_message("User", "sử dụng giọng nói")  # Gửi lệnh 'sử dụng giọng nói' đến AI
            threading.Thread(target=process_and_display_response, args=("sử dụng giọng nói",)).start()
            # Kích hoạt chế độ lắng nghe giọng nói
            threading.Thread(target=voice_input_loop, daemon=True).start()


    def voice_input_loop():
        """Lắng nghe giọng nói liên tục khi bật chế độ giọng nói."""
        while use_voice:
            user_input = listen_to_speech()
            if user_input:
                lang = detect_language(user_input)
                add_message("User", user_input)
                threading.Thread(target=process_and_display_response, args=(user_input, lang)).start()

    def add_message(role, message):
        """Thêm tin nhắn vào chat history và hiển thị với giao diện dạng console."""
        chatbox.config(state=tk.NORMAL)
        chatbox.insert(tk.END, f"{role}: {message}\n")
        chatbox.see(tk.END)
        chatbox.config(state=tk.DISABLED)
        save_chat_history()

    def logout():
        """Xử lý đăng xuất và quay lại màn hình đăng nhập."""
        save_chat_history()
        root.destroy()
        new_user = login_or_register()
        if new_user:
            run_ui(new_user)

    # Widget thiết kế
    # Banner
    banner = tk.Frame(root, bg="#282a36", height=60)
    banner.pack(side="top", fill="x")
    banner_label = tk.Label(
        banner,
        text="Fairy",
        bg="#282a36",
        fg="#ffffff",
        font=("Arial", 20, "bold"),
    )
    banner_label.pack(anchor="center")

    # Chatbox
    chat_frame = tk.Frame(root, bg="#1e1e2e")
    chat_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    chatbox = tk.Text(
        chat_frame,
        bg="#444654",
        fg="#ffffff",
        font=("Arial", 12),
        wrap="word",
        state="disabled",
        bd=0,
        highlightthickness=0,
    )
    chatbox.pack(fill="both", expand=True, pady=(0, 10))

    # Ô nhập liệu
    input_frame = tk.Frame(chat_frame, bg="#1e1e2e")
    input_frame.pack(fill="x")

    textbox = ttk.Entry(input_frame, font=("Arial", 12))
    textbox.pack(side="left", fill="x", expand=True, padx=(0, 10))

    textbox.bind("<Return>", on_send)
    send_button = ttk.Button(input_frame, text="Gửi", command=on_send)
    send_button.pack(side="right")

    voice_button = ttk.Button(input_frame, text="Giọng nói", command=toggle_voice)
    voice_button.pack(side="right", padx=(0, 10))

    logout_button = ttk.Button(input_frame, text="Đăng xuất", command=logout)
    logout_button.pack(side="left", padx=(0, 10))

    root.mainloop()


# Main
if __name__ == "__main__":
    current_user = login_or_register()
    if current_user:
        run_ui(current_user)
