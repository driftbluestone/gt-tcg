import json
from typing import Literal
from PIL import Image
import gui_builder, text
from pathlib import Path
DIR = Path(__file__).resolve().parent

class BaseCard():
    def __init__(self, card_info: dict):
        self.image = Image.new("RGBA", tuple(card_info["dimensions"]))
        base, _ = gui_builder.create_base_gui(*card_info["dimensions"], card_info["base"])
        self.image.paste(im = base, box = base)
        self.scale = 1
        self.fields = {}

        for field in card_info["fields"]:
            offset = (0, 0)
            if "frame" in field:
                base, offset = gui_builder.create_base_gui(*field["dimensions"], field["frame"])
                self.image.paste(base, tuple(field["position"]), base)
            field["position"] = [x + y for x, y in zip(field["position"], offset)]
            self.fields[field["name"]] = field["position"]

    def set_field(self, name: str, field: Image.Image | str, *, scale: int | Literal["consistent"] = 1, padding: tuple[int, int] = None, color: tuple[int, int, int] = None) -> bool:
        """
        Sets a card field to be an image or text.
        Setting scale to "consistent" means that it will always be the same size regardless of image scale
        The color field will only affect text.
        Returns True on success, and False if the field is not found.
        """
        if name not in self.fields: 
            return False
        if isinstance(field, str):
            field = text.minecraft(field, color)
        if scale == "scale":
            scale = self.scale
        if scale != 1:
            field = self.image.resize((scale * field.width, scale * field.height), resample = Image.BOX)
        self.image.paste(field, tuple([x + y for x, y in zip(self.fields[name], padding)]), field)
        return True
    
    def resize(self, scale: int):
        """
        Resize the image while keeping field positions consistent
        """
        for k, v in self.fields.items():
            self.fields[k] = [x * scale for x in v]
        self.image = self.image.resize((scale * self.image.width, scale * self.image.height), resample = Image.BOX)
        self.scale *= scale
    
class Card(BaseCard):
    def __init__(self, card_info: dict = None):
        base_card: str = card_info["base"]
        with open(f"{DIR}/cards/base/{base_card}.json", "r") as file:
            base_card: dict = json.load(file)
        super().__init__(base_card)

im = Card({"base":"test_card"})
im.set_field("title", "MissingNo.", padding=(0, 1), color=(34, 51, 255))
im.set_field("move_1", "Confuse!", padding=(0, 0), color=(0, 0, 0))
im.set_field("move_2", "idk what to write here", padding=(0, 0), color=(0, 0, 0))
im.resize(2)
im.set_field("move_description_1", "dn dn dn\nthis field\nfits 5 lines\nof half scaled text!\nisn't that fun", padding=(5, -5), color=(0, 0, 0))
im.set_field("move_description_2", "age release when\nim waiting!!", padding=(5, -5), color=(0, 0, 0))
im.resize(4)


im.image.save(f"{DIR}/gui.png")
im.image.show()