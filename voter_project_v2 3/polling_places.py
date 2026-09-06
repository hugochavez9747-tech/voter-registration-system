"""
Voter Registration & Polling Place Lookup
Author : Hugo
Created : 8/2/2026
Course : CIS189
IDE : VS Code
Description :
This program registers voters, validates their information, and looks
up the polling place assigned to their district. This file holds the
polling place data and lookup helpers.
I attest that this is my original work.
I have not used unauthorized source code, either modified or
unmodified.
"""

POLLING_PLACES = {
    "1": "Roosevelt High School Gym, 1120 University Ave",
    "2": "Franklin Community Center, 4801 Franklin Ave",
    "3": "Meredith Public Library, 1620 6th Ave",
    "4": "Northside Rec Center, 2225 Euclid Ave",
    "5": "Southside Community Church, 3330 SW 9th St",
}


def get_polling_place(district):
    return POLLING_PLACES.get(str(district))


def list_districts():
    return sorted(POLLING_PLACES.keys())


def all_polling_places():
    lines = []
    for district in list_districts():
        place = get_polling_place(district)
        lines.append(f"District {district} -> {place}")
    return lines
