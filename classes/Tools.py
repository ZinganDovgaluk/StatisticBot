import time
from math import ceil


sbj_names = {"ukrlit":"Українська та зарубіжна культура",
			 "primat":"Прикладна математика",
			 "nos":"Науковий образ світу",
			 "teorver":"Теорія ймовірностей та математична статистика",
			 "kgv":"Комп’ютерна графіка та візуалізація",
			 "sql":"SQL",
			 "ookp":"Об'єктно-орієнтоване конструювання програм",
			 "null":"null"}
sbj_kinds = {"lec":"(Лекція)","pr":"(Практика)"}


class BackTool:
	# Says is value between of two values or not
	@classmethod
	def is_between(cls, left_lim=0.0, value=1.0, right_lim=2.0):
		if left_lim <= value <= right_lim:
			return True
		else:
			return False

	# Splits string by two
	@classmethod
	def divided_by_two_string(cls, string):
		return [
			string[:int(len(string) / 2)],
			string[int(len(string) / 2):]
		]

	@classmethod
	def get_time_dict(cls):
		now = time.ctime(time.time()).split()
		now_time = [int(now[3].split(":")[i]) for i in range(3)]
		return {"day": now[0], "hours": now_time[0], "minutes": now_time[1], "seconds": now_time[2]}

	@classmethod
	def get_curr_time_str(cls, add_hour=0, add_min=0):
		return str(BackTool.get_time_dict()["hours"] + add_hour) + ":" + str(BackTool.get_time_dict()["minutes"] + add_min)

	@classmethod
	def week_of_study(cls):
		months = {"Sep": 1, "Oct": 2, "Nov": 3, "Dec": 4, "Jan": 5, "Feb": 6, "Mar": 7, "Apr": 8, "May": 9,
				  "Jun": 10, "Jul": 11, "Aug": 12}
		months_days = [30, 31, 30, 31, 31, 28, 31, 30, 31, 30, 31, 31]
		now = time.ctime(time.time()).split()
		study_time_hours = int(now[2]) * 24 + int(now[3].split(":")[0])
		for i in range(months[now[1]] - 1):
			study_time_hours += months_days[i] * 24
		return ceil(study_time_hours / 24 / 7)

	@classmethod
	def rename_sbj(cls, sbj_name):
		if sbj_name != "null":
			return sbj_names[sbj_name]
		else:
			return None

	@classmethod
	def rekind_sbj(cls, sbj_kind):
		if sbj_kind != "null":
			return sbj_kinds[sbj_kind]
		else:
			return "null"
