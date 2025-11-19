import re, os

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
        "tue": {'date': None, 'bf': [], 'lunch': [], 'dinner': []},
        "wed": {'date': None, 'bf': [], 'lunch': [], 'dinner': []},
        "thu": {'date': None, 'bf': [], 'lunch': [], 'dinner': []},
        "fri": {'date': None, 'bf': [], 'lunch': [], 'dinner': []}
    }
    days = {
        0: "sat",
        1: "sun",
        2: "mon",
        3: "tue",
        4: "wed",
        5: "thu",
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

    return f"""
<b>شنبه</b> (<i><u>{table["sat"]["date"]}</u></i>)<b>:</b>
<blockquote>
<b>صبحانه:</b> {" | ".join(table["sat"]["bf"])}
<b>ناهار:</b> {" | ".join(table["sat"]["lunch"])}
<b>شام:</b> {" | ".join(table["sat"]["dinner"])}
</blockquote>
<b>یکشنبه</b> (<i><u>{table["sun"]["date"]}</u></i>)<b>:</b>
<blockquote>
<b>صبحانه:</b> {" | ".join(table["sun"]["bf"])}
<b>ناهار:</b> {" | ".join(table["sun"]["lunch"])}
<b>شام:</b> {" | ".join(table["sun"]["dinner"])}
</blockquote>
<b>دوشنبه</b> (<i><u>{table["mon"]["date"]}</u></i>)<b>:</b>
<blockquote>
<b>صبحانه:</b> {" | ".join(table["mon"]["bf"])}
<b>ناهار:</b> {" | ".join(table["mon"]["lunch"])}
<b>شام:</b> {" | ".join(table["mon"]["dinner"])}
</blockquote>
<b>سه‌شنبه</b> (<i><u>{table["tue"]["date"]}</u></i>)<b>:</b>
<blockquote>
<b>صبحانه:</b> {" | ".join(table["tue"]["bf"])}
<b>ناهار:</b> {" | ".join(table["tue"]["lunch"])}
<b>شام:</b> {" | ".join(table["tue"]["dinner"])}
</blockquote>
<b>چهارشنبه</b> (<i><u>{table["wed"]["date"]}</u></i>)<b>:</b>
<blockquote>
<b>صبحانه:</b> {" | ".join(table["wed"]["bf"])}
<b>ناهار:</b> {" | ".join(table["wed"]["lunch"])}
<b>شام:</b> {" | ".join(table["wed"]["dinner"])}
</blockquote>
<b>پنج‌شنبه</b> (<i><u>{table["thu"]["date"]}</u></i>)<b>:</b>
<blockquote>
<b>صبحانه:</b> {" | ".join(table["thu"]["bf"])}
<b>ناهار:</b> {" | ".join(table["thu"]["lunch"])}
<b>شام:</b> {" | ".join(table["thu"]["dinner"])}
</blockquote>
<b>جمعه</b> (<i><u>{table["fri"]["date"]}</u></i>)<b>:</b>
<blockquote>
<b>صبحانه:</b> {" | ".join(table["fri"]["bf"])}
<b>ناهار:</b> {" | ".join(table["fri"]["lunch"])}
<b>شام:</b> {" | ".join(table["fri"]["dinner"])}
</blockquote>
"""

def extract(src):
    dates, meals = clean(src)
    table = classify(dates, meals)
    string = to_str(table)

    return string


def write(string, week):
    with open(os.path.join("menu_data", f"{week}.txt"), 'w', encoding="utf-8") as f:
        f.write(string)

def read(week):
    with open(os.path.join("menu_data", f"{week}.txt"), 'r', encoding='utf-8') as f:
        src = f.read()
    return src


class Menu:
    def __init__(self):
        self.pre = None
        self.current = None
        self.next = None

    def update(self):
        self.pre = read('pre')
        self.current = read('current')
        self.next = read('next')

