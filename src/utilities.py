
from typing import List
import datetime
import pandas as pd


class Util:

    # redondea la fecha a la decena de minutos más cercana y le suma 20 segundos
    def roundTime(date:datetime.datetime) -> datetime:
        time = pd.Timestamp(date)
        time = time.round('10min')
        time += datetime.timedelta(seconds=20)
        return time.to_pydatetime()
    
    # devuelve la fecha con la que se puede obtener la última imagen de satélite
    def getLastAvailableDate() -> datetime.datetime:
        date = datetime.datetime.now()
        date = Util.roundTime(date)
        
        date -= datetime.timedelta(minutes=40)
        return date

    # 1 = 10 minutos
    def generateDates(amount:int) -> List[datetime.datetime]:
        date = Util.roundTime(Util.getLastAvailableDate())
        dates = []

        for i in range(amount):
            dates.append(date)
            date -= datetime.timedelta(minutes=10)

        return dates

# for date in Util.generateDates(24):
#     print(date.strftime("%Y-%m-%d %H:%M:%S"))
