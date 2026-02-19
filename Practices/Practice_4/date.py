import datetime

# ex 1

time_now = datetime.datetime.now()
five_days_before = datetime.timedelta(days = 5)
print(time_now - five_days_before)

# ex 2

diff = datetime.timedelta(days = 1)

print(f"yesterday: {time_now - diff}\nToday: {time_now} \nTomorrow: {time_now + diff}")

# ex 3
time_without_ms = time_now.strftime("%Y-%m-%d %H:%M:%S") # method 1
time_without_ms = time_now.replace(microsecond = 0) # method 2
print(time_without_ms)

# ex 4
date1 = input()
date2 = input()

d1 = datetime.datetime.strptime(date1, "%Y-%m-%d %H:%M:%S")
d2 = datetime.datetime.strptime(date2, "%Y-%m-%d %H:%M:%S")

dt_diff = abs((d1 - d2).total_seconds())
print(dt_diff)
