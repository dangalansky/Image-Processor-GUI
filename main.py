from tkinter import *
from tkinter import filedialog, messagebox
import numpy as np
import cv2


# ----------FUNCTIONS-----------#
def open_img():
    filename = filedialog.askopenfilename(initialdir='/', title='Choose A File',
                                          filetypes=(('png files', '*.png'), ('jpg files', '*.jpg')))
    img.set(filename)


def format_img():
    img = img_entry.get()
    img = cv2.imread(f'/{img}')
    return img


def show_image(img):
    while True:
        cv2.imshow("Current Image", img)
        if cv2.waitKey(2) & 0xFF == 27:
            break
    cv2.destroyAllWindows()


# -------- func: Flip Image ----------- #
def flip_img():
    img = format_img()

    if radio_state.get() == 1:
        img = cv2.flip(img, 0)

    elif radio_state.get() == 2:
        img = cv2.flip(img, 1)

    elif radio_state.get() == 3:
        img = cv2.flip(img, -1)

    show_image(img)

    if flip_state.get() == 1:
        save_image("flip", img)


# ---------- func: Resize Image -------------- #
def resize():
    i = resize_list.curselection()
    n = resize_list.get(i)
    img = format_img()
    resized_img = cv2.resize(img, (0, 0), img, n, n)
    show_image(resized_img)

    if resize_state.get() == 1:
        save_image("resize", resized_img)


# ---------- func: Crop ------------- #
def crop():
    upper_left_entry.delete(0, END)
    bottom_right_entry.delete(0, END)
    cv2.namedWindow(winname="Current Image")
    cv2.setMouseCallback("Current Image", draw_rectangle)
    show_image(format_img())


def draw_rectangle(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        x1, y1 = x, y
        upper_left_entry.insert(0, f'{x1},{y1}')
    if event == cv2.EVENT_LBUTTONUP:
        x2, y2 = x, y
        bottom_right_entry.insert(0, f'{x2},{y2}')


def format_crop():
    upper_left_crop = upper_left_entry.get().split(",")
    bottom_right_crop = bottom_right_entry.get().split(",")
    x1 = int(upper_left_crop[0])
    y1 = int(upper_left_crop[1])
    x2 = int(bottom_right_crop[0])
    y2 = int(bottom_right_crop[1])
    return x1, y1, x2, y2


def preview_crop():
    x1, y1, x2, y2 = format_crop()
    img = format_img()
    preview = img[y1:y2, x1:x2]
    show_image(preview)


def save_crop():
    x1, y1, x2, y2 = format_crop()
    img = format_img()
    crop_save = img[y1:y2, x1:x2]
    save_image("crop", crop_save)


# ---------- func: Gamma Adjust ---------- #
def gamma_adjust():
    n = float(gamma_entry.get())
    img = format_img()
    gamma_img = np.power(img, n)
    show_image(gamma_img)


# -------------- func: Save --------- #
def save_image(name, img):
    cv2.imwrite(f'{name}_img_edit.jpg', img)
    messagebox.showinfo(title='Success!', message='Image has been saved!')


# ------------ GUI ------------- #
window = Tk()
window.title('Image Processing Unit')
window.geometry('625x625')

# ------------Background------------- #
canvas = Canvas(height=625, width=625, bg='black', highlightthickness=0)
canvas.place(x=0, y=0)

# -----------File Upload------------- #
img = StringVar(None)
img_entry = Entry(textvariable=img, width=30, highlightthickness=0)
img_entry.insert(0, "Image File:")
img_entry.place(x=80, y=30)
open_img_btn = Button(text='Select File', borderwidth=0, highlightbackground='black',
                      command=open_img).place(x=370, y=28)

# ------------Image Display-------------- #
display_btn = Button(window, text='Display Image', borderwidth=0, highlightbackground='black',
                     command=lambda: show_image(format_img())).place(x=475, y=28)

# -----------Image Flip------------------ #
flip_label = Label(text="Flip Image:", bg="black", fg="white")
flip_label.place(x=100, y=60)
radio_state = IntVar()
hor_flip = Radiobutton(text="Horizontal", value=1, variable=radio_state, bg="black", fg="white")
hor_flip.place(x=100, y=80)
vert_flip = Radiobutton(text="Vertical", value=2, variable=radio_state, bg="black", fg="white")
vert_flip.place(x=100, y=100)
both_flip = Radiobutton(text="Both", value=3, variable=radio_state, bg="black", fg="white")
both_flip.place(x=100, y=120)
flip_state = IntVar()
save_flip = Checkbutton(text="Save Flip?", variable=flip_state, bg="black", fg="white")
save_flip.place(x=160, y=140)
flip_submit = Button(window, text="Flip", borderwidth=0, highlightbackground='black',
                     command=flip_img)
flip_submit.place(x=100, y=140)

# ------------- Image Resize ------------ #
resize_label = Label(text="Resize Image:", bg="black", fg="white")
resize_label.place(x=100, y=170)
resize_list = Listbox(height=5, width=4)
size_x = [.25, .50, .75, 2.0, 4.0]
for item in size_x:
    resize_list.insert(size_x.index(item), item)
resize_list.place(x=100, y=190)
resize_state = IntVar()
save_resize = Checkbutton(text="Save Resize?", variable=resize_state, bg="black", fg="white")
save_resize.place(x=180, y=280)
resize_submit = Button(window, text="Resize", borderwidth=0, highlightbackground='black',
                       command=resize)
resize_submit.place(x=100, y=280)

# -----------Crop----------------- #
set_crop = Button(text="Set Crop Border", borderwidth=0, highlightbackground='black', command=crop)
set_crop.place(x=100, y=350)
upper_left = StringVar(None)
upper_left_label = Label(text="Upper L (x,y)", bg="black", fg="white")
upper_left_label.place(x=257, y=320)
upper_left_entry = Entry(textvariable=upper_left, width=10, highlightthickness=0)
upper_left_entry.place(x=250, y=350)
bottom_right = StringVar(None)
bottom_right_label = Label(text="Lower R (x,y)", bg="black", fg="white")
bottom_right_label.place(x=357, y=320)
bottom_right_entry = Entry(textvariable=bottom_right, width=10, highlightthickness=0)
bottom_right_entry.place(x=350, y=350)
preview_crop = Button(text="Preview Crop", borderwidth=0, highlightbackground='black', command=preview_crop)
preview_crop.place(x=100, y=390)
save_crop_btn = Button(text="Save Crop", borderwidth=0, highlightbackground='black', command=save_crop)
save_crop_btn.place(x=100, y=420)

# ---------- Gamma Correction --------- #
gamma_label = Label(text="Gamma Correction\n(<1 = brighter; >1 = darker)", bg="black", fg="white")
gamma_label.place(x=300, y=60)
gamma = StringVar(None)
gamma_entry = Entry(textvariable=gamma, width=5, highlightthickness=0)
gamma_entry.place(x=350, y=100)
gamma_apply = Button(text="Apply", borderwidth=0, highlightbackground='black', command=gamma_adjust)
gamma_apply.place(x=410, y=98)

# --------Tkinter Window Run---------- #
window.mainloop()
