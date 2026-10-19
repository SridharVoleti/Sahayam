"""Four-wheel geometric model. All dimensions are provisional."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Chassis:
    wheelbase_m: float = 0.65
    track_m: float = 0.50
    wheel_radius_m: float = 0.10

    def __post_init__(self):
        if min(self.wheelbase_m, self.track_m, self.wheel_radius_m) <= 0:
            raise ValueError("Chassis dimensions must be positive")

    @property
    def wheels(self):
        half_wb, half_track = self.wheelbase_m / 2, self.track_m / 2
        return {"front_left": (half_wb, half_track),
                "front_right": (half_wb, -half_track),
                "rear_left": (-half_wb, half_track),
                "rear_right": (-half_wb, -half_track)}
