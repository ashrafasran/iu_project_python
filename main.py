
from DataBase.database import DATABASE

from Services.analysis import run_analysis
from Services.auth import login, register, get_current_user,logout
from Services.habit_management import run_habit_management
from Services.profile_management import run_profile_management

welcome_prompt="""
--Welcome to our habit tracking app, i wish you are good.--
    press 1 to register
    press 2 to login
    press 3 to logout
    press 0 to exit
    please enter you choice:
"""

db=DATABASE()


if __name__ == "__main__":

        while (user_input := input(welcome_prompt)) != "0":
            try:
                match user_input:
                    case "1":
                        if not register():
                            continue
                    case "2":
                        if not login():
                            continue
                    case "3":
                        logout()
                        continue
                while get_current_user() and (user_input := input(
                        f"""
--Welcome to our menu, {get_current_user().name}--
    press 1 to habit management
    press 2 to habit analysis
    press 3 to profile management
    press 0 to go back
    please enter you choice:
"""
                )) != "0" :
                    match user_input:
                        case "1":
                            run_habit_management()
                        case "2":
                            run_analysis()
                        case "3":
                            run_profile_management()
            except Exception as e:
                print(f"{e}")
        logout()

