from MongoWrapper import MongoWrapper


# Function to add Dex accounts to Database
# This is hardcoded, it is not synced with Dex.
def addDexUsers(mongo: MongoWrapper, DB_USERS:str, COL_USERS:str):
    users = [
        {
            "email": "admin@hw3.com",
            "hash": "$2b$10$8NoCpIs/Z6v0s/pU9YxYIO10uWyhIVOS2kmNac9AD0HsqRhP5dUie",  # password = "password"
            "username": "admin",
            "userID": "123",
        },
        {
            "email": "moderator@hw3.com",
            "hash": "$2b$12$2aaoZyVjMWvoCq.DmCUECOGoW0oaBCyzSluUm3BpLrP26sVT71PSC",  # password = "mpassword"
            "username": "moderator",
            "userID": "456",
        },
        {
            "email": "user@hw3.com",
            "hash": "$2b$12$321HomfT164U9f5l.xQaYuHThGCss8PRPNy8t./tq8Frgr6UYeEka",  # password = "upassword"
            "username": "user",
            "userID": "789",
        },
    ]
    for user in users:
        find = mongo.findDocument(
            DB_USERS,
            COL_USERS,
            {
                "email": user["email"],
                # "userID": user["userID"],
            },
        )
        if not find:
            mongo.insertDocument(
                DB_USERS,
                COL_USERS,
                {
                    "email": user["email"],
                    "username": user["username"],
                    "userID": user["userID"],
                    "friends": [],
                },
            )

# Function to add sample food logs to a user
# Does not do anything if user has *any* food logged already
def addSampleFoods(mongo: MongoWrapper, DB_FOOD:str, COL_FOOD:str, userEmail: str, month: int, day: int):
    def toStr(num: int):
        return str(num).zfill(2)

    todayStr = f"2025-{toStr(month)}-{toStr(day)}"
    lastMonth = f"2025-{toStr(month-1)}-{toStr(day)}"

    foodData = [
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
    find = mongo.findDocument(
        DB_FOOD,
        COL_FOOD,
        {"userid": userEmail},
    )
    if not find:
        for food in foodData:
            mongo.insertDocument(
                DB_FOOD,
                COL_FOOD,
                food,
            )


# Function to add sample record data to a user
# Does not do anything if user has *any* recordgoal data already
def addSampleRecords(mongo: MongoWrapper, DB_USERS:str, COL_RECORD:str, userEmail: str):
    recordData = [
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
    find = mongo.findDocument(
        DB_USERS,
        COL_RECORD,
        {"userid": userEmail},
    )
    if not find:
        for record in recordData:
            mongo.insertDocument(
                DB_USERS,
                COL_RECORD,
                record,
            )

