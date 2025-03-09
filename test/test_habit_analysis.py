import pytest
from datetime import datetime, timedelta
from unittest.mock import patch, MagicMock
from DataBase.habit import Habit, Period
from DataBase.habit_completion import HabitCompletion
from DataBase.user import USER
from DataBase.database import DATABASE
from Services.analysis import list_habits_with_same_periodicity, get_longest_run_streak_of_habits, get_longest_run_streak_of_habit

test_habit_id="0"

# Fixture database setup
@pytest.fixture
def db():
    database = DATABASE()
    database.drop_database()
    return database

# Fixture creating a user
@pytest.fixture
def user(db):
    email = "test@test.com"
    user = USER.get(email)
    if not user:
        user = USER(name="Test User", email=email, password="password")
        user.save()
    return user

# Fixture creating a habit
@pytest.fixture
def create_habits(user):
    predefined_habits = [
        {"id": 1, "title": "sport", "description": "Do a 30-minute sport", "period": Period.DAILY},
        {"id": 2, "title": "read", "description": "Read for at least 20 minutes", "period": Period.WEEKLY},
        {"id": 3, "title": "water", "description": "Drink 2 liters of water", "period": Period.DAILY},
        {"id": 4, "title": "healthy food", "description": "don't eat junke food", "period": Period.WEEKLY},
        {"id": 5, "title": "sleep enough", "description": "sleep about 8 hours", "period": Period.DAILY},
    ]
    habits=[]

    for habit in predefined_habits:
        if Habit.get(habit["id"]):
            habits.append(Habit.get(habit["id"]))
            continue

        h = Habit(user_id=user.id, title=habit["title"],
                  description=habit["description"], period=habit["period"])
        h.save()
        habits.append(h)

    return habits

def create_habit_completion(user, habits):
    periods = [
        [0, 1, 2, 3, 5, 6, 7, 8, 10, 11, 12, 14, 15, 16, 18, 19, 20, 22, 23, 24, 26, 27, 28, 29],
        [0, 1, 3, 5],
        [0, 1, 2, 4, 5, 6, 7, 8, 10, 11, 12, 13, 15, 16, 18, 19, 20, 21, 22, 23, 25, 26, 28, 29],
        [0, 1, 2, 3, 5],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28]
    ]

    habit_completions = {}

    for habit, period in zip(habits, periods):
        habit_completions[habit.id] = []

        for p in period:
            completion = HabitCompletion(habit=habit, period_number=p)
            completion.save()
            habit_completions[habit.id].append(completion)

    return habit_completions

# Test listing habits by daily
@patch("builtins.input", return_value="daily")
@patch("Services.analysis.get_current_user")
def test_list_habits_by_periodicity_daily_case(mock_get_current_user, user, create_habits):

    mock_get_current_user.return_value = user

    # Mock the get_all_habits function
    with patch("DataBase.habit.Habit.get_all_habits", return_value=create_habits):
        returned_habits = list_habits_with_same_periodicity()

    # Assertions
    assert returned_habits is not None
    assert len(returned_habits) == 3
    for h in returned_habits:
        assert h.period == Period.DAILY

# Test for listing habits by weekly
@patch("builtins.input", return_value="weekly")
@patch("Services.analysis.get_current_user")
def test_list_habits_by_periodicity_weekly_case(mock_get_current_user, user, create_habits):

    mock_get_current_user.return_value = user

    # Mock the get_all_habits function
    with patch("DataBase.habit.Habit.get_all_habits", return_value=create_habits):
        returned_habits = list_habits_with_same_periodicity()

    # Assertions
    assert returned_habits is not None
    assert len(returned_habits) == 2
    for h in returned_habits:
        assert h.period == Period.WEEKLY

# Test getting the longest run streak of all habits
@patch("DataBase.habit.Habit.get_all_habits")
@patch("DataBase.habit_completion.HabitCompletion.get")
@patch("Services.analysis.get_current_user")
def test_longest_run_streak_all_habits(mock_get_current_user, mock_get_completions, mock_get_all_habits, user,
                                       create_habits):
    # Mock the current user
    mock_get_current_user.return_value = user

    # Mock the get_all_habits function
    mock_get_all_habits.return_value = create_habits


    completions=create_habit_completion(user,create_habits)

    mock_get_completions.side_effect = lambda habit_id: completions.get(habit_id, [])

    max_streak = get_longest_run_streak_of_habits()

    # Assertions
    assert max_streak == 16

# Test getting the longest run streak first habit
@patch("DataBase.habit.Habit.get")
@patch("DataBase.habit_completion.HabitCompletion.get")
@patch("Services.habit_management.get_current_user")
@patch("builtins.input", return_value="0")
def test_longest_run_streak_first_habit(mock_input, mock_get_current_user, mock_get_completions, mock_get_habit, user,
                                          create_habits):
    id=1
    # Mock the current user
    mock_get_current_user.return_value = user


    completions = create_habit_completion(user, create_habits)

    mock_get_completions.return_value = completions[id]

    longest_streak = get_longest_run_streak_of_habit()


    # Assertions
    assert longest_streak == 4
    
    

# Test getting the longest run streak second habit
@patch("DataBase.habit.Habit.get")
@patch("DataBase.habit_completion.HabitCompletion.get")
@patch("Services.habit_management.get_current_user")
@patch("builtins.input", return_value="1")
def test_longest_run_streak_second_habit(mock_input, mock_get_current_user, mock_get_completions, mock_get_habit, user,
                                          create_habits):
    id=2
    # Mock the current user
    mock_get_current_user.return_value = user


    completions = create_habit_completion(user, create_habits)

    mock_get_completions.return_value = completions[id]

    longest_streak = get_longest_run_streak_of_habit()


    # Assertions
    assert longest_streak == 2

# Test getting the longest run streak third habit
@patch("DataBase.habit.Habit.get")
@patch("DataBase.habit_completion.HabitCompletion.get")
@patch("Services.habit_management.get_current_user")
@patch("builtins.input", return_value="2")
def test_longest_run_streak_third_habit(mock_input, mock_get_current_user, mock_get_completions, mock_get_habit, user,
                                          create_habits):
    id=3
    # Mock the current user
    mock_get_current_user.return_value = user


    completions = create_habit_completion(user, create_habits)

    mock_get_completions.return_value = completions[id]


    longest_streak = get_longest_run_streak_of_habit()


    # Assertions
    assert longest_streak == 6


# Test getting the longest run streak fourth habit
@patch("DataBase.habit.Habit.get")
@patch("DataBase.habit_completion.HabitCompletion.get")
@patch("Services.habit_management.get_current_user")
@patch("builtins.input", return_value="3")
def test_longest_run_streak_fourth_habit(mock_input, mock_get_current_user, mock_get_completions, mock_get_habit, user,
                                          create_habits):
    id=4
    # Mock the current user
    mock_get_current_user.return_value = user

    completions = create_habit_completion(user, create_habits)

    mock_get_completions.return_value = completions[id]

    longest_streak = get_longest_run_streak_of_habit()

    # Assertions
    assert longest_streak == 4

# Test getting the longest run streak fiveth habit
@patch("DataBase.habit.Habit.get")
@patch("DataBase.habit_completion.HabitCompletion.get")
@patch("Services.habit_management.get_current_user")
@patch("builtins.input", return_value="4")
def test_longest_run_streak_fiveth_habit(mock_input, mock_get_current_user, mock_get_completions, mock_get_habit, user,
                                          create_habits):
    id=5
    # Mock the current user
    mock_get_current_user.return_value = user

    completions = create_habit_completion(user, create_habits)

    mock_get_completions.return_value = completions[id]

    longest_streak = get_longest_run_streak_of_habit()

    # Assertions
    assert longest_streak == 16 