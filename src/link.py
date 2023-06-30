import datetime


class Link:
    
    link = "https://estaticos.smn.gob.ar/vmsr/satelite/TOP_C13_ARG_ALTA_"
    date = datetime.datetime.now()
    fileStrFile = "%Y-%m-%d %H;%M;%S.jpg"

    def __init__(self):
        pass

    def setDate(self, date:datetime.datetime) -> None:
        self.date = date

    def setHour(self, hour: int) -> None:
        self.date = self.date.replace(hour=hour)

    def setMinute(self, minute: int) -> None:
        self.date = self.date.replace(minute=minute)

    def setSecond(self, second: int) -> None:
        self.date = self.date.replace(second=second)

    def addMinutes(self) -> None:
        self.date = self.date + datetime.timedelta(minutes=10)

    def addSeconds(self, seconds: int) -> None:
        self.date = self.date + datetime.timedelta(seconds=seconds)

    def addHours(self, hours: int) -> None:
        self.date = self.date + datetime.timedelta(hours=hours)

    def __dateToString(self) -> str:
        auxDate = self.date + datetime.timedelta(hours=3)
        return auxDate.strftime("%Y%m%d_%H%M%SZ.jpg")

    def getFilename(self) -> str:
        return self.date.strftime("%Y-%m-%d %H;%M;%S.jpg")

    def getFinalLink(self) -> str:
        return self.link + self.__dateToString()
