## Habit Tracker Application

### Overview
Welcome to the Habit Tracker Application! This system encourages users to develop healthy habits by allowing them to create, update, delete, and track their habits over time. The application combines object-oriented programming principles with functional programming concepts for an optimized and flexible user experience. The application also supports user registration and login, and all data is stored in an SQLite database.

### Core Features
- **User Authentication**: A secure registration and login system.
- **Data Security**: Secure SQLite database storage.
- **Habit Management**: Ability to create, update, and delete habits.
- **Predefined Habits**: Start quickly with five built-in habit templates.
- **Progress Tracking**: Users can mark a habit as completed.
- **Detailed Analytics**: View habit history with daily and weekly progress tracking, and monitor the longest streak.
- **Testing**: Unit testing is set up for different modules of the application.

### Technologies Used
- **Programming Language**: Python 3.7+
- **Database**: SQLite3
- **Testing**: Pytest

### Requirements
- Python 3.7 or higher
- `pip` package manager

### Project Structure

```sh
habit_tracking_app/
├── DataBase/
│   ├── __init__.py
│   ├── database.py
│   ├── habit.py
│   ├── habit_completion.py
│   └── user.py
├── Services/
│   ├── __init__.py
│   ├── auth.py
│   ├── habit_management.py
│   ├── analysis.py
│   └── profile_management.py
├── Tests/
│   ├── __init__.py
│   ├── test_habit.py
│   ├── test_analysis.py
│   ├── test_habit_completion.py
│   └── test_user.py
└── main.py
```

### Setup and Installation
This project requires Python 3.7+. You can run the program using the Python interpreter in your command line.

1. Clone the repository:  
   ```sh
   git clone https://github.com/ashrafasran/iu_project_python
   ```
2. Find the Python file that serves as the entry point for the program (`main.py` file).
3. Run the `main.py` file using Python by executing the following command:  
   ```sh
   python main.py
   ```

### Usage
#### 1. Create Account
To use the habit tracker, first register and log in with your email and password. Once logged in, you can view, manage, and analyze your habits. The menu provides options for managing habits, running habit analysis, and managing your user profile.

#### 2. Manage Habits
- View your habit schedule
- List all habits and their completions
- Create a new habit
- Update or delete a habit

#### 3. Habit Analysis
- List all tracked habits
- Filter habits by specific periodicity
- Track the longest streak for all habits or a specific habit

#### 4. Testing
Unit tests are available for all major functions. You can run the tests using `pytest` by executing the Python files in the `test` package.

### License
This project is open-source.

### Contributing
You can fork the repository and then create a pull request for me to review and accept your changes.

### Contact
For questions or feedback, contact: [ashraf.asran@googlemail.com](mailto:ashraf.asran@googlemail.com)

### Legal Notice
The Habit Tracker Application was developed as a course project for IU International University. This application is provided "as-is" without any warranties, express or implied. It is intended for personal, non-commercial use only. The developer is not responsible for any loss or damage resulting from the use of this application. By using this software, you agree to assume all associated risks.

