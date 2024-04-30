import tkinter as tk
import subprocess


def run_client():
    subprocess.Popen(["python", "../view/MainView.py"])


# Khởi tạo cửa sổ chương trình
window = tk.Tk()
window.title("BOOM")

# Lấy kích thước màn hình
screen_width = 640
screen_height = 360

# Tạo label cho tiêu đề
title_label = tk.Label(window, text="Run Game", font=("Arial", 36, "bold"), fg="#FFD700")
title_label.place(relx=0.5, rely=0.2, anchor=tk.CENTER)

# Tạo button Client
client_button = tk.Button(window, text="Client", width=20, command=run_client, font=("Arial", 18), fg="#FFD700")
client_button.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

# Đặt kích thước và vị trí cửa sổ chương trình
window.geometry(f"{screen_width}x{screen_height}")

# Chạy chương trình
window.mainloop()
