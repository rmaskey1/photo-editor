from tkinter import *
import os
from tktooltip import ToolTip
from PIL import Image, ImageFilter, ImageOps, ImageTk, ImageEnhance
import pilgram, pilgram.css
from tkinter import filedialog

display = Tk()
display.title('Photo Editor')
display.geometry("700x700")
display.state('zoomed')
display.filename = filedialog.askopenfilename(initialdir="", filetypes=(("jpg files", "*.jpg"),("png files", "*.png"),
                                                         ("jpeg files", "*.jpeg"),))
filenam, file_extension = os.path.splitext(display.filename)

display.grid_columnconfigure(0,weight=3)
display.grid_columnconfigure(1,weight=30)
display.grid_columnconfigure(2,weight=3)
#display.grid_rowconfigure(0,weight=1)
#display.grid_rowconfigure(1,weight=20)
#display.grid_rowconfigure(2,weight=1)

C = Canvas(display, bg="gray", height=700, width=700)
filename = PhotoImage(file = "background.png")
background_label = Label(display, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

#C.grid(row=1, column=1)

frame = Frame(display, width=100, height=100)
# frame.pack(fill='both')
frame.place(anchor='center')
frame.grid(row=1, column=1)
# frame.config(bg="#959E9D")

inner_frame = Frame(frame, width=700, height=700)
inner_frame.pack(fill='both')
inner_frame.place(anchor='center',relx=0.5,rely=0.5)
inner_frame.grid(row=0, column=1, padx=5, pady=5)
# inner_frame.configure(background="blue")
# frame.grid_rowconfigure(0, weight=1)
# frame.grid_columnconfigure(0, weight=1)
#
# display.grid_rowconfigure(0, weight=1)
# display.grid_columnconfigure(0, weight=1)


title_frame_left = Frame(display, width=100, height=100)
title_frame_left.place(x=250, y=28)
title_label_left = Label(title_frame_left, text="KEWL BOIZZ", font=('Verdana 36 bold'), fg="#CCCCCC").pack()

title_frame_right = Frame(display, width=100, height=100)
title_frame_right.place(x=865, y=27)
title_label_right = Label(title_frame_right, text="PHOTO EDITOR", font=('Verdana',36,'bold'), fg="#CCCCCC").pack()

og_img = Image.open(display.filename)
og_img.thumbnail((display.winfo_screenwidth() * 0.7, display.winfo_screenheight() * 0.7))
img = ImageTk.PhotoImage(og_img)

stack = []
stack.append(og_img)

redo_stack = []


def peek(stack):
    if stack:
        return stack[-1]
    else:
        return None


label = Label(inner_frame, image=img)
label.pack()

og_r = None
og_g = None
og_b = None

final_img = peek(stack)


def openfile():
    global my_image, label, stack, redo_stack, og_img
    display.filename = filedialog.askopenfilename(initialdir="", filetypes=(("jpg files", "*.jpg"),("png files", "*.png"),
                                                         ("jpeg files", "*.jpeg"),))
    og_img = Image.open(display.filename)
    og_img.thumbnail((display.winfo_screenwidth() * 0.7, display.winfo_screenheight() * 0.7))
    img = ImageTk.PhotoImage(og_img)

    stack = []
    stack.append(og_img)

    redo_stack = []
    label.configure(image=img)
    label.image = img

def savefile():
    global stack
    file = filedialog.asksaveasfile(mode='w', filetypes=(("Type ", "*." + file_extension),))
    location = file.name
    if file:
        imga = peek(stack)
        imga.save(location)

def clear():
    global og_img
    stack.append(og_img)
    img = ImageTk.PhotoImage(og_img)
    label.configure(image=img)
    label.image = img

def undo():
    global stack
    if stack or peek(stack) != og_img:
        x = stack.pop()
        redo_stack.append(x)
        if stack:
            currimg = peek(stack)
            img = ImageTk.PhotoImage(currimg)
            label.configure(image=img)
            label.image = img
    else:
        return


def redo():
    global redo_stack
    if redo_stack:
        currimg = redo_stack.pop()
        stack.append(currimg)
        img = ImageTk.PhotoImage(currimg)
        label.configure(image=img)
        label.image = img
    else:
        return None


def changeHue():
    global label, stack, og_r, og_g, og_b
    root = Tk()
    root.title('Change RGB')
    root.geometry("400x225")
    r, g, b = peek(stack).convert('RGB').split()

    og_r = r
    og_g = g
    og_b = b

    def changeRed(var):
        global r, og_r, label
        new_r = og_r.point(lambda i: i * (r_slider.get() / 1000))
        after = Image.merge('RGB', (new_r, g, b))
        r = new_r
        after_img = ImageTk.PhotoImage(after)
        label.configure(image=after_img)
        label.image = after_img

    def changeGreen(var):
        global g, og_g, label
        new_g = og_g.point(lambda i: i * (g_slider.get() / 1000))
        after = Image.merge('RGB', (r, new_g, b))
        g = new_g
        after_img = ImageTk.PhotoImage(after)
        label.configure(image=after_img)
        label.image = after_img

    def changeBlue(var):
        global b, og_b, label
        new_b = og_b.point(lambda i: i * (b_slider.get() / 1000))
        after = Image.merge('RGB', (r, g, new_b))
        b = new_b
        after_img = ImageTk.PhotoImage(after)
        label.configure(image=after_img)
        label.image = after_img

    def closeWindow():
        global final_img
        stack.append(final_img)
        root.destroy()

    r_slider = Scale(root, from_=0, to=1000, orient=HORIZONTAL, command=changeRed)
    r_slider.set(1000)
    r_slider.pack()
    r_label = Label(root, text='Red').pack()

    g_slider = Scale(root, from_=0, to=1000, orient=HORIZONTAL, command=changeGreen)
    g_slider.set(1000)
    g_slider.pack()
    g_label = Label(root, text='Green').pack()

    b_slider = Scale(root, from_=0, to=1000, orient=HORIZONTAL, command=changeBlue)
    b_slider.set(1000)
    b_slider.pack()
    b_label = Label(root, text='Blue').pack()

    root.protocol("WM_DELETE_WINDOW", closeWindow)

    root.mainloop()


def blur_image():
    global stack, final_img
    root = Tk()
    root.title('Blur Amount')
    root.geometry("400x100")
    final_img = peek(stack)

    def blur(var):
        global stack, final_img, label
        after = peek(stack).filter(ImageFilter.GaussianBlur(blur_slider.get() / 10))
        final_img = after
        after_img = ImageTk.PhotoImage(after)
        label.configure(image=after_img)
        label.image = after_img

    def closeWindow():
        global final_img
        stack.append(final_img)
        root.destroy()

    blur_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=blur)
    blur_slider.set(0)
    blur_slider.pack()
    root.protocol("WM_DELETE_WINDOW", closeWindow)
    root.mainloop()


def change_saturation():
    global stack, final_img
    root = Tk()
    root.title('Saturation')
    root.geometry("400x100")
    final_img = peek(stack)

    def saturate(var):
        global stack, final_img, label
        after = ImageEnhance.Color(peek(stack)).enhance(saturation_slider.get() / 50)
        final_img = after
        after_img = ImageTk.PhotoImage(after)
        label.configure(image=after_img)
        label.image = after_img

    def closeWindow():
        global final_img
        stack.append(final_img)
        root.destroy()

    saturation_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=saturate)
    saturation_slider.set(50)
    saturation_slider.pack()
    root.protocol("WM_DELETE_WINDOW", closeWindow)
    root.mainloop()


def change_contrast():
    global stack, final_img
    root = Tk()
    root.title('Contrast')
    # root.iconbitmap('C:\Users\maske\Desktop\filters')
    root.geometry("400x100")
    final_img = None

    def contrast(var):
        global stack, final_img, label
        after = ImageEnhance.Contrast(peek(stack)).enhance(cont_slider.get() / 50)
        final_img = after
        after_img = ImageTk.PhotoImage(after)
        label.configure(image=after_img)
        label.image = after_img

    def closeWindow():
        global final_img
        stack.append(final_img)
        root.destroy()

    cont_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=contrast)
    cont_slider.set(50)
    cont_slider.pack()
    root.protocol("WM_DELETE_WINDOW", closeWindow)
    root.mainloop()


def change_brightness():
    global stack, final_img
    root = Tk()
    root.title('Brightness')
    root.geometry("400x100")
    final_img = None

    def brightness(var):
        global stack, final_img, label
        after = ImageEnhance.Brightness(peek(stack)).enhance(bright_slider.get() / 50)
        final_img = after
        after_img = ImageTk.PhotoImage(after)
        label.configure(image=after_img)
        label.image = after_img

    def closeWindow():
        global final_img
        stack.append(final_img)
        root.destroy()

    bright_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=brightness)
    bright_slider.set(50)
    bright_slider.pack()
    root.protocol("WM_DELETE_WINDOW", closeWindow)
    root.mainloop()


def change_sharpness():
    global stack, final_img
    root = Tk()
    root.title('Sharpness')
    root.geometry("400x100")
    final_img = None

    def sharpness(var):
        global stack, final_img, label
        after = ImageEnhance.Sharpness(peek(stack)).enhance(sharp_slider.get() / 50)
        final_img = after
        after_img = ImageTk.PhotoImage(after)
        label.configure(image=after_img)
        label.image = after_img

    def closeWindow():
        global final_img
        stack.append(final_img)
        root.destroy()

    sharp_slider = Scale(root, from_=0, to=100, orient=HORIZONTAL, command=sharpness)
    sharp_slider.set(50)
    sharp_slider.pack()
    root.protocol("WM_DELETE_WINDOW", closeWindow)
    root.mainloop()


def sepia():
    before = peek(stack).convert('RGB')
    width, height = before.size

    pixels = before.load()
    for h in range(height):
        for w in range(width):
            r, g, b = before.getpixel((w, h))
            final_r = int(0.393 * r + 0.769 * g + 0.189 * b)
            final_g = int(0.349 * r + 0.686 * g + 0.168 * b)
            final_b = int(0.272 * r + 0.534 * g + 0.131 * b)

            if final_r > 255:
                final_r = 255
            if final_g > 255:
                final_g = 255
            if final_b > 255:
                final_b = 255
            pixels[w, h] = (final_r, final_g, final_b)
    img = ImageTk.PhotoImage(before)
    label.configure(image=img)
    label.image = img
    stack.append(before)


def _1977():
    after = pilgram._1977(peek(stack))
    stack.append(after)
    after_img = ImageTk.PhotoImage(after)
    label.configure(image=after_img)
    label.image = after_img


def walden():
    after = pilgram.walden(peek(stack))
    stack.append(after)
    after_img = ImageTk.PhotoImage(after)
    label.configure(image=after_img)
    label.image = after_img


def grayscale():
    after = ImageOps.grayscale(peek(stack))
    stack.append(after)
    after_img = ImageTk.PhotoImage(after)
    label.configure(image=after_img)
    label.image = after_img


def toaster():
    after = pilgram.toaster(peek(stack))
    stack.append(after)
    after_img = ImageTk.PhotoImage(after)
    label.configure(image=after_img)
    label.image = after_img


def brannan():
    after = pilgram.brannan(peek(stack))
    stack.append(after)
    after_img = ImageTk.PhotoImage(after)
    label.configure(image=after_img)
    label.image = after_img


def lofi():
    after = pilgram.lofi(peek(stack))
    stack.append(after)
    after_img = ImageTk.PhotoImage(after)
    label.configure(image=after_img)
    label.image = after_img


def kelvin():
    after = pilgram.kelvin(peek(stack))
    stack.append(after)
    after_img = ImageTk.PhotoImage(after)
    label.configure(image=after_img)
    label.image = after_img


button_top = Frame(display, width=300, height=100)
button_top.grid(row=0, column=1, pady= (20, 0))
# button_top.grid_rowconfigure(1, weight=1)
# button_top.grid_columnconfigure(1, weight=1)
add_image = Button(button_top, text='Import', width=10, height=3, command=openfile)
add_image.pack(side="left")
# add_image.configure(font=('Verdana 18 bold'))
download = Button(button_top, text='Download', width=10, height=3, command=savefile)
download.pack(side="left")
# download.configure(font=('Verdana 18 bold'))

button_frame = Frame(display, width=100, height=400)
button_frame.grid(row=1, column=0, padx= 50)
# button_frame.grid_rowconfigure(1, weight=1)
# button_frame.grid_columnconfigure(1, weight=1)
toolbar_label = Label(button_frame, text="Toolbar", font=('Helvetica 20'), fg="#BBBBBB").pack()
hue_btn_image = PhotoImage(file="hue_icon.png")
# hue_btn_image = hue_btn_image.subsample(10, 10)
hue_btn = Button(button_frame, image=hue_btn_image, width=60, height=62, command=changeHue)
hue_btn.pack(side="top")
ToolTip(hue_btn, "Hue")

blur_btn_image = PhotoImage(file="blur.png")
blur_btn = Button(button_frame, image=blur_btn_image, width=60, height=62, command=blur_image)
blur_btn.pack(side="top")
ToolTip(blur_btn, "Blur")

saturate_btn_image = PhotoImage(file="saturate.png")
saturate_btn = Button(button_frame, image=saturate_btn_image, width=60, height=62, command=change_saturation)
saturate_btn.pack(side="top")
ToolTip(saturate_btn, "Saturate")

contrast_btn_image = PhotoImage(file="contrast.png")
contrast_btn = Button(button_frame, image=contrast_btn_image, width=60, height=62, command=change_contrast)
contrast_btn.pack(side="top")
ToolTip(contrast_btn, "Contrast")

brightness_btn_image = PhotoImage(file="brightness.png")
brightness_btn = Button(button_frame, image=brightness_btn_image, width=60, height=62, command=change_brightness)
brightness_btn.pack(side="top")
ToolTip(brightness_btn, "Brightness")

sharpness_btn_image = PhotoImage(file="sharpness.png")
sharpness_btn = Button(button_frame, image=sharpness_btn_image, width=60, height=62, command=change_sharpness)
sharpness_btn.pack(side="top")
ToolTip(sharpness_btn, "Sharpness")

undo_btn_image = PhotoImage(file="undo.png")
undo_btn = Button(button_frame, image=undo_btn_image, width=60, height=62, command=undo)
undo_btn.pack(side="top")
ToolTip(undo_btn, "Undo")

redo_btn_image = PhotoImage(file="redo.png")
redo_btn = Button(button_frame, image=redo_btn_image, width=60, height=62, command=redo)
redo_btn.pack(side="top")
ToolTip(redo_btn, "Redo")

clear_btn_image = PhotoImage(file="clear.png")
clear_btn = Button(button_frame, image=clear_btn_image, width=60, height=62, command=clear)
clear_btn.pack(side="top")
ToolTip(clear_btn, "Clear")

filter_frame = Frame(display, width=50, height=400)
filter_frame.grid(row=1, column=2, padx= 50, sticky='e')
# filter_frame.grid_rowconfigure(0, weight=1)
# filter_frame.grid_columnconfigure(2, weight=1)


toolbar_label = Label(filter_frame, text="Filters", font=('Helvetica 20'), fg="#BBBBBB").pack()
_1977_btn = Button(filter_frame, text='_1977', width=7, height=3, command=_1977)
_1977_btn.pack(side="top")
_1977_btn.configure(font=('Verdana 18 bold'))

walden_btn = Button(filter_frame, text='Walden', width=7, height=3, command=walden)
walden_btn.pack(side="top")
walden_btn.configure(font=('Verdana 18 bold'))

grayscale_btn = Button(filter_frame, text='Grayscale', width=7, height=3, command=grayscale)
grayscale_btn.pack(side="top")
grayscale_btn.configure(font=('Verdana 18 bold'))

toaster_btn = Button(filter_frame, text='Toaster', width=7, height=3, command=toaster)
toaster_btn.pack(side="top")
toaster_btn.configure(font=('Verdana 18 bold'))

kelvin_btn = Button(filter_frame, text='Kelvin', width=7, height=3, command=kelvin)
kelvin_btn.pack(side="top")
kelvin_btn.configure(font=('Verdana 18 bold'))

lofi_btn = Button(filter_frame, text='Lofi', width=7, height=3, command=lofi)
lofi_btn.pack(side="top")
lofi_btn.configure(font=('Verdana 18 bold'))

brannan_btn = Button(filter_frame, text='Brannan', width=7, height=3, command=brannan)
brannan_btn.pack(side="top")
brannan_btn.configure(font=('Verdana 18 bold'))

sepia_btn = Button(filter_frame, text='Sepia', width=7, height=3, command=sepia)
sepia_btn.pack(side="top")
sepia_btn.configure(font=('Verdana 18 bold'))

display.mainloop()