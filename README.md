# Voter Registration & Polling Place Lookup System

A Python console application that registers voters, validates their information,
and matches each voter to their assigned polling place based on district.

## What It Demonstrates
- Object-oriented design with a class hierarchy (`Voter` → `AbsenteeVoter`),
  using inheritance and polymorphism to model distinct voter types
- Custom exception handling for invalid data and duplicate registrations
- File I/O for persisting the voter roll between sessions
- An 18-test unit test suite (`unittest`) covering validation, equality,
  and save/load round-trips
- Input validation with a re-prompting console menu

## How to Run
\`\`\`
python3 main.py
\`\`\`

## Run Tests
\`\`\`
python3 -m unittest discover -s tests -v
\`\`\`

## Project Structure
- `voter.py` — Voter and AbsenteeVoter classes
- `polling_places.py` — polling place data by district
- `registry.py` — registration, lookup, and file persistence logic
- `main.py` — console driver
- `tests/` — unit tests
