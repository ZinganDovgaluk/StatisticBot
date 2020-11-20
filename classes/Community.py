from classes.Data import Data


class Group:
    def __init__(self, name, week):
        self.name = name
        self.week = week

    def get_day(self, day_name):
        return self.week.get_day(day_name)


class Groups:
    ipz211 = Group('ipz21/1', Data.week211)
    ipz212 = Group('ipz21/2', Data.week212)

    @classmethod
    def get_group_by_group_name(cls, name):
        if name == cls.ipz211.name:
            return cls.ipz211

        elif name == cls.ipz212.name:
            return cls.ipz212



 
