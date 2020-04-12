import time, calendar
from datetime import datetime

MAX_YEARS = 80
MAX_MONTHS = 12
MAX_DAYS = 30
MAX_HOURS = 60
MAX_MINUTES = 60

def getTimeMaxTime(givenTime):
    diffInTime  =  givenTime-time.time()

    noOfMinutes =  diffInTime/60
    noOfHours   =  noOfMinutes/60
    noOfDays    =  noOfHours/24
    noOfMonths  =  noOfDays/30
    noOfYears   =  noOfMonths/12

    theYearInInteger = int(diffInTime/(60*60*24*30*12))
    noOfMonthRem = (noOfYears-theYearInInteger)*12 #gives me number of months in point
    theMonthInInteger = int(noOfMonthRem)
    noOFDaysRem = (noOfMonthRem-theMonthInInteger)*30
    theDaysInInteger = int(noOFDaysRem)
    noOfHourRem = (noOFDaysRem-theDaysInInteger)*24
    theHourInInteger = int(noOfHourRem)
    noOfMinuteRem = (noOfHourRem-theHourInInteger)*60
    theMinuteInInteger = int(noOfMinuteRem)

    times= []
    maxTimes= []
    times.extend((theYearInInteger,theMonthInInteger,theDaysInInteger,theHourInInteger,theMinuteInInteger))
    times = list(map(lambda x: str(x)[:3],times))
    maxTimes.extend([MAX_YEARS,MAX_MONTHS,MAX_DAYS,MAX_HOURS,MAX_MINUTES])
    return times,maxTimes

