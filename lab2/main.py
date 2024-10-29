import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk

ONE_THIRD = 1.0 / 3.0
ONE_SIXTH = 1.0 / 6.0
TWO_THIRD = 2.0 / 3.0

def _v(m1, m2, hue):
    hue = hue % 1.0
    if hue < ONE_SIXTH:
        return m1 + (m2 - m1) * hue * 6.0
    if hue < 0.5:
        return m2
    if hue < TWO_THIRD:
        return m1 + (m2 - m1) * (TWO_THIRD - hue) * 6.0
    return m1

def rgb_to_hls(r, g, b):
    maxc = max(r, g, b)
    minc = min(r, g, b)
    sumc = maxc + minc
    rangec = maxc - minc
    l = sumc / 2.0
    if minc == maxc:
        return 0.0, l, 0.0
    if l <= 0.5:
        s = rangec / sumc
    else:
        s = rangec / (2.0 - maxc - minc)
    rc = (maxc - r) / rangec
    gc = (maxc - g) / rangec
    bc = (maxc - b) / rangec
    if r == maxc:
        h = bc - gc
    elif g == maxc:
        h = 2.0 + rc - bc
    else:
        h = 4.0 + gc - rc
    h = (h / 6.0) % 1.0
    return h, l, s

def hls_to_rgb(h, l, s):
    if s == 0.0:
        return l, l, l
    if l <= 0.5:
        m2 = l * (1.0 + s)
    else:
        m2 = l + s - (l * s)
    m1 = 2.0 * l - m2
    return (_v(m1, m2, h + ONE_THIRD), _v(m1, m2, h), _v(m1, m2, h - ONE_THIRD))

def rgb_to_cmyk(r, g, b):
    if (r, g, b) == (0, 0, 0):
        return 0, 0, 0, 1
    c = 1 - r / 255
    m = 1 - g / 255
    y = 1 - b / 255
    k = min(c, m, y)
    c = (c - k) / (1 - k)
    m = (m - k) / (1 - k)
    y = (y - k) / (1 - k)
    return round(c * 100), round(m * 100), round(y * 100), round(k * 100)

def cmyk_to_rgb(c, m, y, k):
    r = 255 * (1 - c / 100) * (1 - k / 100)
    g = 255 * (1 - m / 100) * (1 - k / 100)
    b = 255 * (1 - y / 100) * (1 - k / 100)
    return round(r), round(g), round(b)

def update_entities_from_rgb(event=None):
    try:
        r = int(r_entry.get())
        g = int(g_entry.get())
        b = int(b_entry.get())
    except ValueError:
        r = 0
        g = 0
        b = 0
    update_sliders(r, g, b)

def update_entities_from_cmyk(event=None):
    try:
        c = int(cyan_entry.get())
        m = int(magenta_entry.get())
        y = int(yellow_entry.get())
        k = int(black_entry.get())
    except ValueError:
        c, m, y, k = 0, 0, 0, 0
    r, g, b = cmyk_to_rgb(c, m, y, k)
    update_sliders(r, g, b)

def update_entities_from_hls(event=None):
    try:
        h = int(hue_entry.get())
        l = int(lightness_entry.get())
        s = int(saturation_entry.get())
    except ValueError:
        h, l, s = 0, 0, 0
    r, g, b = [round(x * 255) for x in hls_to_rgb(h / 360, l / 100, s / 100)]
    update_sliders(r, g, b)
    
def update_slider_from_rgb(event=None):
    try:
        r = int(red_slider.get())
        g = int(green_slider.get())
        b = int(blue_slider.get())
    except ValueError:
        r = 0
        g = 0
        b = 0
    update_entries(r, g, b)

def update_slider_from_cmyk(event=None):
    try:
        c = int(cyan_slider.get())
        m = int(magenta_slider.get())
        y = int(yellow_slider.get())
        k = int(black_slider.get())
    except ValueError:
        c, m, y, k = 0, 0, 0, 0
    r, g, b = cmyk_to_rgb(c, m, y, k)
    update_entries(r, g, b)
    

def update_slider_from_hls(event=None):
    try:
        h = int(hue_slider.get())
        l = int(lightness_slider.get())
        s = int(saturation_slider.get())
    except ValueError:
        h, l, s = 0, 0, 0
    r, g, b = [round(x * 255) for x in hls_to_rgb(h / 360, l / 100, s / 100)]
    update_entries(r, g, b)

def update_entries(r, g, b):
    cut_values = lambda v: min(max(0, v), 255)
    r, g, b = map(cut_values, (r, g, b))
    c, m, y, k = rgb_to_cmyk(r, g, b)
    h, l, s = rgb_to_hls(r / 255, g / 255, b / 255)

    def process_entry(entry, val):
        entry.delete(0, tk.END)
        entry.insert(0, val)
    
    process_entry(r_entry, r)
    process_entry(g_entry, g)
    process_entry(b_entry, b)
    
    process_entry(hue_entry, h)
    process_entry(lightness_entry, l)
    process_entry(saturation_entry, s)

    process_entry(cyan_entry, c)
    process_entry(magenta_entry, m)
    process_entry(yellow_entry, y)
    process_entry(black_entry, k)

    color_display.config(bg=f'#{r:02x}{g:02x}{b:02x}')
    
def update_sliders(r, g, b):
    cut_values = lambda v: min(max(0, v), 255)
    r, g, b = map(cut_values, (r, g, b))
    c, m, y, k = rgb_to_cmyk(r, g, b)
    h, l, s = rgb_to_hls(r / 255, g / 255, b / 255)

    red_slider.set(r)
    green_slider.set(g)
    blue_slider.set(b)
    
    hue_slider.set(h)
    lightness_slider.set(l)
    saturation_slider.set(s)
    
    cyan_slider.set(c)
    magenta_slider.set(m)
    yellow_slider.set(y)
    black_slider.set(k)
    
    color_display.config(bg=f'#{r:02x}{g:02x}{b:02x}')
    
    

def update_views(r, g, b):
    cut_values = lambda v: min(max(0, v), 255)
    r, g, b = map(cut_values, (r, g, b))
    c, m, y, k = rgb_to_cmyk(r, g, b)
    h, l, s = rgb_to_hls(r / 255, g / 255, b / 255)

    def process_entry(entry, val):
        entry.delete(0, tk.END)
        entry.insert(0, val)
    
    process_entry(r_entry, r)
    process_entry(g_entry, g)
    process_entry(b_entry, b)
    
    process_entry(hue_entry, h)
    process_entry(lightness_entry, l)
    process_entry(saturation_entry, s)

    process_entry(cyan_entry, c)
    process_entry(magenta_entry, m)
    process_entry(yellow_entry, y)
    process_entry(black_entry, k)

    color_display.config(bg=f'#{r:02x}{g:02x}{b:02x}')
    red_slider.set(r)
    green_slider.set(g)
    blue_slider.set(b)

def choose_color():
    color_code = colorchooser.askcolor(title="Choose color")[0]
    if color_code:
        r, g, b = map(int, color_code)
        update_views(r, g, b)
        


app = tk.Tk()
app.title("Color Converter")

PADX = 5
PADY = 5
WIDTH = 5
RETURN_KEY = "<Return>"

ttk.Label(app, text="RGB").grid(column=0, row=0, padx=PADX, pady=PADY, sticky='w')
color_display = tk.Label(app, text="", bg="white", width=20, height=2)
r_entry = ttk.Entry(app, width=WIDTH)
g_entry = ttk.Entry(app, width=WIDTH)
b_entry = ttk.Entry(app, width=WIDTH)
ttk.Label(app, text="CMYK").grid(column=0, row=3, padx=PADX, pady=PADY, sticky='w')
ttk.Label(app, text="HLS").grid(column=0, row=7, padx=PADX, pady=PADY, sticky='w')

r_entry.grid(column=1, row=0)
red_slider = tk.Scale(app, from_=0, to=255, orient='horizontal', command=lambda _: update_slider_from_rgb())
red_slider.grid(column=2, row=0, sticky='ew')

g_entry.grid(column=1, row=1)
green_slider = tk.Scale(app, from_=0, to=255, orient='horizontal', command=lambda _: update_slider_from_rgb())
green_slider.grid(column=2, row=1, sticky='ew')

b_entry.grid(column=1, row=2)
blue_slider = tk.Scale(app, from_=0, to=255, orient='horizontal', command=lambda _: update_slider_from_rgb())
blue_slider.grid(column=2, row=2, sticky='ew')

cyan_entry = ttk.Entry(app, width=WIDTH)
cyan_entry.grid(column=1, row=3)
cyan_slider = tk.Scale(app, from_=0, to=100, orient='horizontal', command=lambda _: update_slider_from_cmyk())
cyan_slider.grid(column=2, row=3, sticky='ew')

magenta_entry = ttk.Entry(app, width=WIDTH)
magenta_entry.grid(column=1, row=4)
magenta_slider = tk.Scale(app, from_=0, to=100, orient='horizontal', command=lambda _: update_slider_from_cmyk())
magenta_slider.grid(column=2, row=4, sticky='ew')

yellow_entry = ttk.Entry(app, width=WIDTH)
yellow_entry.grid(column=1, row=5)
yellow_slider = tk.Scale(app, from_=0, to=100, orient='horizontal', command=lambda _: update_slider_from_cmyk())
yellow_slider.grid(column=2, row=5, sticky='ew')

black_entry = ttk.Entry(app, width=WIDTH)
black_entry.grid(column=1, row=6)
black_slider = tk.Scale(app, from_=0, to=100, orient='horizontal', command=lambda _: update_slider_from_cmyk())
black_slider.grid(column=2, row=6, sticky='ew')

hue_entry = ttk.Entry(app, width=WIDTH)
hue_entry.grid(column=1, row=7)
hue_slider = tk.Scale(app, from_=0, to=360, orient='horizontal', command=lambda _: update_slider_from_hls())
hue_slider.grid(column=2, row=7, sticky='ew')

lightness_entry = ttk.Entry(app, width=WIDTH)
lightness_entry.grid(column=1, row=8)
lightness_slider = tk.Scale(app, from_=0, to=100, orient='horizontal', command=lambda _: update_slider_from_hls())
lightness_slider.grid(column=2, row=8, sticky='ew')

saturation_entry = ttk.Entry(app, width=WIDTH)
saturation_entry.grid(column=1, row=9)
saturation_slider = tk.Scale(app, from_=0, to=100, orient='horizontal', command=lambda _: update_slider_from_hls())
saturation_slider.grid(column=2, row=9, sticky='ew')

color_display.grid(column=3, row=0, rowspan=10, padx=10, pady=5)

r_entry.bind(RETURN_KEY, update_entities_from_rgb)
g_entry.bind(RETURN_KEY, update_entities_from_rgb)
b_entry.bind(RETURN_KEY, update_entities_from_rgb)

cyan_entry.bind(RETURN_KEY, update_entities_from_cmyk)
magenta_entry.bind(RETURN_KEY, update_entities_from_cmyk)
yellow_entry.bind(RETURN_KEY, update_entities_from_cmyk)
black_entry.bind(RETURN_KEY, update_entities_from_cmyk)

hue_entry.bind(RETURN_KEY, update_entities_from_hls)
lightness_entry.bind(RETURN_KEY, update_entities_from_hls)
saturation_entry.bind(RETURN_KEY, update_entities_from_hls)

update_entries(0, 0, 0)
update_sliders(0, 0, 0)

app.mainloop()