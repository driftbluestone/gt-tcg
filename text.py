import re, os, math
from typing import Literal
from PIL import Image, ImageChops
from pathlib import Path
DIR = Path(__file__).resolve().parent

widths: dict[str, int] = {}
chars: dict[str, Image.Image] = {" ": 5}
for file in os.listdir(f"{DIR}/gui/font"):
    with Image.open(f"{DIR}/gui/font/{file}") as text_char:
        bbox = text_char.getbbox()
        text_char = text_char.crop((bbox[0], 0, bbox[2], text_char.height))
        chars[file[:-4]] = text_char.copy()
        widths[file[:-4]] = text_char.width

text_replace = str.maketrans({
    "_":"underscore", "/":"slash", ".":"period",
    "-":"dash", ",":"comma", "+":"plus", "*":"star",
    ")":"close_paren", "(":"open_paren", "'":"apostrophe",
    "&":"and", "%":"percent", "$":"dollar", "#":"hashtag",
    "\"":"quote", "!":"exclamation", "~":"tilde",
    "}":"close_curly", "{":"open_curly", "`":"backtick",
    "^":"carat", "]":"close_square", "[":"open_square",
    "\\":"backslash", "@":"at", "?":"question",
    ">":"greater_than", "=":"equal", "<":"less_than",
    ";":"semicolon", ":":"colon", "|":"pipe"
})

def minecraft(text: str, rgb: tuple[int, int, int] = None, box_width: int = None) -> Image.Image:
    """
    Generate Minecraft text
    """
    
    text_block = render(text, box_width)
    
    if rgb is not None:
        text_block = _tint_rgb(text_block, rgb)
    return text_block

def render(text: str, box_width: int) -> Image.Image:
    text = [[[re.sub(r"([a-z])", r"\g<1>2", character).translate(text_replace) for character in list(word)] for word in letter] for letter in [word.split(" ") for word in text.split("\n")]]

    # calculate image size
    line_widths = []
    for line in text:
        line_widths.append(get_line_width(line))
    if box_width is None:
        box_width = max(line_widths)
        
    text_block = Image.new("RGBA", (box_width, 0), (0, 0, 0, 0))

    for line in text:
        line = render_line(line, box_width)
        new_text_block = Image.new("RGBA", (box_width, text_block.height + line.height), (0, 0, 0, 0))
        new_text_block.paste(text_block, (0, 0), text_block)

        new_text_block.paste(line, (0, text_block.height), line)
        text_block = new_text_block

    return text_block

def render_line(line: list[list[str]], box_width: int) -> Image.Image:

    height = 1
    word_widths = []
    temp_word_widths = []

    for word in line:
        word_width = get_word_width(word)
        word_widths.append(word_width + 5)
        temp_word_widths.append(word_width + 5)
        if sum(temp_word_widths) > box_width:
            height += 1
            tww_len = len(temp_word_widths)
            temp_word_widths = []
            
            if tww_len != 1:
                temp_word_widths.append(word_width + 5)

    line_image = Image.new("RGBA", (box_width, height * 10), (0, 0, 0, 0))

    position_x = 0
    position_y = 0
    for index, word in enumerate(line):
        next_word = render_word(word, word_widths[index])
        if position_x + next_word.width > box_width:
            position_x  =  0
            position_y += 10

        line_image.paste(next_word, (position_x, position_y), next_word)
        position_x += next_word.width
    return line_image

def render_word(word: list[str], width) -> Image.Image:

    word_image = Image.new("RGBA", (width, 10), (0, 0, 0, 0))

    position = 0
    for char in word:
        char = chars[char]
        word_image.paste(char, (position, 0), char)
        position += char.width + 1

    return word_image

def get_word_width(word):
        # get word width
    width = 0
    for char in word:
        width += widths[char] + 1
    width -= 1
    return width

def get_line_width(line: list[list[str]]) -> int:
    width = 0
    for word in line:
        for char in word:
            width += widths[char] + 1
        width += 4
    width -= 5
    return width

def _tint_rgb(img: Image.Image, rgb: tuple[int, int, int]) -> Image.Image:
    if isinstance(rgb, list):
        rgb = tuple(rgb)
    img = img.convert("RGBA")
    r, g, b, a = img.split()
    rgb_img = Image.merge("RGB", (r, g, b))
    tint_layer = Image.new("RGB", rgb_img.size, rgb)
    tinted = ImageChops.multiply(rgb_img, tint_layer)
    return Image.merge("RGBA", (*tinted.split(), a))

minecraft("wowie this is so crazy isnt it i can finally have wrapping in my text!!", (255, 255, 255), 50).show()