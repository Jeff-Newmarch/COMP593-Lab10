import poke_api
from tkinter import *
from tkinter import ttk
import os
import ctypes
import image_lib
# Get the path of the script and its parent directory
script_path = os.path.abspath(__file__)
script_dir = os.path.dirname(script_path)
image_cache_dir = os.path.join(script_dir, 'images')

# Make the image cache folder if it does not already exist
if os.path.isdir(image_cache_dir):
    os.makedirs(image_cache_dir)

root= Tk()
root.title("Pokemon Image Viewer")
root.minsize(500, 500)

# Set the window icon
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID('COMP593.PokeImageViewer')
icon_path = os.path.join(script_dir, 'Poke-Ball.ico')
root.iconbitmap(icon_path)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

# Create the frame
frame = ttk.Frame(root)
frame.grid(row=0, column=0, padx=10, pady=10, sticky=NSEW)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)
frame.columnconfigure(0, weight=1)
frame.rowconfigure(0, weight=1)

# Adding image to the frame
image_path = os.path.join(script_dir,'pokemon_ball.png')
img_poke = PhotoImage(file=image_path)
lbl_poke_image = ttk.Label(frame, image=img_poke)
lbl_poke_image.grid(row=0, column=0)

# Add the Pokemon name pull-down list to the frame
pokemon_name_list = poke_api.get_pokemon_names()
cbox_poke_names = ttk.Combobox(frame, values=pokemon_name_list, state='readonly')
cbox_poke_names.set("Select a Pokemon")
cbox_poke_names.grid(row=1, column=0, padx=10, pady=10)

def handle_pokemon_sel(event):
    # Get the name of the selected Pokemon
    pokemon_name = cbox_poke_names.get()
    # Download and save the artwork for the selected Pokemon
    global image_path
    image_path = poke_api.download_pokemon_artwork(pokemon_name, image_cache_dir)
    # Display the Pokemon artwork
    if image_path is not None:
        img_poke['file'] = image_path

cbox_poke_names.bind('<<ComboboxSelected>>', handle_pokemon_sel)


# Set as Desktop button
btn_set_desktop = ttk.Button(frame, text='Set as Desktop Image')
image_lib.set_desktop_background_image(image_path)
btn_set_desktop.grid(row=2, column=0,padx=10, pady=10)
if cbox_poke_names.bind('<<ComboboxSelected>>', handle_pokemon_sel) is True:
    btn_set_desktop.state(['!disabled'])
else:
    btn_set_desktop.state(['disabled'])


root.mainloop()