from classes.Tools import BackTool as bt


# Struct
class Week:
    def __init__(self, raw_arrays):
        self.monday = Day("Mon", raw_arrays, "Понеділок")
        self.tuesday = Day("Tue", raw_arrays, "Вівторок")
        self.wednesday = Day("Wed", raw_arrays, "Середа")
        self.thursday = Day("Thu", raw_arrays, "Четвер")
        self.friday = Day("Fri", raw_arrays, "П`ятниця")

        self.days = {
            "Mon": self.monday,
            "Tue": self.tuesday,
            "Wed": self.wednesday,
            "Thu": self.thursday,
            "Fri": self.friday,
        }

    def get_day(self, day_title):
        return self.days[day_title]


class Day:
    def __init__(self, name, raw_arrays, ukr_name):
        self.name = name
        self.lessons = LessonTool.generate_lessons_of_a_day_from_raw_array(self.name, raw_arrays)
        self.ukr_name = ukr_name

    def get_detail_info(self):
        lessons_info = ""
        for lesson in self.lessons:
            lessons_info += lesson.get_info() + '\n\n'

        return lessons_info

    def get_info(self):
        day_string = "<b>"+self.ukr_name + "</b>:\n"
        for lesson in self.lessons:
            lesson_string = lesson.time_period.get_str() + " "
            lesson_string += bt.rekind_sbj(lesson.kind)
            lesson_string += " "
            lesson_string += bt.rename_sbj(lesson.sbj_name)
            day_string += lesson_string + "\n"
        return day_string


class Lesson:
    def __init__(self, time_period, subject_name, week, kind, link):
        self.time_period = time_period
        self.sbj_name = subject_name
        self.week = week
        self.kind = kind
        self.link = link

    def get_info(self):
        return self.time_period.get_str() + '\n'+\
                bt.rename_sbj(self.sbj_name) + bt.rekind_sbj(self.kind) + '\n'+\
                self.link


class Period:
    def __init__(self, hours, minutes=0.0, seconds=0.0):
        self.begin = Time(hours, minutes, seconds)
        self.end = TimeTool.sum_of_time(self.begin, Time(1, 20, 0))

    def does_this_time_period(self, current):
        begin_secs = TimeTool.time_to_seconds(self.begin)
        now_secs = TimeTool.time_to_seconds(current)
        end_secs = TimeTool.time_to_seconds(self.end)
        if bt.is_between(begin_secs, now_secs, end_secs):
            return True
        return False

    def show(self):
        print("It goes ", end='')
        print("from ", end='')
        self.begin.show()
        print(" to ", end='')
        self.end.show()
        print()

    def get_str(self):
        return self.begin.get_str() + ' - ' + self.end.get_str()


class Time:
    def __init__(self, hours=0, minutes=0.0, seconds=0.0):
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds

    def show(self):
        print(str(self.hours) + ":" + str(self.minutes), end='')

    def get_str(self):
        h_str = str(self.hours)
        m_str = str(self.minutes)

        if self.hours < 10:
            h_str = '0' + h_str
        if self.minutes < 10:
            m_str = '0' + m_str

        return h_str + ':' + m_str

    def to_seconds(self):
        return TimeTool.time_to_seconds(self)


# Tools
class TimeTool:
    # Just makes int value of seconds from 'Time' object
    @classmethod
    def time_to_seconds(cls, time):
        return 3600 * time.hours + 60 * time.minutes + time.seconds

    # Makes 'Time' object from sum of two 'Time' objects
    @classmethod
    def sum_of_time(cls, time1, time2):
        hours, minutes, seconds = 0, 0, 0

        seconds += time1.seconds + time2.seconds
        if seconds >= 60:
            minutes += 1
            seconds -= 60

        minutes += time1.minutes + time2.minutes
        if minutes >= 60:
            hours += 1
            minutes -= 60

        hours += time1.hours + time2.hours
        if hours >= 24:
            hours -= 24

        return Time(hours, minutes, seconds)

    # Makes 'Time' object from for example "1540" string
    @classmethod
    def generate_time_period_from_str(cls, str_time_period):
        # For example makes ["15", "40"] from "1540"
        split_time_strings = bt.divided_by_two_string(str_time_period)
        # Make values of hours and minutes int and returns 'Period' object
        hours, minutes = int(split_time_strings[0]), int(split_time_strings[1])
        return Period(hours, minutes)


class LessonTool:
    # Generates array of 'Lesson' objects for concrete day
    @classmethod
    def generate_lessons_of_a_day_from_raw_array(cls, day_name, raw_arrays):
        lessons = []
        for raw_array in raw_arrays:
            # Now we found array with concrete day
            if raw_array[0] == day_name and raw_array[2] != "null":
                # Now we are collecting data for current 'Lesson' object
                time = raw_array[1]
                sbj_name = raw_array[2]
                week = int(raw_array[3])
                kind = raw_array[4]
                link = raw_array[5]
                # Now we adding Lesson object to array of current day
                lessons.append(Lesson(TimeTool.generate_time_period_from_str(time), sbj_name, week, kind, link))
        return lessons





