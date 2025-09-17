# House Shuffling Program

## Overview
The **House Shuffling Program** is designed to automate the distribution of students into school houses based on their recent achievements in sports and other events. In schools with large student populations, manual shuffling can be tedious and prone to bias. This program ensures a fair and balanced allocation of students across all houses, encouraging healthy competition, teamwork, and sportsmanship.

---

## Features
- Automatically distributes students into four houses: **Fathima, Montfort, Joseph, and Gabriel**.
- Balances the number of students and their achievements to ensure no house has an unfair advantage.
- Eliminates human bias and favoritism in the assignment process.
- Shuffles students randomly while maintaining an equitable distribution.
- Updates the main student database with the newly assigned house information.

---

## How It Works
1. Connects to a MySQL database containing student and achievement data.
2. Fetches all student records and categorizes them based on recent achievements.
3. Distributes students evenly into houses while balancing high achievers.
4. Creates tables for each house in the database and inserts the assigned students.
5. Updates the main `students` table with the house assignments.
6. Ensures each house has an equal chance to excel in curricular and extracurricular events.

---

## Requirements
- Python 3.x
- `mysql-connector-python` library
- MySQL database with `students` and `Achievements` tables

Install the MySQL connector using:

```bash
pip install mysql-connector-python
