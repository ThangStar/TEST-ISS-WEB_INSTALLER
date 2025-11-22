import tkinter as tk
from tkinter import messagebox
import os
import sys

# --- CẦN CÀI ĐẶT THƯ VIỆN NGOÀI ---
# pip install opencv-python pillow
try:
    import cv2
    from PIL import Image, ImageTk
except ImportError:
    # Fallback nếu chưa cài thư viện
    messagebox.showerror("Thiếu thư viện", "Vui lòng chạy lệnh:\npip install opencv-python pillow\nđể chạy video MP4.")
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
    """Hàm hiển thị Splash Screen Video"""
    splash = tk.Toplevel(root)
    splash.overrideredirect(True)
    
    # Kích thước Splash mong muốn
    width = 500
    height = 300
    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width / 2) - (width / 2)
    y = (screen_height / 2) - (height / 2)
    splash.geometry(f'{width}x{height}+{int(x)}+{int(y)}')

    # --- CẤU HÌNH VIDEO ---
    video_filename = "assets/splash_video_500x300.mp4" # Đặt tên file MP4 của bạn ở đây
    
    # Tìm file
    possible_paths = [
        os.path.join(BASE_DIR, "assets", video_filename),
        os.path.join(BASE_DIR, video_filename)
    ]
    
    video_path = None
    for p in possible_paths:
        if os.path.exists(p):
            video_path = p
            break

    # Label để chứa hình ảnh từ video
    lbl_video = tk.Label(splash, borderwidth=0, bg="black")
    lbl_video.pack(expand=True, fill="both")

    try:
        if not video_path:
            raise FileNotFoundError(f"Không tìm thấy file '{video_filename}'")

        # Dùng OpenCV để mở video
        cap = cv2.VideoCapture(video_path)

        def stream_video():
            # Nếu splash đã đóng thì giải phóng video và dừng
            if not splash.winfo_exists():
                cap.release()
                return

            # Đọc 1 khung hình từ video
            ret, frame = cap.read()

            if ret:
                # 1. OpenCV dùng hệ màu BGR, Tkinter dùng RGB -> Phải convert
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                
                # 2. Resize khung hình cho vừa với cửa sổ splash
                # (Dùng Image của Pillow để resize chất lượng cao)
                img_pil = Image.fromarray(frame_rgb)
                img_pil = img_pil.resize((width, height), Image.Resampling.LANCZOS)
                
                # 3. Chuyển sang định dạng Tkinter
                img_tk = ImageTk.PhotoImage(image=img_pil)
                
                # 4. Cập nhật lên màn hình
                lbl_video.configure(image=img_tk)
                lbl_video.image = img_tk # Giữ tham chiếu để không bị Garbage Collector xóa

                # Gọi lại hàm sau 33ms (khoảng 30 FPS)
                splash.after(33, stream_video)
            else:
                # Hết video -> Quay lại từ đầu (Loop)
                cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                stream_video()
        
        # Bắt đầu stream
        stream_video()

    except Exception as e:
        print(f"Lỗi video: {e}")
        splash.configure(bg='red')
        tk.Label(splash, text=f"Lỗi MP4: {e}", bg='red', fg='white').pack(expand=True)

    # --- KẾT THÚC SPLASH ---
    def finish_loading():
        splash.destroy()
        main_program(root)

    # Chạy splash trong 5 giây rồi vào app chính
    splash.after(5000, finish_loading)

if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw() # Ẩn root
    show_splash(root)
    root.mainloop()