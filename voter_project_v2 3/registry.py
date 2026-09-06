"""
Voter Registration & Polling Place Lookup
Author : Hugo
Created : 8/2/2026
Course : CIS189
IDE : VS Code
Description :
This program registers voters, validates their information, and looks
up the polling place assigned to their district. This file defines the
VoterRegistry class, which manages voters and saves/loads them from a
file.
I attest that this is my original work.
I have not used unauthorized source code, either modified or
unmodified.
"""

import os

from voter import Voter, AbsenteeVoter, InvalidVoterDataError
from polling_places import get_polling_place


class DuplicateVoterError(Exception):
    pass


class VoterRegistry:
    def __init__(self, data_file="data/voters.txt"):
        self.data_file = data_file
        self.voters = []
        self.load()

    def register_voter(self, voter):
        if not isinstance(voter, Voter):
            raise InvalidVoterDataError("Only Voter objects can be registered.")
        for existing in self.voters:
            if existing == voter:
                raise DuplicateVoterError(f"{voter.name} is already registered.")
        self.voters.append(voter)
        return voter

    def find_voter(self, name):
        target = name.strip().lower()
        for v in self.voters:
            if v.name.lower() == target:
                return v
        return None

    def polling_place_for(self, name):
        voter = self.find_voter(name)
        if voter is None:
            return None
        if isinstance(voter, AbsenteeVoter):
            return f"Absentee ballot mailed to {voter.mailing_address}"
        return get_polling_place(voter.district)

    def save(self):
        directory = os.path.dirname(self.data_file)
        try:
            if directory:
                os.makedirs(directory, exist_ok=True)
            with open(self.data_file, "w", encoding="utf-8") as f:
                for v in self.voters:
                    f.write(v.to_record() + "\n")
        except OSError as e:
            raise OSError(f"Could not save voter roll: {e}")

    def load(self):
        if not os.path.exists(self.data_file):
            return
        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                for line in f:
                    line = line.strip()
                    if line:
                        self._load_record(line)
        except OSError as e:
            raise OSError(f"Could not load voter roll: {e}")

    def _load_record(self, line):
        parts = line.split("|")
        try:
            if len(parts) == 6 and parts[4] == "absentee":
                name, address, district, _iso_date, _tag, mailing = parts
                v = AbsenteeVoter(name, address, district, mailing)
            elif len(parts) == 5 and parts[4] == "voter":
                name, address, district, _iso_date, _tag = parts
                v = Voter(name, address, district)
            else:
                return
            self.voters.append(v)
        except InvalidVoterDataError:
            pass

    def count_by_district(self):
        counts = {}
        for v in self.voters:
            counts[v.district] = counts.get(v.district, 0) + 1
        return counts

    def __len__(self):
        return len(self.voters)
