import re

def clean(src):
    src = str(src)
    date_pattern = r'<td class="ng-binding">(.*?)<br/>(.*?)</td>'
    dates = re.findall(date_pattern, src)
    meal_pattern = r'(\d)..Meals\[mealIndex\].FoodMenu"><i class="fa fa-caret-left"></i>(.+?)</p>'
    meals = re.findall(meal_pattern, src)

    return dates, meals


def classify(dates, meals):
    table = {"sat": {'date': None, 'bf': [], 'lunch': [], 'dinner': []},
        "sun": {'date': None, 'bf': [], 'lunch': [], 'dinner': []},
        "mon": {'date': None, 'bf': [], 'lunch': [], 'dinner': []},
        "tues": {'date': None, 'bf': [], 'lunch': [], 'dinner': []},
        "wedns": {'date': None, 'bf': [], 'lunch': [], 'dinner': []},
        "thurs": {'date': None, 'bf': [], 'lunch': [], 'dinner': []},
        "fri": {'date': None, 'bf': [], 'lunch': [], 'dinner': []}
    }
    days = {
        0: "sat",
        1: "sun",
        2: "mon",
        3: "tues",
        4: "wedns",
        5: "thurs",
        6: "fri",
    }
    diet = {
        0: 'bf',
        1: 'lunch',
        2: 'dinner'
    }

    
    for i, date in enumerate(dates):
        table[days[i]]['date'] = date[1].strip()

    
    diet_count = 0
    stack = 0
    for day, meal in meals:
        day = int(day)
        if day < stack:
            diet_count += 1

        stack = day
        table[days[day]][diet[diet_count]].append(meal)

    return table



def to_str(table):

    string = f"""
- شنبه {table["sat"]['date']}
    + صبحانه: {" | ".join(table["sat"]["bf"])}
    + ناهار: {" | ".join(table["sat"]["lunch"])}
    + شام: {" | ".join(table["sat"]["dinner"])}

- یکشنبه {table["sun"]['date']}
    + صبحانه: {" | ".join(table["sun"]["bf"])}
    + ناهار: {" | ".join(table["sun"]["lunch"])}
    + شام: {" | ".join(table["sun"]["dinner"])}

- دوشنبه {table["mon"]['date']}
    + صبحانه: {" | ".join(table["mon"]["bf"])}
    + ناهار: {" | ".join(table["mon"]["lunch"])}
    + شام: {" | ".join(table["mon"]["dinner"])}

- سه شنبه {table["tues"]['date']}
    + صبحانه: {" | ".join(table["tues"]["bf"])}
    + ناهار: {" | ".join(table["tues"]["lunch"])}
    + شام: {" | ".join(table["tues"]["dinner"])}

- چهارشنبه {table["wedns"]['date']}
    + صبحانه: {" | ".join(table["wedns"]["bf"])}
    + ناهار: {" | ".join(table["wedns"]["lunch"])}
    + شام: {" | ".join(table["wedns"]["dinner"])}

- پنجشنبه {table["thurs"]['date']}
    + صبحانه: {" | ".join(table["thurs"]["bf"])}
    + ناهار: {" | ".join(table["thurs"]["lunch"])}
    + شام: {" | ".join(table["thurs"]["dinner"])}

- جمعه {table["fri"]['date']}
    + صبحانه: {" | ".join(table["fri"]["bf"])}
    + ناهار: {" | ".join(table["fri"]["lunch"])}
    + شام: {" | ".join(table["fri"]["dinner"])}

"""

    return string

def extract(src):
    dates, meals = clean(src)
    table = classify(dates, meals)
    string = to_str(table)

    return string


def write(string, week):
    with open(f"data\\{week}.txt", 'w', encoding="utf-8") as f:
        f.write(string)

def read(week):
    with open(f"data\\{week}.txt", 'r', encoding='utf-8') as f:
        src = f.read()
    return src



class Menu:
    def __init__(self):
        self.pre = None
        self.corrent = None
        self.next = None

    def update(self):
        self.pre = read('pre')
        self.corrent = read('corrent')
        self.next = read('next')
