import tkinter as tk
from tkinter import messagebox
import os
import sys

# Cần cài đặt Pillow để xử lý resize ảnh GIF
# pip install pillow
try:
    from PIL import Image, ImageTk, ImageSequence
except ImportError:
    messagebox.showerror("Thiếu thư viện", "Vui lòng chạy lệnh:\npip install pillow\nđể xử lý ảnh GIF.")
    sys.exit()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def main_program(root):
    """Hàm hiển thị nội dung chính sau khi Splash kết thúc"""
    root.deiconify() 
    root.title("Ứng dụng Chính")
    root.geometry("600x400")
    
    label = tk.Label(root, text="Chào mừng! Ứng dụng đã khởi động xong.", font=("Arial", 14))
    label.pack(pady=50)
    btn = tk.Button(root, text="Thoát", command=root.quit)
    btn.pack()

def show_splash(root):
    """Hàm hiển thị Splash Screen GIF Trong suốt"""
    splash = tk.Toplevel(root)
    splash.overrideredirect(True) # Bỏ viền cửa sổ
    
    # --- CẤU HÌNH TRONG SUỐT (QUAN TRỌNG) ---
    # Chọn một màu sắc lạ (Chroma Key) để làm màu trong suốt
    # Lưu ý: Tính năng transparentcolor chủ yếu hoạt động tốt trên Windows
    transparent_bg = '#add123' 
    splash.config(bg=transparent_bg)
    
    try:
        # Lệnh này bảo hệ điều hành: "Màu #add123 là vô hình"
        splash.wm_attributes("-transparentcolor", transparent_bg)
        # Giữ splash luôn nổi lên trên các cửa sổ khác
        splash.wm_attributes("-topmost", True)
    except tk.TclError:
        # Fallback cho MacOS/Linux (không hỗ trợ transparentcolor tốt như Windows)
        print("Hệ điều hành không hỗ trợ transparentcolor, bỏ qua.")
        pass

    # Kích thước Splash mong muốn
    width = 500
    height = 380
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    splash.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    # --- CẤU HÌNH GIF ---
    gif_filename = "splash_loading.gif" 
    
    possible_paths = [
        os.path.join(BASE_DIR, "assets", gif_filename),
        os.path.join(BASE_DIR, gif_filename)
    ]
    
    gif_path = None
    for p in possible_paths:
        if os.path.exists(p):
            gif_path = p
            break

    # Label chứa ảnh PHẢI có màu nền trùng với màu trong suốt (transparent_bg)
    lbl_img = tk.Label(splash, borderwidth=0, bg=transparent_bg)
    lbl_img.pack(expand=True, fill="both")

    try:
        if not gif_path:
            raise FileNotFoundError(f"Không tìm thấy file '{gif_filename}' trong thư mục assets.")

        # Mở ảnh bằng Pillow
        pil_image = Image.open(gif_path)
        
        frames = []
        for frame in ImageSequence.Iterator(pil_image):
            # 1. Convert sang RGBA để đảm bảo xử lý kênh Alpha (trong suốt) đúng
            frame = frame.convert("RGBA")
            
            # 2. Resize frame
            frame = frame.resize((width, height), Image.Resampling.LANCZOS)
            
            # 3. Convert sang định dạng Tkinter
            frames.append(ImageTk.PhotoImage(frame))
        
        print(f"Đã tải {len(frames)} frames từ GIF.")

        if frames:
            delay = pil_image.info.get('duration', 100)

            def update_anim(ind):
                if not splash.winfo_exists(): return
                
                frame = frames[ind]
                ind += 1
                if ind == len(frames): ind = 0
                
                lbl_img.configure(image=frame)
                splash.after(delay, update_anim, ind)
            
            splash.after(0, update_anim, 0)

    except Exception as e:
        print(f"Lỗi GIF: {e}")
        # Nếu lỗi, đổi màu nền về đỏ để dễ nhìn thấy thông báo
        splash.config(bg='red') 
        splash.wm_attributes("-transparentcolor", "") # Tắt chế độ trong suốt để hiện chữ lỗi
        tk.Label(splash, text=f"Lỗi tải GIF:\n{e}", bg='red', fg='white').pack(expand=True)

    # --- KẾT THÚC SPLASH ---
    def finish_loading():
        splash.destroy()
        main_program(root)

    splash.after(5000, finish_loading)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw() 
    show_splash(root)
    root.mainloop()