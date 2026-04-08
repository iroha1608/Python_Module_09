import sys
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = Field(default=True)
    notes: str | None = Field(default=None, max_length=200)


def main() -> None:
    print("Space Station Data Validation")
    print("========================================")
    try:
        ss_valid = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            # last_maintenance=datetime(2026, 4, 8, 0, 0, 0),
            last_maintenance=datetime.now(),
            is_operational=True,
            notes=None
        )
    except ValidationError as e:
        print(f"Unexpected validation error: {e}", file=sys.stderr)
    print("Valid station created:")
    print(f"ID: {ss_valid.station_id}")
    print(f"Name: {ss_valid.name}")
    print(f"Crew: {ss_valid.crew_size} people")
    print(f"Power: {ss_valid.power_level}%")
    print(f"Oxygen: {ss_valid.oxygen_level}%")
    # print(f"Last maintenance: {ss_valid.last_maintenance}")
    print(f"Status: "
          f"{'Operational' if ss_valid.is_operational else 'Nonoperational'}")
    print()
    print("========================================")
    try:
        ss_invalid = SpaceStation(
            station_id="ISS002",
            name="International Space Staton",
            crew_size=150,
            power_level=100.0,
            oxygen_level=0.0,
            last_maintenance=datetime.now(),
            is_operational=True,
            notes=None
        )
        print(ss_invalid)
    except ValidationError as e:
        print("Expected validation error:")
        print(f"{e.errors()[0]['msg']}", file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
