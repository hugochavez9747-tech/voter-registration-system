"""
Voter Registration & Polling Place Lookup
Author : Hugo
Created : 8/2/2026
Course : CIS189
IDE : VS Code
Description :
This program registers voters, validates their information, and looks
up the polling place assigned to their district. This file contains
unit tests for the VoterRegistry class.
I attest that this is my original work.
I have not used unauthorized source code, either modified or
unmodified.
"""

import unittest
import os
import sys
import tempfile

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from registry import VoterRegistry, DuplicateVoterError
from voter import Voter, AbsenteeVoter


class TestVoterRegistry(unittest.TestCase):

    def setUp(self):
        self.tmp_dir = tempfile.mkdtemp()
        self.data_file = os.path.join(self.tmp_dir, "voters.txt")
        self.registry = VoterRegistry(self.data_file)

    def tearDown(self):
        if os.path.exists(self.data_file):
            os.remove(self.data_file)
        os.rmdir(self.tmp_dir)

    def test_register_and_count(self):
        v = Voter("Jane Doe", "123 Main St", "1")
        self.registry.register_voter(v)
        self.assertEqual(len(self.registry), 1)

    def test_duplicate_registration_raises(self):
        v1 = Voter("Jane Doe", "123 Main St", "1")
        v2 = Voter("Jane Doe", "123 Main St", "1")
        self.registry.register_voter(v1)
        with self.assertRaises(DuplicateVoterError):
            self.registry.register_voter(v2)

    def test_find_voter_case_insensitive(self):
        v = Voter("Jane Doe", "123 Main St", "1")
        self.registry.register_voter(v)
        found = self.registry.find_voter("jane doe")
        self.assertIsNotNone(found)

    def test_polling_place_for_regular_voter(self):
        v = Voter("Jane Doe", "123 Main St", "1")
        self.registry.register_voter(v)
        place = self.registry.polling_place_for("Jane Doe")
        self.assertIsNotNone(place)
        self.assertNotIn("Absentee", place)

    def test_polling_place_for_absentee_voter(self):
        v = AbsenteeVoter("John Smith", "1 Elm St", "2", "PO Box 5")
        self.registry.register_voter(v)
        place = self.registry.polling_place_for("John Smith")
        self.assertIn("PO Box 5", place)

    def test_save_and_reload_roundtrip(self):
        v = Voter("Jane Doe", "123 Main St", "1")
        self.registry.register_voter(v)
        self.registry.save()

        reloaded = VoterRegistry(self.data_file)
        self.assertEqual(len(reloaded), 1)
        self.assertIsNotNone(reloaded.find_voter("Jane Doe"))

    def test_count_by_district(self):
        self.registry.register_voter(Voter("A A", "1 St", "1"))
        self.registry.register_voter(Voter("B B", "2 St", "1"))
        self.registry.register_voter(Voter("C C", "3 St", "2"))
        counts = self.registry.count_by_district()
        self.assertEqual(counts["1"], 2)
        self.assertEqual(counts["2"], 1)

    def test_malformed_line_is_skipped_without_crashing(self):
        with open(self.data_file, "w", encoding="utf-8") as f:
            f.write("Jane Doe|123 Main St|1|2026-08-02T10:00:00|voter\n")
            f.write("this is not a valid record\n")
            f.write("Bad Name|123 Main St|99|2026-08-02T10:00:00|voter\n")
            f.write("\n")

        reloaded = VoterRegistry(self.data_file)

        self.assertEqual(len(reloaded), 1)
        self.assertIsNotNone(reloaded.find_voter("Jane Doe"))
        self.assertIsNone(reloaded.find_voter("Bad Name"))


if __name__ == "__main__":
    unittest.main()
