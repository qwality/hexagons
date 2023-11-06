import json

from dataclasses import dataclass

@dataclass
class Metadata:
    name  : str
    width : int
    height: int

with open('metadata.json', 'r') as f:
    data = json.load(f)

    metadata = Metadata(
        name   = data['name'],
        width  = data['size']['width'],
        height = data['size']['height']
        )