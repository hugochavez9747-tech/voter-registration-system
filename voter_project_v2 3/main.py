"""
Voter Registration & Polling Place Lookup
Author : Hugo
Created : 8/2/2026
Course : CIS189
IDE : VS Code
Description :
This program registers voters, validates their information, and looks
up the polling place assigned to their district. This file is the
console driver program.
I attest that this is my original work.
I have not used unauthorized source code, either modified or
unmodified.
"""

from voter import Voter, AbsenteeVoter, InvalidVoterDataError
from registry import VoterRegistry, DuplicateVoterError
from polling_places import list_districts, all_polling_places

DATA_FILE = "data/voters.txt"


def prompt_nonempty(label):
    while True:
        value = input(f"{label}: ").strip()
        if value:
            return value
        print("  This field cannot be empty. Please try again.")


def prompt_district():
    valid = list_districts()
    while True:
        district = input(f"District ({'/'.join(valid)}): ").strip()
        if district in valid:
            return district
        print(f"  Invalid district. Choose from: {', '.join(valid)}")


def prompt_yes_no(label):
    while True:
        answer = input(f"{label} (y/n): ").strip().lower()
        if answer in ("y", "n"):
            return answer == "y"
        print("  Please answer y or n.")


def register_voter_flow(registry):
    print("\n-- Register a New Voter --")
    name = prompt_nonempty("Full name")
    address = prompt_nonempty("Home address")
    district = prompt_district()
    is_absentee = prompt_yes_no("Register as absentee voter")

    try:
        if is_absentee:
            mailing = prompt_nonempty("Mailing address for ballot")
            voter = AbsenteeVoter(name, address, district, mailing)
        else:
            voter = Voter(name, address, district)
        registry.register_voter(voter)
        registry.save()
        print(f"Registered: {voter.summary()}")
    except InvalidVoterDataError as e:
        print(f"Registration failed - invalid data: {e}")
    except DuplicateVoterError as e:
        print(f"Registration failed - {e}")
    except OSError as e:
        print(f"Registered in memory, but saving to file failed: {e}")


def lookup_flow(registry):
    print("\n-- Look Up a Voter --")
    name = prompt_nonempty("Full name to look up")
    voter = registry.find_voter(name)
    if voter is None:
        print(f"No voter found matching '{name}'.")
        return
    print(voter.summary())
    place = registry.polling_place_for(name)
    print(f"Polling place / ballot info: {place}")


def list_polling_places_flow():
    print("\n-- Polling Places by District --")
    for line in all_polling_places():
        print(" ", line)


def stats_flow(registry):
    print("\n-- Registration Statistics --")
    counts = registry.count_by_district()
    if not counts:
        print("  No voters registered yet.")
        return
    for district in sorted(counts):
        print(f"  District {district}: {counts[district]} voter(s)")
    print(f"  Total registered: {len(registry)}")


def print_menu():
    print("\n===== Voter Registration & Polling Place Lookup =====")
    print("1. Register a new voter")
    print("2. Look up a voter's polling place")
    print("3. List all polling places")
    print("4. View registration statistics")
    print("5. Exit")


def main():
    registry = VoterRegistry(DATA_FILE)
    print(f"Loaded {len(registry)} existing voter(s) from {DATA_FILE}.")

    while True:
        print_menu()
        choice = input("Choose an option (1-5): ").strip()

        if choice == "1":
            register_voter_flow(registry)
        elif choice == "2":
            lookup_flow(registry)
        elif choice == "3":
            list_polling_places_flow()
        elif choice == "4":
            stats_flow(registry)
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1-5.")


if __name__ == "__main__":
    main()
