from tkinter import *
from time import strftime
import serial

# Thiết lập kết nối Serial với Arduino
ser = serial.Serial(port='COM4', baudrate=9600, timeout=0.2)

# Tạo cửa sổ chính
root = Tk()
root.title("ĐIỀU KHIỂN THIẾT BỊ QUA ARDUINO UNO")
root.state('zoomed')  # Maximize cửa sổ
# Màu nền giống Windows 10
tk_color = '#0078D7'
root.configure(bg=tk_color)

# Nhãn thời gian và ngày tháng góc trên trái (nền tkinter, chữ vàng)
label = Label(
    root,
    font=('Digital-7', 20),
    bg=root.cget('bg'),
    fg='yellow'
)
label.pack(anchor='nw', padx=10, pady=(10, 0))
date_label = Label(
    root,
    font=('Helvetica', 14, 'italic'),
    bg=root.cget('bg'),
    fg='yellow'
)
date_label.pack(anchor='nw', padx=10, pady=(0, 10))

# Tiêu đề phần mềm
title_label = Label(
    root,
    text='PHẦN MỀM ĐIỀU KHIỂN THIẾT BỊ QUA ARDUINO',
    font=('Helvetica', 32, 'bold'),
    bg=tk_color,
    fg='purple'
)
title_label.pack(pady=(0, 20))

# Canvas chứa các nút và trạng thái, dời xuống chút
top_offset = 50
canvas_width = 600  # Độ rộng đủ hiển thị trạng thái
canvas_height = 4 * (2 * 50 + 30)
btn_canvas = Canvas(
    root,
    bg=tk_color,
    width=canvas_width,
    height=canvas_height,
    highlightthickness=0
)
btn_canvas.pack(pady=(top_offset, 20))

# Vẽ các nút tròn
def draw_buttons():
    r = 50
    margin = 30
    cmds = [
        ('batloa', 'BẬT LOA'),
        ('tatloa', 'TẮT LOA'),
        ('batquat', 'BẬT QUẠT'),
        ('tatquat', 'TẮT QUẠT')
    ]
    for i, (cmd, text) in enumerate(cmds):
        x_btn = 130
        y_btn = margin + r + i * (2 * r + margin)
        btn_color = 'green' if 'BẬT' in text else 'black'
        btn_canvas.create_oval(
            x_btn - r, y_btn - r,
            x_btn + r, y_btn + r,
            fill=btn_color, outline='black', width=2,
            tags=(cmd,)
        )
        btn_canvas.create_text(
            x_btn, y_btn,
            text=text,
            font=('Helvetica', 10, 'bold'),
            fill='white',
            tags=(cmd,)
        )
        btn_canvas.tag_bind(cmd, '<Button-1>', lambda e, c=cmd: globals()[c]())

# Vẽ text cho trạng thái loa và quạt (không có oval)
def draw_status_labels():
    r = 50
    margin = 30
    # Trạng thái loa
    y0 = margin + r
    y1 = y0 + (2 * r + margin)
    y_mid_loa = (y0 + y1) / 2
    # Trạng thái quạt
    y2 = y_mid_loa + (2 * r + margin)
    y3 = y2 + (2 * r + margin)
    y_mid_quat = (y2 + y3) / 2
    x_status = 500
    global tag_txt_loa, tag_txt_quat
    tag_txt_loa = 'status_loa_txt'
    tag_txt_quat = 'status_quat_txt'
    btn_canvas.create_text(
        x_status, y_mid_loa,
        text='LOA ĐANG TẮT', font=('Helvetica', 18, 'bold'), fill='black',
        tags=(tag_txt_loa,)
    )
    btn_canvas.create_text(
        x_status, y_mid_quat,
        text='QUẠT ĐANG TẮT', font=('Helvetica', 18, 'bold'), fill='black',
        tags=(tag_txt_quat,)
    )

# Vẽ nút và nhãn trạng thái
draw_buttons()
draw_status_labels()

# Nhãn email (màu tím, to hơn)
email_label = Label(
    root,
    text='qbquangbinh@gmail.com',
    font=('Helvetica', 22, 'bold'),
    bg=tk_color,
    fg='purple'
)
email_label.place(x=10, y=10)

# Cập nhật thời gian & ngày tháng
def update_time():
    label.config(text=strftime('%H:%M:%S %p'))
    date_label.config(text=strftime('%A/%d/%m/%Y'))
    label.after(1000, update_time)

# Animation email
def animate_email():
    animate_email.x += 5
    if animate_email.x > root.winfo_width():
        animate_email.x = -email_label.winfo_reqwidth()
    y = root.winfo_height() - 60
    email_label.place(x=animate_email.x, y=y)
    root.after(30, animate_email)
animate_email.x = 0

def phanhoi():
    if ser.in_waiting:
        print(ser.readline().decode().strip())

# Hàm điều khiển Arduino và cập nhật trạng thái
def batloa():
    btn_canvas.itemconfig(tag_txt_loa, fill='yellow', text='LOA ĐANG BẬT')
    if ser.in_waiting == 0:
        ser.write(b'batloa\r')
    root.after(1000, phanhoi)

def tatloa():
    btn_canvas.itemconfig(tag_txt_loa, fill='black', text='LOA ĐANG TẮT')
    if ser.in_waiting == 0:
        ser.write(b'tatloa\r')
    root.after(1000, phanhoi)

def batquat():
    btn_canvas.itemconfig(tag_txt_quat, fill='yellow', text='QUẠT ĐANG BẬT')
    if ser.in_waiting == 0:
        ser.write(b'batquat\r')
    root.after(1000, phanhoi)

def tatquat():
    btn_canvas.itemconfig(tag_txt_quat, fill='black', text='QUẠT ĐANG TẮT')
    if ser.in_waiting == 0:
        ser.write(b'tatquat\r')
    root.after(1000, phanhoi)

root.after(0, update_time)
root.after(0, animate_email)
root.mainloop()
