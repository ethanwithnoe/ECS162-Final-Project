# Opter Meal Tracker
ECS 162 Spring Quarter Final Project

Made by Group 11:
- Matthew Hoey
- Kyle Lam
- Ethan Liu
- Ty Matson
- Sean Singleton
- Ellison Song

## .env File

Some features of this app require an API key stored as an environment variable.

The `.env` file is not included in the repository, as is standard practice, but FOR GRADING PURPOSES, its contents are provided here:
```
USDA_API_KEY=BGnNaFcVG8j5Kg4Ysq8QSHFAmTM81pobhBcCcg2F
PORT=8000
```

## Sample Data
This project automatically adds sample data.

To disable this, remove or comment out lines `88` to `96` in `backend/app.py`:
```python
DemoData.generateSampleData(
    mongo=mongo,
    DB_USERS=DB_USERS,
    DB_FOOD=DB_FOOD,
    COL_USERS=COL_USERS,
    COL_FOOD=COL_FOOD,
    COL_GOALS=COL_GOALS,
    COL_RECORD=COL_RECORD,
)
```

The sample data can be configured to be added to specific account and is callibrated for a specifc day.

To change which account the sample data is attributed to, change line `483` in `backend/DemoData.py`:
```python
userEmail = "moderator@hw3.com"
```

To change which day the sample data centered around (today), change lines `485` to `487` in `backend/DemoData.py`:
```python
year = 2025
month = 6
day = 11
```
### Account Information

Account usernames and emails are added with the sample data call.
These can be changed on lines `7` to `20` in `backend/DemoData.py`:
```python
users = [
    {
        "email": "admin@hw3.com",
        "username": "admin",
    },
    {
        "email": "moderator@hw3.com",
        "username": "moderator",
    },
    {
        "email": "user@hw3.com",
        "username": "user",
    },
]
```
Passwords are not stored in the database. Authentication is handled by Dex.
