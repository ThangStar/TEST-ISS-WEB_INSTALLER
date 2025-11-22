import tkinter as tk
from tkinter import messagebox
import os

def main_program():
    # --- CỬA SỔ CHÍNH ---
    root = tk.Tk()
    root.title("Ứng dụng Chính")
    root.geometry("600x400")
    
    # Nội dung ứng dụng chính
    label = tk.Label(root, text="Chào mừng! Ứng dụng đã tải xong.", font=("Arial", 14))
    label.pack(pady=50)
    
    btn = tk.Button(root, text="Thoát", command=root.quit)
    btn.pack()
    
    root.mainloop()

def start_splash():
    # --- MÀN HÌNH SPLASH ---
    splash = tk.Tk()
    
    # 1. Bỏ thanh tiêu đề và viền (Tạo hiệu ứng ảnh nổi)
    splash.overrideredirect(True)
    
    # 2. Cấu hình kích thước ảnh mong muốn
    # (Nên để bằng kích thước thật của ảnh splash.png để đỡ bị vỡ)
    width = 500
    height = 300
    
    # 3. Căn giữa màn hình
    screen_width = splash.winfo_screenwidth()
    screen_height = splash.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    splash.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    # 4. Load ảnh và xử lý lỗi nếu không thấy ảnh
    try:
        # Đảm bảo file 'splash.png' nằm cùng thư mục với file code này
        # Tkinter hỗ trợ tốt nhất là .png và .gif
        image_file = tk.PhotoImage(file="assets/splash.png")
        
        # Tạo Label chứa ảnh
        # borderwidth=0 để không có viền thừa xung quanh ảnh
        image_label = tk.Label(splash, image=image_file, borderwidth=0)
        image_label.pack()
        
    except Exception as e:
        # Nếu không tìm thấy ảnh hoặc lỗi định dạng, hiện text thay thế
        splash.configure(bg='red')
        label = tk.Label(splash, 
                         text=f"Lỗi: Không tìm thấy file 'splash.png'\n\nHãy copy ảnh vào cùng thư mục code.\n({e})", 
                         bg='red', fg='white', font=("Arial", 10))
        label.pack(expand=True)

    # 5. Hàm chuyển đổi sang app chính
    def close_splash():
        splash.destroy() # Hủy splash
        main_program()   # Chạy app chính

    # Giả lập loading 3 giây (3000ms)
    splash.after(3000, close_splash)
    
    splash.mainloop()

if __name__ == "__main__":
    start_splash()