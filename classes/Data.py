from .Parser import Parser
from .TimeStruct import Week


class Data:
    week211 = Week(Parser.parse("files/schedule_21.txt")[0])
    week212 = Week(Parser.parse("files/schedule_21.txt")[1]) 