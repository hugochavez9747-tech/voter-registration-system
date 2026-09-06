"""
Voter Registration & Polling Place Lookup
Author : Hugo
Created : 8/2/2026
Course : CIS189
IDE : VS Code
Description :
This program registers voters, validates their information, and looks
up the polling place assigned to their district. This file defines the
Voter class and the AbsenteeVoter subclass.
I attest that this is my original work.
I have not used unauthorized source code, either modified or
unmodified.
"""

from datetime import datetime


class InvalidVoterDataError(Exception):
    pass


class Voter:
    VALID_DISTRICTS = {"1", "2", "3", "4", "5"}

    def __init__(self, name, address, district):
        self.name = self._validate_name(name)
        self.address = self._validate_address(address)
        self.district = self._validate_district(district)
        self.registered_on = datetime.now()

    @staticmethod
    def _validate_name(name):
        if not name or not name.strip():
            raise InvalidVoterDataError("Name cannot be empty.")
        return name.strip().title()

    @staticmethod
    def _validate_address(address):
        if not address or not address.strip():
            raise InvalidVoterDataError("Address cannot be empty.")
        return address.strip()

    @classmethod
    def _validate_district(cls, district):
        district = str(district).strip()
        if district not in cls.VALID_DISTRICTS:
            raise InvalidVoterDataError(
                f"District must be one of {sorted(cls.VALID_DISTRICTS)}."
            )
        return district

    def summary(self):
        return (f"{self.name} | District {self.district} | {self.address} "
                f"| Registered {self.registered_on.strftime('%Y-%m-%d %H:%M')}")

    def to_record(self):
        return (f"{self.name}|{self.address}|{self.district}|"
                f"{self.registered_on.isoformat()}|voter")

    def __eq__(self, other):
        if not isinstance(other, Voter):
            return NotImplemented
        return (self.name.lower() == other.name.lower()
                and self.address.lower() == other.address.lower())

    def __repr__(self):
        return f"Voter({self.name!r}, District {self.district})"


class AbsenteeVoter(Voter):
    def __init__(self, name, address, district, mailing_address):
        super().__init__(name, address, district)
        self.mailing_address = self._validate_address(mailing_address)

    def summary(self):
        base = super().summary()
        return f"{base} | ABSENTEE -> Ballot mailed to: {self.mailing_address}"

    def to_record(self):
        return (f"{self.name}|{self.address}|{self.district}|"
                f"{self.registered_on.isoformat()}|absentee|{self.mailing_address}")

    def __repr__(self):
        return f"AbsenteeVoter({self.name!r}, District {self.district})"
