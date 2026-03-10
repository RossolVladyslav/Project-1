import json
from datetime import datetime, timedelta
import os

FILE_NAME = "events.json"


def load_events():
    if os.path.exists(FILE_NAME):
        with open(FILE_NAME, "r", encoding="utf-8") as file:
            return json.load(file)
    return []


def save_events(events):
    with open(FILE_NAME, "w", encoding="utf-8") as file:
        json.dump(events, file, indent=4, ensure_ascii=False)


def help_menu():
    print("""
Команди:
help      - довідка
add       - додати подію
list      - показати всі події
date      - події на дату
period    - події між датами
category  - події за категорією
search    - пошук події
week      - події на тиждень
today     - події сьогодні
tomorrow  - події завтра
next      - найближча подія
edit      - редагувати подію
delete    - видалити подію
exit      - завершити програму
""")


def find_conflict(events, date, time):
    for event in events:
        if event["date"] == date and event["time"] == time:
            print("У цей час вже є подія:", event["name"])
            return True
    return False


def create_event(events):
    name = input("Назва: ")
    date = input("Дата YYYY-MM-DD: ")
    time = input("Час HH:MM: ")
    category = input("Категорія: ")

    if find_conflict(events, date, time):
        return

    new_id = 1
    if len(events) > 0:
        max_id = 0
        for event in events:
            if event["id"] > max_id:
                max_id = event["id"]
        new_id = max_id + 1

    new_event = {
        "id": new_id,
        "name": name,
        "date": date,
        "time": time,
        "category": category
    }

    events.append(new_event)
    save_events(events)
    print("Подію додано")


def show_all_events(events):
    if len(events) == 0:
        print("Подій немає")
        return

    for event in events:
        print(f'{event["id"]}. {event["name"]} | {event["date"]} {event["time"]} | {event["category"]}')


def show_events_by_date(events):
    date = input("Введіть дату YYYY-MM-DD: ")
    found = False

    for event in events:
        if event["date"] == date:
            print(event["name"], event["time"], event["category"])
            found = True

    if not found:
        print("Подій на цю дату немає")


def show_events_by_period(events):
    start_date = input("Дата початку YYYY-MM-DD: ")
    end_date = input("Дата кінця YYYY-MM-DD: ")

    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    end_date = datetime.strptime(end_date, "%Y-%m-%d")

    found = False

    for event in events:
        current_date = datetime.strptime(event["date"], "%Y-%m-%d")
        if start_date <= current_date <= end_date:
            print(event["name"], event["date"], event["time"], event["category"])
            found = True

    if not found:
        print("Подій за цей період немає")


def show_events_by_category(events):
    category = input("Категорія: ")
    found = False

    for event in events:
        if event["category"].lower() == category.lower():
            print(event["name"], event["date"], event["time"])
            found = True

    if not found:
        print("Подій у цій категорії немає")


def search_events(events):
    text = input("Введіть слово для пошуку: ").lower()
    found = False

    for event in events:
        if text in event["name"].lower():
            print(event["name"], event["date"], event["time"], event["category"])
            found = True

    if not found:
        print("Нічого не знайдено")


def show_week_events(events):
    today = datetime.today()
    week_start = today - timedelta(days=today.weekday())
    week_end = week_start + timedelta(days=6)

    found = False

    for event in events:
        current_date = datetime.strptime(event["date"], "%Y-%m-%d")
        if week_start <= current_date <= week_end:
            print(event["name"], event["date"], event["time"])
            found = True

    if not found:
        print("Подій цього тижня немає")


def show_today_events(events):
    today = datetime.today().strftime("%Y-%m-%d")
    found = False

    for event in events:
        if event["date"] == today:
            print(event["name"], event["time"], event["category"])
            found = True

    if not found:
        print("Сьогодні подій немає")


def show_tomorrow_events(events):
    tomorrow = (datetime.today() + timedelta(days=1)).strftime("%Y-%m-%d")
    found = False

    for event in events:
        if event["date"] == tomorrow:
            print(event["name"], event["time"], event["category"])
            found = True

    if not found:
        print("Завтра подій немає")


def show_next_event(events):
    now = datetime.now()
    future_events = []

    for event in events:
        event_datetime = datetime.strptime(event["date"] + " " + event["time"], "%Y-%m-%d %H:%M")
        if event_datetime > now:
            future_events.append((event_datetime, event))

    if len(future_events) > 0:
        future_events.sort()
        nearest = future_events[0][1]
        print("Найближча подія:")
        print(nearest["name"], nearest["date"], nearest["time"], nearest["category"])
    else:
        print("Майбутніх подій немає")


def delete_event(events):
    show_all_events(events)

    try:
        event_id = int(input("Введіть ID події: "))
    except ValueError:
        print("Неправильний ID")
        return

    for event in events:
        if event["id"] == event_id:
            events.remove(event)
            save_events(events)
            print("Подію видалено")
            return

    print("Подію не знайдено")


def edit_event(events):
    show_all_events(events)

    try:
        event_id = int(input("Введіть ID події: "))
    except ValueError:
        print("Неправильний ID")
        return

    for event in events:
        if event["id"] == event_id:
            name = input("Нова назва: ")
            date = input("Нова дата: ")
            time = input("Новий час: ")
            category = input("Нова категорія: ")

            for other_event in events:
                if other_event["id"] != event_id and other_event["date"] == date and other_event["time"] == time:
                    print("У цей час вже є інша подія:", other_event["name"])
                    return

            event["name"] = name
            event["date"] = date
            event["time"] = time
            event["category"] = category

            save_events(events)
            print("Подію змінено")
            return

    print("Подію не знайдено")


def main():
    events = load_events()

    print("Вітаю! Це організатор подій")
    print("Введіть help, щоб побачити список команд")

    while True:
        command = input(">> ").lower()

        if command == "help":
            help_menu()
        elif command == "add":
            create_event(events)
        elif command == "list":
            show_all_events(events)
        elif command == "date":
            show_events_by_date(events)
        elif command == "period":
            show_events_by_period(events)
        elif command == "category":
            show_events_by_category(events)
        elif command == "search":
            search_events(events)
        elif command == "week":
            show_week_events(events)
        elif command == "today":
            show_today_events(events)
        elif command == "tomorrow":
            show_tomorrow_events(events)
        elif command == "next":
            show_next_event(events)
        elif command == "edit":
            edit_event(events)
        elif command == "delete":
            delete_event(events)
        elif command == "exit":
            print("Програму завершено")
            break
        else:
            print("Невідома команда")


main()"# Project-1" 
