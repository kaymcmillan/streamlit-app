# College Student Budget Tracker

## Student Name
Kaylie

## App Description
This app helps college students build a monthly budget around the expenses they personally pay for and see their whole financial picture in one place. Students start by entering their income and any savings they are willing to spend, then choose which expenses they are responsible for (rent, groceries, and so on) or type in their own. They can track each purchase under the matching budget and see how much money is left in every category. The app also includes a savings goal tool for big purchases like a spring break trip.

## Intended Users
This app is intended for college students who are managing their own money for the first time, including students whose parents cover some bills and students who pay for everything themselves.

## Current Features (Implemented)
- Choose which month to budget for
- Income questions: whether the student earns money during the school year, how much per month, and optional income from financial aid, family, or summer earnings
- Option to include savings the student is willing to spend
- Students choose only the expenses they are responsible for from a list (rent, utilities, groceries, transportation/gas, textbooks, phone, subscriptions, eating out, going out, student loans, health costs, travel home)
- Option to type in a custom expense that is not on the list
- Monthly budget amount for each selected expense (all values start at $0)
- Expense tracker: log a purchase, assign it to a budget, and see the money left in each category with progress bars
- Delete option for expenses entered by mistake
- Savings goal tool with total cost, amount saved so far, target date, the monthly amount needed, and a progress bar
- Monthly summary showing money available, total budgeted, money not yet assigned, and budget vs. actual spending in a chart and table
- Recommendation messages that change based on the student's numbers (over-planned, over budget in a category, or on track)

## Planned Features (Final Version)
- Save data between sessions so budgets and expenses are not lost when the page is refreshed
- Emergency fund check showing whether savings could cover about 3 months of expenses
- Month-to-month history to compare spending over time
- Recurring bill reminders with due dates
- Semester view that totals the budget across several months
- Option to download the monthly summary as a file

## How to Run
```
pip install -r requirements.txt
streamlit run app.py
```
