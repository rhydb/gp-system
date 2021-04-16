import datetime

# if the year is multiple of 400
# or year is multiple of 4 but not 100
# it is a leap year
def is_leap_year(year: int):
    return year % 400 == 0 or year % 4 == 0 and year % 100 != 0

def is_valid_date(date: str) -> bool:
    CURRENT_DATE =  datetime.datetime.now()
    CURRENT_YEAR = CURRENT_DATE.year
    CURRENT_MONTH = CURRENT_DATE.month
    CURRENT_DAY = CURRENT_DATE.day
    YEAR_RANGE = 150 # oldest year is 100 years before
    # date must be in the format dd-mm-yyyy
    # seperated by - and all must be integer
    split = date.split("-")
    if len(split) != 3:
        return False
    try:
        day = int(split[0])
        month = int(split[1])
        year = int(split[2])
    except Exception:
        return False

    # check if the year and month is within range
    if year < CURRENT_YEAR - YEAR_RANGE or year > CURRENT_YEAR:
        return False
    if month < 1 or month > 12:
        return False

    # check if day is within range
    # check if month is february and if so is within the range
    if month == 2:
        # 28 days normally, 29 on leap year
        # leap year is every 4 years
        if is_leap_year(year):
            if day > 29:
                return False
        elif day > 28:
            return False
    else: # month other than february
        # months 4 6 9 and 11 have 30 days
        if month == 4 \
                or month == 6 \
                or month == 9 \
                or month == 11 \
                and day > 30:
            return False
    return True
