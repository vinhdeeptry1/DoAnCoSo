import json
import os
import tkinter as tk
from tkinter import messagebox

DATA_FILE = "user_data.json"

# Hàm tiện ích để tải và lưu dữ liệu JSON
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    return {"users": {}}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

def center_window(window, width, height):
    """Đặt cửa sổ ở giữa màn hình."""
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width - width) // 2
    y = (screen_height - height) // 2
    window.geometry(f"{width}x{height}+{x}+{y}")

# Đăng nhập hoặc đăng ký
def login_or_register():
    login_window = tk.Tk()
    login_window.title("Login / Register")
    center_window(login_window, 400, 300)
    login_window.configure(bg="#2c2f33")

    current_user = {}

    def handle_login(event=None):
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Lỗi", "Không được để trống tài khoản/mật khẩu.")
            return

        data = load_data()
        users = data.get("users", {})

        if username in users and users[username]["password"] == password:
            current_user["username"] = username
            login_window.destroy()
        else:
            messagebox.showerror("Lỗi", "Tài khoản/mật khẩu không đúng hoặc không tồn tại.")
            
    def handle_register():
        """Xử lý đăng ký."""
        username = username_entry.get().strip()
        password = password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Lỗi", "Không được để trống tài khoản/mật khẩu.")
            return


        data = load_data()
        users = data.get("users", {})

        if username in users:
            messagebox.showerror("Lỗi", "Tài khoản đã tồn tại.")
        else:
            users[username] = {"password": password, "chat_history": []}
            save_data(data)
            messagebox.showinfo("Thành công", "Đăng ký thành công. Bạn có thể đăng nhập ngay bây giờ.")

    # Giao diện đăng nhập/đăng ký
    tk.Label(login_window, text="Tài khoản:", bg="#2c2f33", fg="#ffffff").pack(pady=10)
    username_entry = tk.Entry(login_window)
    username_entry.pack(pady=10)

    tk.Label(login_window, text="Mật khẩu:", bg="#2c2f33", fg="#ffffff").pack(pady=10)
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack(pady=10)

    # Gắn sự kiện Enter cho cả username_entry và password_entry
    username_entry.bind("<Return>", handle_login)
    password_entry.bind("<Return>", handle_login)

    tk.Button(login_window, text="Đăng nhập", command=handle_login, bg="#5865f2", fg="#ffffff").pack(pady=10)
    tk.Button(login_window, text="Đăng ký", command=handle_register, bg="#5865f2", fg="#ffffff").pack(pady=10)

    login_window.mainloop()
    return current_user
