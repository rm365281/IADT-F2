from dataclasses import dataclass
from vehicle import Vehicle

@dataclass(frozen=True)
class Solution:
    vehicles: list[Vehicle]

    def __str__(self):
        lines = []
        lines.append(f"Number of vehicles: {len(self.vehicles)}")
        for v_idx, vehicle in enumerate(self.vehicles, start=1):
            vehicle_str = str(vehicle).replace("Vehicle", f"Vehicle {v_idx}")
            lines.append(f"  {vehicle_str}")
        return "\n".join(lines)