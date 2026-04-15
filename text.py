import re
from PIL import Image, ImageChops
from pathlib import Path
DIR = Path(__file__).resolve().parent

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

str.maketrans(text_replace)
def minecraft(text: str, rgb: tuple[int, int, int] = None, wrapping: bool = False, box_width: int = None) -> Image.Image:
    if wrapping and (box_width is None):
        raise ValueError("box_width must be provided if wrapping is enabled")
    text = [[[re.sub(r"([a-z])", r"\g<1>2", character).translate(text_replace) for character in list(word)] for word in letter] for letter in [word.split(" ") for word in text.split("\n")]]
    text_block = Image.new("RGBA", (1, 1), (0, 0, 0, 0))
    for line in text:
        line_image = _render_line(line, box_width)
        
        new_text_image = Image.new('RGBA', (max(text_block.width, line_image.width), text_block.height + line_image.height), (0, 0, 0, 0))
        new_text_image.paste(text_block, (0, 0))
        text_block = new_text_image
        text_block.paste(line_image, (0, text_block.height - line_image.height))
    if rgb is not None:
        text_block = _tint_rgb(text_block, rgb)
    return text_block

def _render_line(line, box_width) -> Image.Image:
    text_line = Image.new("RGBA", (1, 10), (0, 0, 0, 0))
    horizontal, vertical = -4, 0
    for index, word in enumerate(line):
        text_word = _render_word(word)
        if (box_width is not None) and (text_word.width > box_width):
            return text_line
        if (box_width is not None) and ((text_word.width + text_line.width) > (box_width - 4)):
            new_line = _render_line(line[index:], box_width)
            new_text_image = Image.new('RGBA', (box_width, new_line.height + text_line.height), (0, 0, 0, 0))
            new_text_image.paste(text_line, (0, 0), text_line)
            text_line = new_text_image
            text_line.paste(new_line, (0, text_line.height - new_line.height), new_line)
            return text_line
        
        horizontal += text_word.width + 4
        new_text_image = Image.new('RGBA', (horizontal, vertical + 10), (0, 0, 0, 0))
        new_text_image.paste(text_line, (0, 0), text_line)
        text_line = new_text_image
        text_line.paste(text_word, (horizontal - text_word.width, vertical), text_word)

    bbox = text_line.getbbox()
    if bbox is not None:
        text_line = text_line.crop((bbox[0], 0, bbox[2], text_line.height))
    return text_line

def _render_word(word: list[str]) -> Image.Image:
    text_image = Image.new("RGBA", (1, 10), (0, 0, 0, 0))
    horizontal = 0
    for letter in word:
        with Image.open(f"{DIR}/gui/font/{letter}.png") as text_char:
            bbox = text_char.getbbox()
            text_char = text_char.crop((bbox[0], 0, bbox[2], text_char.height))
            new_text_image = Image.new('RGBA', (text_char.width + text_image.width + 1, 10), (0, 0, 0, 0))
            new_text_image.paste(text_image, (0, 0))
            text_image = new_text_image
            text_image.paste(text_char, (horizontal, 0))
            horizontal += text_char.width + 1
    bbox = text_image.getbbox()
    if bbox is not None:
        text_image = text_image.crop((bbox[0], 0, bbox[2], text_image.height))
    return text_image

def _tint_rgb(img: Image.Image, rgb: tuple[int, int, int]) -> Image.Image:
    if isinstance(rgb, list):
        rgb = tuple(rgb)
    img = img.convert("RGBA")
    r, g, b, a = img.split()
    rgb_img = Image.merge("RGB", (r, g, b))
    tint_layer = Image.new("RGB", rgb_img.size, rgb)
    tinted = ImageChops.multiply(rgb_img, tint_layer)
    return Image.merge("RGBA", (*tinted.split(), a))
