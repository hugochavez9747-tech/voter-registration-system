# Voter Registration & Polling Place Lookup System

A Python console application that registers voters, validates their information, and matches each voter to their assigned polling place based on district.

## Features & Highlights

- **Object-Oriented Architecture**: Utilizes a class hierarchy (`Voter` → `AbsenteeVoter`) leveraging inheritance and polymorphism to handle distinct voter types.
- **Custom Exception Handling**: Prevents invalid data entries and duplicate voter registrations.
- **Data Persistence**: Uses file I/O to save and load the voter roll across sessions.
- **Comprehensive Unit Testing**: Includes an 18-test suite using `unittest` covering validation, equality checks, and save/load round-trips.
- **Interactive Console Interface**: Robust input validation with re-prompting user flows.

## Project Structure

```text
voter-registration-system/
├── voter.py           # Voter and AbsenteeVoter core classes
├── polling_places.py  # Polling place data mapped by district
├── registry.py        # Voter registration, lookup, and file persistence logic
├── main.py            # Console application driver
└── tests/             # Unit test suite
