from dataclasses import dataclass, field

from customer import Customer


@dataclass
class Vehicle:
    itinerary: list[Customer]
    capacity: int = 100
    distance: float = field(default=0.0, compare=False)

    def __str__(self):
        lines = []
        lines.append(f"Vehicle (capacity={self.capacity}, customers={len(self.itinerary)}, distance={round(self.distance, 2)}):")
        if not self.itinerary:
            lines.append("  [empty]")
        else:
            for customer in self.itinerary:
                lines.append(f"{customer}")
        return "\n".join(lines)