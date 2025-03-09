from DataBase.habit import Habit, Period
from DataBase.habit_completion import HabitCompletion
from Services.auth import get_current_user

def run_habit_management():
    menu_prompt = """
---Habit Management---
    press 1 to display schedule
    press 2 to complete a habit task
    press 3 to list all habits.
    press 4 to list all habit completions 
    press 5 to create a new habit.
    press 6 to update a habit.
    press 7 to delete a habit.
    press 8 to insert 5 predefined habits
    press 0 to go back to the main menu.
    please enter your choice:
    """

    while (user_input := input(menu_prompt)) != "0":
        match user_input:
            case "1":
                display_schedule()
            case "2":
                complete_habit()
            case "3":
                print("-List all habits-")
                list_habits()
            case "4":
                get_all_completions()
            case "5":
                create_habit()
            case "6":
                update_habit()
            case "7":
                delete_habit()
            case "8":
                insert_predefined_habits()


def display_schedule():
    habits=Habit.get_all_habits( get_current_user().id )
    habits_completions = []
    for habit in habits:
        completions = HabitCompletion.get(habit.id) or []
        for completion in completions:
            habits_completions.append(completion)

    habits_to_be_completed=[]

    for habit in habits:
        completions = []
        for completion in habits_completions:
            if completion.habit_id == habit.id:
                completions.append(completion)

        if len(completions)==0:
            habits_to_be_completed.append(habit)
            continue


        expected_period_number = HabitCompletion.calc_period_number(habit)
        last_completion_period = max([c.period_number for c in completions], default=-1)

        if last_completion_period < expected_period_number:
            habits_to_be_completed.append(habit)

    if not habits_to_be_completed:
        print("All habits are up to date! No pending tasks.")
        return

    print("---Habit Schedule---")
    print(f"{'ID':<5} {'| Habit Title':<20} {'| Due Period':<10} {'| Period Type':<10}")
    print("-" * 55)

    for habit in habits_to_be_completed:
        expected_period_number = HabitCompletion.calc_period_number(habit)
        print(f"{habit.id:<5}| {habit.title:<20}| {expected_period_number:<10}| {habit.period:<10}")

    print("You have pending habit tasks to complete!")

    return habits_to_be_completed

def create_habit():
    print("-Create Habit-")
    title = input("Enter habit title: ")
    description = input("Enter habit description (optional): ")
    period = input("Enter habit period (daily or weekly): ").strip().lower()
    while period not in Period._value2member_map_:
        period = input("please enter valid choise for habit period (daily or weekly): ").strip().lower()
    habit = Habit(user_id=get_current_user().id, title=title, description=description, period=Period(period))
    habit.save()
    print("Habit created successfully.")

def update_habit():
    print("-Update Habit-")
    list_habits()
    habit_id = int(input("Enter habit ID to be updated: "))
    title = input("Enter new habit title (optional): ")
    description = input("Enter new habit description (optional): ")
    period = input("Enter new habit period (daily or weekly, optional): ")
    habit = Habit.get(habit_id)
    if title:
        habit.title = title
    if description:
        habit.description = description
    if period:
        habit.period = Period[period.upper()]
    habit.update()
    print("Habit updated successfully.")

def delete_habit():
    print("-Delete Habit-")
    list_habits()
    habit_id = int(input("Enter habit ID to delete: "))
    Habit.delete(habit_id)
    print("Habit deleted successfully.")

def list_habits(habits=None):
    if habits is None:
        habits = Habit.get_all_habits(get_current_user().id)
        if not habits :
            print("user has no habits.")

    print(f"{'ID':<5} {'| Habit Title':<20} {'| Habit description ':<40} {'| Period Type':<10}")
    print("-" * 55)
    for habit in habits:
        print(f"{habit.id:<5}| {habit.title:<20}| {habit.description:<40}| {habit.period:<10}")

def complete_habit():
    tasks=display_schedule()
    if not tasks:
        return
    valid_ids = {habit.id for habit in tasks}
    habit_id = int(input("Enter habit ID to complete from schedule: "))

    while habit_id not in valid_ids:
        print("Invalid habit ID. Please enter a valid ID from the schedule.")

    habit_completeion = HabitCompletion(Habit.get(habit_id))
    if habit_completeion.save() is True:
        print("habit completed successfully")
        print(habit_completeion)
    else:
        print("Error: habit completion not saved successfully")

def get_all_completions():
    list_habits()
    habit_id = int(input("Enter habit ID: "))
    habit_completions = HabitCompletion.get(habit_id)
    habit=Habit.get(habit_id)
    if not habit_completions:
        print("No completions found for this habit.")
    else:
        print(f"-List all completions for habit id {habit_id} with title {habit.title} -")
        print(f"{'Completion date'} \t\t  {'| Period number'}\t\t{'| Period type'}")
        print("-" * 55)
        for completion in habit_completions:
            print(f"{str(completion.completion_date.date()):<20}| {completion.period_number:<10}| {habit.period:<15}")

def insert_predefined_habits():
    user_id = get_current_user().id
    predefined_habits = [
        {"id": 1,"title": "sport", "description": "Do a 30-minute sport", "period": Period.DAILY},
        {"id": 2,"title": "read", "description": "Read for at least 20 minutes", "period": Period.DAILY},
        {"id": 3,"title": "water", "description": "Drink 2 liters of water", "period": Period.DAILY},
        {"id": 4,"title": "healthy food", "description": "don't eat junke food", "period": Period.DAILY},
        {"id": 5,"title": "sleep enough", "description": "sleep about 8 hours", "period": Period.DAILY},
    ]

    new_predefined_habits=[]
    for habit in predefined_habits:
        h = Habit(user_id=user_id, title=habit["title"],
                  description=habit["description"], period=habit["period"],habit_id=habit["id"])
        new_predefined_habits.append(h)

    print("\n--- Predefined Habits ---")
    list_habits(new_predefined_habits)


    for habit in predefined_habits:
        h = Habit(user_id=user_id, title=habit["title"],
                  description=habit["description"], period=habit["period"])
        h.save()

    print(f"predefined habits added successfully")
