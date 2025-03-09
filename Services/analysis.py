from DataBase.habit import Period, Habit
from DataBase.habit_completion import HabitCompletion
from Services.auth import get_current_user
from Services.habit_management import list_habits

# run analysis part code
def run_analysis():
    menu_prompt = f"""
---Analysis for {get_current_user().name} habits---
    press 1 to list all tracked habits
    press 2 to list habits with a specific periodicity
    press 3 to get the longest run streak of all habits
    press 4 to get the longest run streak for a specific habit
    press 0 to go back
    please enter your choice:
    """
    while (user_input := input(menu_prompt)) != "0":
        match user_input:
            case "1":
                list_habits()
            case "2":
                list_habits_with_same_periodicity()
            case "3":
                get_longest_run_streak_of_habits()

            case "4":
                get_longest_run_streak_of_habit()

# print habits with same period
def list_habits_with_same_periodicity():

    # get user input for period type
    period_input = input("Enter periodicity (daily/weekly): ").strip().lower()

    # get enum period type
    while period_input not in Period._value2member_map_:
        period_input = input("please enter valid choise for habit period (daily or weekly): ").strip().lower()

    period_input=Period(period_input)
    # init empty habits list to hold habits with same period
    habits = []

    # loop over all habits for a user to get one with period
    for habit in Habit.get_all_habits(get_current_user().id):
        if habit.period == period_input:
            habits.append(habit)

    # if there habits then print it
    if habits:
        print(f"Habits with periodicity {period_input}:")
        list_habits(habits)
        return habits
    else:
        print(f"No habits found with periodicity {period_input}.")
        return None

def get_longest_run_streak_of_habits():
    # Get all habits of the current user
    user = get_current_user()
    if not user:
        print("Error: No current user found.")
        return 0

    habits = Habit.get_all_habits(user.id)
    if not habits:  # Ensure habits is not None
        print("No habits found.")
        return 0

    # To store the longest completed habit streak
    max_streak_per_habits = 0
    best_habit = None

    for habit in habits:
        # Get all completions of a habit
        completions = HabitCompletion.get(habit.id)
        if not completions:  # Ensure completions is not None
            continue

        # Extract period numbers
        periods = [c.period_number for c in completions if c.period_number is not None]

        if not periods:  # Skip if there are no valid periods
            continue

        # Sort periods to find max consecutive streak
        periods.sort()

        # Variables to track the max streak
        habit_maximum_streak = 1
        habit_streak = 1

        for i in range(1, len(periods)):
            if periods[i] == periods[i - 1] + 1:
                habit_streak += 1
            else:
                habit_streak = 1

            habit_maximum_streak = max(habit_maximum_streak, habit_streak)

        # Check if a new best habit is found
        if max_streak_per_habits < habit_maximum_streak:
            best_habit = habit
            max_streak_per_habits = habit_maximum_streak

    # Print output based on the best habit
    if best_habit:
        print(f"Longest run streak: {max_streak_per_habits} periods for {best_habit}")
        return max_streak_per_habits
    else:
        print("No completed habits found.")
        return 0

def get_longest_run_streak_of_habit():
    print("""
-- Get longest run streak for habit --
Here are all habits, please choose which one you want: """)

    # Print all habits
    list_habits()

    try:
        # Take user input of habit ID
        habit_id = int(input("Enter habit ID: "))
    except ValueError:
        print("Invalid input. Please enter a valid habit ID.")
        return 0

    # Get the habit object
    habit = Habit.get(habit_id)
    if habit is None:
        print("Error: Habit not found.")
        return 0

    # Get all habit completions
    completions = HabitCompletion.get(habit_id)
    if not completions:  # Ensure completions is not None or empty
        print(f"No completions found for habit: {habit.title}")
        return 0

    # Extract period numbers while ensuring they are valid
    periods = [c.period_number for c in completions if c.period_number is not None]

    if not periods:
        print(f"No valid completion periods found for habit: {habit.title}")
        return 0

    # Sort periods to check for the max consecutive streak
    periods.sort()

    # Initialize variables for tracking the streak
    habit_maximum_streak = 1
    habit_streak = 1

    # Loop over periods to find the longest streak
    for i in range(1, len(periods)):
        if periods[i] == periods[i - 1] + 1:
            habit_streak += 1
        else:
            habit_streak = 1

        habit_maximum_streak = max(habit_maximum_streak, habit_streak)

    print(f"Longest run streak for {habit.title}: {habit_maximum_streak} periods")
    return habit_maximum_streak

