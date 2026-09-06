"""
Voter Registration & Polling Place Lookup
Author : Hugo
Created : 8/2/2026
Course : CIS189
IDE : VS Code
Description :
This program registers voters, validates their information, and looks
up the polling place assigned to their district. This file contains
unit tests for the Voter and AbsenteeVoter classes.
I attest that this is my original work.
I have not used unauthorized source code, either modified or
unmodified.
"""

import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from voter import Voter, AbsenteeVoter, InvalidVoterDataError


class TestVoter(unittest.TestCase):

    def test_valid_voter_creation(self):
        v = Voter("jane doe", "123 Main St", "2")
        self.assertEqual(v.name, "Jane Doe")
        self.assertEqual(v.district, "2")

    def test_empty_name_raises(self):
        with self.assertRaises(InvalidVoterDataError):
            Voter("   ", "123 Main St", "2")

    def test_empty_address_raises(self):
        with self.assertRaises(InvalidVoterDataError):
            Voter("Jane Doe", "", "2")

    def test_invalid_district_raises(self):
        with self.assertRaises(InvalidVoterDataError):
            Voter("Jane Doe", "123 Main St", "99")

    def test_equality_by_name_and_address(self):
        v1 = Voter("Jane Doe", "123 Main St", "1")
        v2 = Voter("jane doe", "123 main st", "3")
        self.assertEqual(v1, v2)

    def test_summary_contains_district(self):
        v = Voter("Jane Doe", "123 Main St", "4")
        self.assertIn("District 4", v.summary())

    def test_to_record_format(self):
        v = Voter("Jane Doe", "123 Main St", "1")
        record = v.to_record()
        self.assertEqual(record.split("|")[0], "Jane Doe")
        self.assertEqual(record.split("|")[-1], "voter")


class TestAbsenteeVoter(unittest.TestCase):

    def test_absentee_creation(self):
        v = AbsenteeVoter("John Smith", "1 Elm St", "3", "PO Box 99")
        self.assertEqual(v.mailing_address, "PO Box 99")

    def test_absentee_is_a_voter(self):
        v = AbsenteeVoter("John Smith", "1 Elm St", "3", "PO Box 99")
        self.assertIsInstance(v, Voter)

    def test_absentee_summary_mentions_mailing(self):
        v = AbsenteeVoter("John Smith", "1 Elm St", "3", "PO Box 99")
        self.assertIn("PO Box 99", v.summary())

    def test_absentee_invalid_mailing_raises(self):
        with self.assertRaises(InvalidVoterDataError):
            AbsenteeVoter("John Smith", "1 Elm St", "3", "  ")


if __name__ == "__main__":
    unittest.main()
