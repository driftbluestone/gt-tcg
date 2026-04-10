import math
from pathlib import Path
from PIL import Image
DIR = Path(__file__).resolve().parent

# input_slots = int(input("Input Slots: "))
# output_slots = int(input("Output Slots: "))
# base gui colors
# border = (0, 0, 0)
# background = (198, 198, 198)
# top_left = (255, 255, 255)
# bottom_right = (85, 85, 85)
def create_base_gui(width: int, height: int, frame: str = "frame") -> Image.Image:
    """Creates an empty GUI"""
    
    with Image.open(f"{DIR}/gui/{frame}/corner_top_left.png") as img:
        frame_width = img.width
        frame_height = img.height
        width -= frame_width * 2
        height -= frame_height * 2
        basegui = Image.new('RGBA', (width + (frame_width * 2), height + (frame_height * 2)))
        basegui.paste(im=img, box=(0, 0))
    with Image.open(f"{DIR}/gui/{frame}/corner_bottom_left.png") as img:
        basegui.paste(im=img, box=(0, height + frame_height))
    with Image.open(f"{DIR}/gui/{frame}/corner_top_right.png") as img:
        basegui.paste(im=img, box=(width + frame_width, 0))
    with Image.open(f"{DIR}/gui/{frame}/corner_bottom_right.png") as img:
        basegui.paste(im=img, box=(width + frame_width, height + frame_width))

    with Image.open(f"{DIR}/gui/{frame}/border_top.png") as img:
        border_top = img.resize((width, img.height))
        basegui.paste(im=border_top, box=(frame_width, 0))
    with Image.open(f"{DIR}/gui/{frame}/border_bottom.png") as img:
        border_bottom = img.resize((width, img.height))
        basegui.paste(im=border_bottom, box=(frame_width, height + frame_height))
    with Image.open(f"{DIR}/gui/{frame}/border_left.png") as img:
        border_left = img.resize((img.width, height))
        basegui.paste(im=border_left, box=(0, frame_height))
    with Image.open(f"{DIR}/gui/{frame}/border_right.png") as img:
        border_right = img.resize((img.width, height))
        basegui.paste(im=border_right, box=(width + frame_width, frame_height))
    with Image.open(f"{DIR}/gui/{frame}/center.png") as img:
        center = img.resize((width, height))
        basegui.paste(im=center, box=(frame_width, frame_height))
    
    return basegui

def add_slots(gui: Image.Image, input_slots: int, output_slots: int) -> Image.Image:
    vertical = 8
    horizontal = 8
    height = max([math.ceil(input_slots / 3), math.ceil(output_slots / 3)])
    gui.__setattr__("input_slots", input_slots)
    gui.__setattr__("output_slots", output_slots)

    with Image.open(f"{DIR}/gui/slot.png") as img:
        for i in range(input_slots):
            i += 1
            gui.paste(im=img, box=(horizontal, vertical))
            horizontal+=18
            if i % 3 == 0:
                horizontal = 8
                vertical += 18
    
    arrow_distance = 54 + 20
    if input_slots < 3:
        arrow_distance = input_slots*18 + 20
    arrow_height = (height * 9) -1
    with Image.open(f"{DIR}/gui/arrow.png") as img:
        img = img.convert("RGBA")
        progress_bar_width = img.width
        gui.paste(im=img, box=(arrow_distance, arrow_height), mask=img)
    
    vertical = 8
    horizontal = arrow_distance + progress_bar_width + 12
    gui.__setattr__("output_slot_distance", horizontal+1)
    with Image.open(f"{DIR}/gui/slot.png") as img:
        for i in range(output_slots):
            i += 1
            gui.paste(im=img, box=(horizontal, vertical))
            horizontal+=18
            if i % 3 == 0:
                horizontal = arrow_distance + progress_bar_width + 12
                vertical += 18
    return gui

def create_gui(input_slots: int, output_slots: int) -> Image.Image:
    with Image.open(f"{DIR}/gui/arrow.png") as img:
        img = img.convert("RGBA")
        progress_bar_width = img.width
    width = progress_bar_width + 32
    height = (max([math.ceil(input_slots / 3), math.ceil(output_slots / 3)])) * 18 + 8
    if input_slots >= 3:
        width += 54
    else:
        width += 18*input_slots
    if output_slots >= 3:
        width += 54
    else:
        width += 18*output_slots

    gui = create_base_gui(width, height, 8)
    gui = add_slots(gui, input_slots, output_slots)
    return gui

#basegui = create_gui(4, 4)
base = create_base_gui(40, 40, "frame")
slot = create_base_gui(24, 24, "slot")
base.paste(slot, box=(8, 8), mask=slot)
base = base.resize((8*base.width, 8*base.height), resample= Image.BOX)

base.show()