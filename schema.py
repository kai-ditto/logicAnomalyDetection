from pydantic import BaseModel
from typing import Optional, Literal, List

class JuiceBottle(BaseModel):
    bottle_color: Literal["yellow","wine","white","unknown"]
    image_label: Literal["cherry", "banana", "orange", "unknown"]
    text_label: Literal["100% juice", "unknown"]
    volume_level: Literal["around_half_neck","full","empty"]
    sticker_count: int = 0
    image_label_position: Literal["top","middle","bottom","missing"]
    text_label_position: Literal["top","middle","bottom","missing"]
    juice_fruit_match: Literal["yes","no","unknown"]

    def decode(obj: dict):
        text = ""
        for key, value in obj.items():
            if value == "unknown" or value == "missing" or value == 0:
                continue
            if key == "bottle_color":
                text += f"{value} colored bottle. "
            elif key == "image_label":
                text += f"Image label shows {value}. "
            elif key == "text_label":
                text += f"Text label indicates {value}. "
            elif key == "volume_level":
                text += f"Volume level is {value.replace('_', ' ')}. "
            elif key == "sticker_count":
                text += f"Number of stickers on the bottle: {value}. "
            elif key == "image_label_position":
                text += f"Image label is located at the {value} of the bottle. "
            elif key == "text_label_position":
                text += f"Text label is located at the {value} of the bottle. "
            elif key == "juice_fruit_match":
                text += f"Juice fruit match status: {value}. "
        return text.strip()