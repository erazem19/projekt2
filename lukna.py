import tkinter as tk
from PIL import Image, ImageTk

zoom_factor=1
dots = []
is_dragging = False

def on_mouse_press(event):
    global start_x, start_y, dot_id, dots, x2, y2, rel_x, rel_y, is_dragging
    is_dragging = False
    start_x = event.x
    start_y = event.y
    
def on_mouse_release(event):
    global is_dragging
    if not is_dragging:
        #koordinate slike pa to
        top_latitude = 60
        bottom_latitude = -60

        zoomed_width = img.width * zoom_factor
        zoomed_height = img.height * zoom_factor
        #koordinate slike glede na poz
        img_x, img_y = canvas.coords(image_id)
        #koordinate glede na zoom
        rel_x = (event.x - img_x) / zoom_factor
        rel_y = (event.y - img_y) / zoom_factor


        #real world koordinate
        longitude = (rel_x / img.width) * 360 - 180
        latitude = top_latitude - (rel_y / img.height) * (top_latitude - bottom_latitude)

        print (longitude, latitude)

        # skankuliraj naspornte koordinate
        opp_longitude = longitude + 180
        if opp_longitude > 180:
            opp_longitude -= 360
        opp_latitude = -latitude

        # skankuliraj real world naspoprtne kordinate nazaj v koordinate na sliki
        x2 = ((opp_longitude + 180) / 360) * img.width
        y2 = ((top_latitude - opp_latitude) / (top_latitude - bottom_latitude)) * img.height

        # prekankuliraj v koordinate na sliki glede na zoom pa te stvari
        opp_canvas_x = x2 * zoom_factor + img_x
        opp_canvas_y = y2 * zoom_factor + img_y
        
        #jajca
        dots.append({
            'rel_x': rel_x,
            'rel_y': rel_y,
            'opp_rel_x': x2,
            'opp_rel_y': y2,
            'red_id': None,
            'green_id': None
        })
    nariši_dots()

def on_mouse_drag(event):
    global start_x, start_y, is_dragging
    #izbriši piko če je premik in ne pritis
    is_dragging = True
        

    image_pos = [0, 0]
    
    dx = event.x - start_x
    dy = event.y - start_y
    dx_scale= int(dx * 1)
    dy_scale = int(dy * 1)
    
    # dimenzije 
    x, y = canvas.coords(image_id)
    canvas_width = canvas.winfo_width()
    canvas_height = canvas.winfo_height()
    img_width = img.width
    img_height = img.height

    new_x = x + dx_scale
    new_y = y + dy_scale
    zoomed_img_width = img_width * zoom_factor
    zoomed_img_height = img_height * zoom_factor
    # omeji premik v x smeri
    min_x = canvas_width - zoomed_img_width
    max_x = 0
    new_x = max(min_x, min(new_x, max_x))

    # omeji premik v y smeri
    min_y = canvas_height - zoomed_img_height
    max_y = 0
    new_y = max(min_y, min(new_y, max_y))

    # premakni kurčevo sliko
    canvas.coords(image_id, new_x, new_y)

    # updejt nečesa
    start_x = event.x
    start_y = event.y
    print (f"X: {start_x} Y: {start_y} premik: {dx},{dy}" )
    nariši_dots()

def on_mouse_wheel(event):
    global zoom_factor, photo, image_id
    print (event.delta)
    direction = 1 if event.delta > 0 else -1
    zoom_factor *= 0.15 + direction 



    
    zoom_factor = max(1, min(zoom_factor, 3.0))

    new_width = int(img.width * zoom_factor)
    new_height = int(img.height * zoom_factor)
    resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    photo = ImageTk.PhotoImage(resized)

    canvas.itemconfig(image_id, image=photo)
    nariši_dots()

def nariši_dots():
    global dots
    img_x, img_y = canvas.coords(image_id)

    # Delete existing dots from canvas before drawing new ones
    for dot in dots:
        if dot['red_id']:
            canvas.delete(dot['red_id'])
        if dot['green_id']:
            canvas.delete(dot['green_id'])

    for dot in dots:
        # Calculate canvas coords from image relative coords and zoom
        red_canvas_x = dot['rel_x'] * zoom_factor + img_x
        red_canvas_y = dot['rel_y'] * zoom_factor + img_y
        green_canvas_x = dot['opp_rel_x'] * zoom_factor + img_x
        green_canvas_y = dot['opp_rel_y'] * zoom_factor + img_y

        # Draw red dot
        dot_radius = 4
        dot['red_id'] = canvas.create_oval(
            red_canvas_x - dot_radius, red_canvas_y - dot_radius,
            red_canvas_x + dot_radius, red_canvas_y + dot_radius,
            fill="red", outline=""
        )

        # Draw green dot
        dot_radius = 6
        dot['green_id'] = canvas.create_oval(
            green_canvas_x - dot_radius, green_canvas_y - dot_radius,
            green_canvas_x + dot_radius, green_canvas_y + dot_radius,
            fill="green", outline=""
        )

root = tk.Tk()

# Load image
img = Image.open("map-world.jpg")
photo = ImageTk.PhotoImage(img)

# Create canvas and add image
canvas = tk.Canvas(root, width=img.width, height=img.height)
canvas.pack()
image_id = canvas.create_image(0, 0, anchor="nw", image=photo)

#mouse events
canvas.bind("<ButtonPress-1>", on_mouse_press)
canvas.bind("<B1-Motion>", on_mouse_drag)
canvas.bind("<MouseWheel>", on_mouse_wheel)
canvas.bind("<ButtonRelease-1>", on_mouse_release)

root.mainloop()
