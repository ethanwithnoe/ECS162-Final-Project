from MongoWrapper import MongoWrapper


# Function to add Dex accounts to Database
# This is hardcoded, it is not synced with Dex.
def addDexUsers(mongo: MongoWrapper, DB_USERS: str, COL_USERS: str):
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
    for user in users:
        find = mongo.findDocument(
            DB_USERS,
            COL_USERS,
            {
                "email": user["email"],
            },
        )
        if not find:
            mongo.insertDocument(
                DB_USERS,
                COL_USERS,
                {
                    "email": user["email"],
                    "username": user["username"],
                    "friends": [],
                },
            )


# Function to add sample food logs to a user
def addSampleFoods(
    mongo: MongoWrapper,
    DB_FOOD: str,
    COL_FOOD: str,
    userEmail: str,
    month: int,
    day: int,
):
    def toStr(num: int):
        return str(num).zfill(2)

    todayStr = f"2025-{toStr(month)}-{toStr(day)}"
    lastMonth = f"2025-{toStr(month-1)}-{toStr(day)}"

    data = [
        {
            "calories": 300,
            "carbohydrates": 45,
            "fat": 10,
            "protein": 20,
            "description": "Morning Oatmeal",
            "name": "Oatmeal",
            "timestamp": f"{lastMonth}T08:00:00.000000-08:00",  # 8:00 AM > falls into the 8 AM bin
            "userid": userEmail,
            # "_id": "119"
        },
        {
            "calories": 450,
            "carbohydrates": 60,
            "fat": 15,
            "protein": 25,
            "description": "Chicken Salad",
            "name": "Grilled Chicken Salad",
            "timestamp": f"{todayStr}T10:15:00.000000-08:00",
            "userid": userEmail,
            # "_id": "11"
        },
        {
            "calories": 150,
            "carbohydrates": 20,
            "fat": 5,
            "protein": 10,
            "description": "Apple and Peanut Butter",
            "name": "Snack",
            "timestamp": f"{todayStr}T12:30:00.000000-08:00",
            "userid": userEmail,
            # "_id": "11"
        },
        {
            "calories": 600,
            "carbohydrates": 75,
            "fat": 20,
            "protein": 40,
            "description": "Dinner - Steak and Potatoes",
            "name": "Steak Dinner",
            "timestamp": f"{todayStr}T17:00:00.000000-08:00",
            "userid": userEmail,
            # "_id": "11"
        },
        {
            "calories": 200,
            "carbohydrates": 30,
            "fat": 10,
            "protein": 15,
            "description": "Evening Smoothie",
            "name": "Smoothie",
            "timestamp": f"{todayStr}T20:00:00.000000-08:00",
            "userid": userEmail,
            # "_id": "11"
        },
    ]
    mongo.deleteDocument(
        DB_FOOD,
        COL_FOOD,
        {"isDemo": True},
    )
    for doc in data:
        doc["isDemo"] = True
        mongo.insertDocument(
            DB_FOOD,
            COL_FOOD,
            doc,
        )


# Function to add sample record data to a user
def addSampleRecords(
    mongo: MongoWrapper, DB_USERS: str, COL_RECORD: str, userEmail: str
):
    data = [
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddc1"},
            "calories": True,
            "protein": True,
            "fat": True,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-05-10",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddc2"},
            "calories": True,
            "protein": True,
            "fat": True,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-05-11",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddc3"},
            "calories": True,
            "protein": False,
            "fat": True,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-05-12",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddc4"},
            "calories": True,
            "protein": True,
            "fat": True,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-05-13",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddc5"},
            "calories": True,
            "protein": True,
            "fat": False,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-05-14",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddc6"},
            "calories": True,
            "protein": True,
            "fat": True,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-05-15",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddc7"},
            "calories": False,
            "protein": True,
            "fat": True,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-05-16",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddc8"},
            "calories": True,
            "protein": True,
            "fat": True,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-05-17",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddc9"},
            "calories": True,
            "protein": True,
            "fat": False,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-05-18",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddca"},
            "calories": True,
            "protein": True,
            "fat": True,
            "carbohydrates": False,
            "userid": userEmail,
            "timestamp": "2025-05-19",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddcb"},
            "calories": True,
            "protein": True,
            "fat": True,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-05-20",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddcc"},
            "calories": True,
            "protein": True,
            "fat": True,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-05-21",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddcd"},
            "calories": False,
            "protein": True,
            "fat": True,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-05-22",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddce"},
            "calories": True,
            "protein": True,
            "fat": True,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-05-23",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddcf"},
            "calories": True,
            "protein": False,
            "fat": True,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-05-24",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddd0"},
            "calories": True,
            "protein": True,
            "fat": True,
            "carbohydrates": False,
            "userid": userEmail,
            "timestamp": "2025-05-25",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddd1"},
            "calories": True,
            "protein": True,
            "fat": False,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-05-26",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddd2"},
            "calories": True,
            "protein": True,
            "fat": True,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-05-27",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddd3"},
            "calories": True,
            "protein": True,
            "fat": True,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-05-28",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddd4"},
            "calories": True,
            "protein": True,
            "fat": True,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-05-29",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddd5"},
            "calories": False,
            "protein": False,
            "fat": True,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-05-30",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddd6"},
            "calories": True,
            "protein": True,
            "fat": True,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-05-31",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddd7"},
            "calories": True,
            "protein": True,
            "fat": False,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-06-01",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddd8"},
            "calories": True,
            "protein": True,
            "fat": True,
            "carbohydrates": False,
            "userid": userEmail,
            "timestamp": "2025-06-02",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddd9"},
            "calories": True,
            "protein": True,
            "fat": True,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-06-03",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024ddda"},
            "calories": True,
            "protein": True,
            "fat": True,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-06-04",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024dddb"},
            "calories": True,
            "protein": False,
            "fat": True,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-06-05",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024dddc"},
            "calories": True,
            "protein": True,
            "fat": True,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-06-06",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024dddd"},
            "calories": True,
            "protein": True,
            "fat": False,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-06-07",
        },
        {
            # "_id": {"$oid": "6845294727d84e4d2024dee4"},
            "calories": True,
            "protein": True,
            "fat": False,
            "carbohydrates": True,
            "userid": userEmail,
            "timestamp": "2025-06-08",
        },
    ]

    mongo.deleteDocument(
        DB_USERS,
        COL_RECORD,
        {"isDemo": True},
    )
    for doc in data:
        doc["isDemo"] = True
        mongo.insertDocument(
            DB_USERS,
            COL_RECORD,
            doc,
        )


# Function to add sample record data to a user
def addSampleGoals(
    mongo: MongoWrapper,
    DB_USERS: str,
    COL_GOALS: str,
    userEmail: str,
    month: int,
    day: int,
):
    def toStr(num: int):
        return str(num).zfill(2)

    todayStr = f"2025-{toStr(month)}-{toStr(day)}"
    data = [
        {
            # "_id": "68492a1b579b4a8baea8e9c8",
            "Age": 22,
            "Gender": "M",
            "HeightFt": 5,
            "HeightIn": 4,
            "HeightCM": 162.56,
            "Weight": 144,
            "WeightKG": 65.31730128000001,
            "Activity": "L",
            "BMR": 1564.1730128000002,
            "AMR": 2150.7378926,
            "calories": 2151,
            "protein": 54,
            "fat": 48,
            "carbohydrates": 242,
            "userid": userEmail,
            "timestamp": f"{todayStr}T10:15:00.000000-08:00",
        }
    ]
    mongo.deleteDocument(
        DB_USERS,
        COL_GOALS,
        {"isDemo": True},
    )
    for doc in data:
        doc["isDemo"] = True
        mongo.insertDocument(
            DB_USERS,
            COL_GOALS,
            doc,
        )


# master caller function
# change demo data params here
def generateSampleData(
    mongo: MongoWrapper,
    DB_USERS: str,
    DB_FOOD: str,
    COL_USERS: str,
    COL_FOOD: str,
    COL_GOALS: str,
    COL_RECORD: str,
):
    userEmail = "moderator@hw3.com"
    month = 6
    day = 11

    addDexUsers(mongo=mongo, DB_USERS=DB_USERS, COL_USERS=COL_USERS)
    addSampleFoods(
        mongo=mongo,
        DB_FOOD=DB_FOOD,
        COL_FOOD=COL_FOOD,
        userEmail=userEmail,
        month=month,
        day=day,
    )
    addSampleRecords(
        mongo=mongo,
        DB_USERS=DB_USERS,
        COL_RECORD=COL_RECORD,
        userEmail=userEmail,
    )
    addSampleGoals(
        mongo=mongo,
        DB_USERS=DB_USERS,
        COL_GOALS=COL_GOALS,
        userEmail=userEmail,
        month=month,
        day=day,
    )
