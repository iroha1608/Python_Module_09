import sys
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError, model_validator


class Rank(str, Enum):
    CADET = "Cadet"
    OFFICER = "Officer"
    LIEUTENANT = "Lieutenant"
    CAPTAIN = "Captain"
    COMMANDER = "Commander"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=2, max_length=50)
    rank: Rank
    age: int = Field(ge=18, le=80)
    specialization: str = Field(min_length=3, max_length=30)
    year_experience: int = Field(ge=0, le=50)
    is_active: bool = Field(default=True)


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15)
    mission_name: str = Field(min_length=3, max_length=100)
    destination: str = Field(min_length=3, max_length=50)
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650)
    crew: list[CrewMember] = Field(min_length=1, max_length=12)
    mission_status: str = Field(default="plannned")
    budget_millions: float = Field(ge=1.0, le=10000.0)

    @model_validator(mode="after")
    def check_budget(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission_id must start with 'M'")
        high_ranker = [
            c
            for c
            in self.crew if c.rank in [Rank.COMMANDER, Rank.CAPTAIN]
        ]
        if not high_ranker:
            raise ValueError(
                "Mission must have at least one Commander or Captain"
            )
        if self.duration_days > 365:
            high_experienced_crew = [
                c
                for c
                in self.crew if c.year_experience > 5
            ]
            if self.crew.__len__() / 2 > high_experienced_crew.__len__():
                raise ValueError(
                    "Long missions (> 365 days) need "
                    "50% experienced crew (5+ years)"
                )
        if [c for c in self.crew if not c.is_active]:
            raise ValueError(
                "Mission must have all active crew members"
            )
        return self


def main() -> None:
    print("Space Mission Crew Validation")
    print("=========================================")

    try:
        mission = SpaceMission(
            mission_id="M2024_MARS",
            mission_name="Mars Colony Establishment",
            destination="Mars",
            launch_date=datetime(2024, 1, 1, 12, 0),
            duration_days=900,
            crew=[
                CrewMember(
                    member_id="M2024_001",
                    name="Sarah Connor",
                    rank=Rank.COMMANDER,
                    age=25,
                    specialization="Mission Command",
                    year_experience=25,
                    is_active=True
                ),
                CrewMember(
                    member_id="M2024_002",
                    name="John Smith",
                    rank=Rank.LIEUTENANT,
                    age=30,
                    specialization="Navigation",
                    year_experience=10,
                    is_active=True
                ),
                CrewMember(
                    member_id="M2024_003",
                    name="Alice Johnson",
                    rank=Rank.OFFICER,
                    age=60,
                    specialization="Engineering",
                    year_experience=50,
                    is_active=True
                ),
            ],
            budget_millions=2500.0
        )
        print("Valid mission created:")
        print(f"Mission: {mission.mission_name}")
        print(f"ID: {mission.mission_id}")
        print(f"Destination: {mission.destination}")
        print(f"Duration: {mission.duration_days} days")
        print(f"Budget: ${mission.budget_millions}M")
        print(f"Crew size: {mission.crew.__len__()}")
        print("Crew members:")
        for c in mission.crew:
            print(f" - {c.name} ({c.rank.value.lower()}) - {c.specialization}")
    except ValidationError as e:
        print(f"Unexpected validation error: {e}", file=sys.stderr)
    print()

    print("=========================================")
    try:
        mission = SpaceMission(
            mission_id="M2024_MOON",
            mission_name="MOON Colony Establishment",
            destination="MOON",
            launch_date=datetime.now(),
            duration_days=3650,
            crew=[
                CrewMember(
                    member_id="M2025_001",
                    name="Bana Banana",
                    rank=Rank.OFFICER,
                    age=20,
                    specialization="Cleaner",
                    year_experience=18,
                    is_active=True
                ),
                CrewMember(
                    member_id="M2025_002",
                    name="Kodakku",
                    rank=Rank.CADET,
                    age=18,
                    specialization="Swimmer",
                    year_experience=5,
                    is_active=True
                ),
                CrewMember(
                    member_id="M2025_003",
                    name="Google Pixel",
                    rank=Rank.LIEUTENANT,
                    age=60,
                    specialization="Gemini AI",
                    year_experience=50,
                    is_active=True
                ),
            ],
            budget_millions=1.0
        )
        print("Valid mission created:")
        print(f"Mission: {mission.mission_name}")
        print(f"ID: {mission.mission_id}")
        print(f"Destination: {mission.destination}")
        print(f"Duration: {mission.duration_days} days")
        print(f"Budget: ${mission.budget_millions}M")
        print(f"Crew size: {mission.crew.__len__()}")
        print("Crew members:")
        for c in mission.crew:
            print(f" - {c.name} ({c.rank.value.lower()}) - {c.specialization}")
    except ValidationError as e:
        print("Expected validation error:")
        print(f"{e.errors()[0]['msg'].split(', ', 1)[1]}", file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
