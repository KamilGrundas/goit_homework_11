from datetime import datetime

date_str = "2024-02-20"
date_obj = datetime.strptime(date_str, "%Y-%m-%d")
date_tuple = date_obj.timetuple()

year = date_tuple.tm_year
month = date_tuple.tm_mon
day = date_tuple.tm_mday

print(date_obj.year)