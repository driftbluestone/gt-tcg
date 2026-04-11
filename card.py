import json
from PIL import Image
import gui_builder, text_generator
from pathlib import Path
DIR = Path(__file__).resolve().parent

class Card():
    def __init__(self, card_info: dict):
        self.name = card_info["name"]
        self.image = Image.new("RGBA", tuple(card_info["dimensions"]))
        base, _ = gui_builder.create_base_gui(*card_info["dimensions"], card_info["base"])
        self.image.paste(im = base, box = base)

        for field in card_info["fields"]:
            field: dict
            base, _ = gui_builder.create_base_gui(*field["dimensions"], field["frame"])
            self.image.paste(base, tuple(field["position"]), base)

        for field in card_info["text_fields"]:
            field: dict
            if "background" in field:
                background, border_size = gui_builder.create_base_gui(*field["background"]["dimensions"], field["background"]["frame"])
                self.image.paste(background, tuple(field["position"]), background)
                field["position"] = [x + y for x, y in zip(field["position"], border_size)]
            text = text_generator.generate_text(field["text"], tuple(field["color"]))
            self.image.paste(text, tuple(field["position"]), text)
with open(f"{DIR}/test_card.json", "r") as file:
    test_card_info = json.load(file)

im = Card(test_card_info)
im.image = im.image.resize((8*im.image.width, 8*im.image.height), resample= Image.BOX)
im.image.save(f"{DIR}/gui.png")
im.image.show()