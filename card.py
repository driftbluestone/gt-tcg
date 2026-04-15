import json
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
        self.image_field_dimensions = {}

        for field in card_info["fields"]:
            offset = (0, 0)
            if "frame" in field:
                base, offset = gui_builder.create_base_gui(*field["dimensions"], field["frame"])
                self.image_field_dimensions[field["name"]] = field["dimensions"]
                self.image.paste(base, tuple(field["position"]), base)
            field["position"] = [x + y for x, y in zip(field["position"], offset)]
            self.fields[field["name"]] = field["position"]

    def set_field(self, name: str, field: Image.Image | str, *, scale: float = 1, literal_scale: bool = False, padding: tuple[int, int] = (0, 0), color: tuple[int, int, int] = (0, 0, 0), wrapping: bool = True) -> bool:
        """
        Sets a card field to be an image or text.

        Enabling literal scale means that the scale will not be adjusted by the image's scale.

        The color field will only affect text.

        Returns True on success, and False if the field is not found.
        """
        if name not in self.fields: 
            return False
        
        if wrapping:
            width = self.image_field_dimensions[name][0] if name in self.image_field_dimensions else (self.image.width - self.fields[name][0])
            box_width = width - padding[0]
            print(box_width)
            box_width = int(box_width / (self.scale * scale))
            print(box_width)
        else:
            box_width = None
        
        if isinstance(field, str):
            field = text.minecraft(field, color, wrapping, box_width)

        if not literal_scale:
            scale *= im.scale
            padding = [x * 8 for x in padding]
        if scale != 1:
            field = field.resize((int(scale * field.width), int(scale * field.height)), resample = Image.BOX)

        self.image.paste(field, tuple([x + y for x, y in zip(self.fields[name], padding)]), field)
        return True
    
    def resize(self, scale: float):
        """
        Resize the image while keeping field positions consistent
        """
        for k, v in self.fields.items():
            self.fields[k] = [int(x * scale) for x in v]
        for k, v in self.image_field_dimensions.items():
            self.image_field_dimensions[k] = [int(x * scale) for x in v]
        self.image = self.image.resize((int(scale * self.image.width), int(scale * self.image.height)), resample = Image.BOX)
        self.scale *= scale
    
class Card(BaseCard):
    def __init__(self, card_info: dict = None):
        base_card: str = card_info["base"]
        with open(f"{DIR}/cards/base/{base_card}.json", "r") as file:
            base_card: dict = json.load(file)
        super().__init__(base_card)

im = Card({"base":"test_card"})
im.resize(8)
im.set_field("title", "Twink Vista", color=(34, 51, 255))
im.set_field("move_1", "Release Age!")
# im.set_field("move_2", "idk what to write here")
im.set_field("move_description_1", "Can you believe it, guys? AGE! Just a week away. AGE is in a week! Woohoo! I am so happy about this information. AGE, just a week away. Oh, wow. Can you believe it? AGE! Just in a week! It got here so fast. AGE, just a week away!", padding=(4, -5), scale=0.5)
# im.set_field("move_description_2", "age release when\nim waiting!!", padding=(5, -5), scale = 0.5)

im.image.save(f"{DIR}/gui.png")
im.image.show()