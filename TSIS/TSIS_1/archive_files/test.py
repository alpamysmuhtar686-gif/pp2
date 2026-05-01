import datetime
birthday = "2026-04-26"
try:
    result = datetime.datetime.strptime(birthday, "%Y-%M-%d")
    print(result)
except Exception as error:
    print(f"error: {error}")