import json
from PIL import Image
import gui_builder, text
from pathlib import Path
DIR = Path(__file__).resolve().parent

Text = str

class BaseCard():
    def __init__(self, card_info: dict):
        self.name = card_info["name"]
        self.image = Image.new("RGBA", tuple(card_info["dimensions"]))
        self.size = self.image.size
        self.width = self.image.width
        self.height = self.image.height
        self.paste: function = self.image.paste
        base, _ = gui_builder.create_base_gui(*card_info["dimensions"], card_info["base"])
        self.image.paste(im = base, box = base)
        self.fields = {}
        self.field_sizes = {}

        for field in card_info["fields"]:
            offset = (0, 0)
            if "frame" in field:
                base, offset = gui_builder.create_base_gui(*field["dimensions"], field["frame"])

                self.image.paste(base, tuple(field["position"]), base)
            field["position"] = [x + y for x, y in zip(field["position"], offset)]
            self.fields[field["name"]] = field["position"]
            self.field_sizes[field["name"]] = field["dimensions"]

    def set_field(self, name: str, field: Image.Image | Text, padding: tuple[int, int] = None, color: tuple[int, int, int] = None) -> bool:
        """
        Sets a card field to be an image or text.
        The color and padding fields will only affect text.
        Returns True on success, and False if the field is not found.
        """

        if name not in self.fields: 
            return False
        if isinstance(field, str):
            field = text.minecraft(field, padding, color)
        self.paste(field, tuple(self.fields[name]), field)
        return True
    
class Card(BaseCard):
    def __init__(self, card_info):
        super().__init__(card_info)

with open(f"{DIR}/test_card.json", "r") as file:
    test_card_info = json.load(file)

im = BaseCard(test_card_info)
im.set_field("title", "MissingNo.", (0, 1), (34, 51, 255))
# with Image.open(f"{DIR}/gui/missingno.png") as img:
#     img = img.resize(tuple(im.field_sizes["image"]), resample = Image.BOX)
#     im.set_field("image", img)
im.image = im.image.resize((8*im.image.width, 8*im.image.height), resample = Image.BOX)
im.image.save(f"{DIR}/gui.png")
im.image.show()