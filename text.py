import re
from PIL import Image, ImageChops
from pathlib import Path
DIR = Path(__file__).resolve().parent

text_replace = {
    "_":"underscore",
    "/":"slash",
    ".":"period",
    "-":"dash",
    ",":"comma",
    "+":"plus",
    "*":"star",
    ")":"close_paren",
    "(":"open_paren",
    "'":"apostrophe",
    "&":"and",
    "%":"percent",
    "$":"dollar",
    "#":"hashtag",
    "\"":"quote",
    "!":"exclamation",
    "~":"tilde",
    "}":"close_curly",
    "{":"open_curly",
    "`":"backtick",
    "^":"carat",
    "]":"close_square",
    "[":"open_square",
    "\\":"backslash",
    "@":"at",
    "?":"question",
    ">":"greater_than",
    "=":"equal",
    "<":"less_than",
    ";":"semicolon",
    ":":"colon",
    "|":"pipe"
}

def minecraft(text: str, rgb: tuple[int, int, int] = None) -> Image.Image:
    text = list(text)
    text_array = []
    for i in text:

        i= re.sub(r"([a-z])", r"\g<1>2", i)
        for k, v in text_replace.items():
            i = i.replace(k, v)
        text_array.append(i)
    horizontal = 0
    vertical = 10
    space = 0
    text_image = Image.new("RGBA", (1, vertical), (0, 0, 0, 0))
    for i in text_array:
        if i == "\n":
            horizontal = 0
            vertical += 10
            continue
        if i == " ":
            horizontal += 4
            space += 4
            continue
        with Image.open(f"{DIR}/gui/font/{i}.png") as im:
            bbox = im.getbbox()
            im = im.crop((bbox[0], 0, bbox[2], im.height))
            im_width = im.width + text_image.width + 1 + space
            new_text_image = Image.new('RGBA', (im_width, vertical), (0, 0, 0, 0))
            new_text_image.paste(text_image, (0, 0))
            text_image = new_text_image
            text_image.paste(im, (horizontal, vertical-10))
            horizontal += im.width + 1
    bbox = text_image.getbbox()
    text_image = text_image.crop((bbox[0], 0, bbox[2], text_image.height))
    text_image = _tint_rgb(text_image, rgb)
    return text_image

def _tint_rgb(img: Image.Image, rgb: tuple[int, int, int]) -> Image.Image:
    img = img.convert("RGBA")
    r, g, b, a = img.split()
    rgb_img = Image.merge("RGB", (r, g, b))
    tint_layer = Image.new("RGB", rgb_img.size, rgb)
    tinted = ImageChops.multiply(rgb_img, tint_layer)
    return Image.merge("RGBA", (*tinted.split(), a))
# im = minecraft("test", (1, 1), (0, 0, 0))
# im = im.resize((8*im.width, 8*im.height), resample= Image.BOX)
# im.show()