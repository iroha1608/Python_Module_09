import sys
from enum import Enum
from datetime import datetime
from pydantic import BaseModel, Field, ValidationError, model_validator


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15)
    timestamp: datetime
    locaton: str = Field(min_length=3, max_length=100)
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0)
    duration_minutes: int = Field(ge=1, le=1440)
    witness_count: int = Field(ge=1, le=100)
    message_received: str | None = Field(default=None, max_length=500)
    is_verified: bool = Field(default=False)

    @model_validator(mode="after")
    def validate_rules(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError(
                "Contact ID must start with 'AC'(Alien Contact)"
            )
        if (
            self.contact_type == ContactType.PHYSICAL
            and not self.is_verified
        ):
            raise ValueError(
                "Physical contact must be verified"
            )
        if (
            self.contact_type == ContactType.TELEPATHIC
            and self.witness_count < 3
        ):
            raise ValueError(
                "Telepathic contact requires at least 3 witnesses"
            )
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError(
                "Strong signal (> 7.0) must have a message received"
            )
        return self


def main() -> None:
    print("Alien Contact Log Validation")
    print("========================================")
    try:
        ac_valid = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.now(),
            locaton="Area 51, Nevada",
            contact_type=ContactType.RADIO,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greeting from Zeta Reticuli",
            is_verified=False
        )
        print("Valid contact report:")
        print(f"ID: {ac_valid.contact_id}")
        print(f"Type: {ac_valid.contact_type.value}")
        print(f"Location: {ac_valid.locaton}")
        print(f"Signal: {ac_valid.signal_strength}/10.0")
        print(f"Duration: {ac_valid.duration_minutes} minutes")
        print(f"Witnesses: {ac_valid.witness_count}")
        print(f"Message: '{ac_valid.message_received}'")
    except ValidationError as e:
        print(f"Unexpected validation error: {e}", file=sys.stderr)
    print()

    print("========================================")
    try:
        ac_invalid = AlienContact(
            contact_id="AC_2024_002",
            # contact_id="DC_2024_002",
            timestamp=datetime.now(),
            locaton="Area 51, Nevada",
            contact_type=ContactType.TELEPATHIC,
            # contact_type=ContactType.PHYSICAL,
            # signal_strength=7.1,
            signal_strength=1.0,
            duration_minutes=30,
            # witness_count=3,
            witness_count=1,
            # message_received="testetates",
            message_received="",
            is_verified=False
            # is_verified=True
        )
        print(ac_invalid)
    except ValidationError as e:
        print("Expected validation error:")
        print(f"{e.errors()[0]['msg'].split(', ', 1)[1]}", file=sys.stderr)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
