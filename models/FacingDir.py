from dataclasses import dataclass
from models.Vector2 import Vector2

@dataclass
class FacingDir:
    """
    Represents a facing direction in 2D space.
    """
    direction: Vector2  # The direction vector
    facing_for_frames: int =0# Number of frames the player has been facing this direction
    def __post_init__(self, x=0.0, y=0.0):
        self.direction = Vector2(x, y)
        magnitude = self.direction.magnitude()
        if magnitude != 0:
            self.direction = self.direction / magnitude # turn the vector into a unit vector
