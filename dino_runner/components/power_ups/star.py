from dino_runner.utils.constants import STAR, STAR_TYPE
from dino_runner.components.power_ups.power_up import PowerUp


class Star(PowerUp):
    def __init__(self):
        self.image = STAR
        self.type = STAR_TYPE
        super().__init__(self.image, self.type)