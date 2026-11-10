import calendar
import datetime

import pandas as pd
import streamlit as st

st.set_page_config(page_title="College Student Budget Tracker", page_icon="💰")

# ---------- Options students can choose from ----------
STANDARD_EXPENSES = [
    "Rent",
    "Utilities",
    "Groceries",
    "Transportation / Gas",
    "Textbooks and school supplies",
    "Phone bill",
    "Subscriptions (Spotify, Netflix, etc.)",
    "Eating out and coffee",
    "Going out and social activities",
    "Student loan payments",
    "Health costs (insurance, prescriptions, copays)",
    "Travel home for breaks",
]

OTHER_INCOME_SOURCES = [
    "Financial aid / scholarship money paid to me",
    "Money from parents or family",
    "Summer job earnings spread across the year",
]

MONTHS = list(calendar.month_name)[1:]


# ---------- Helper functions ----------
def money(amount):
    """Format a number as dollars, e.g. $1,250.00 or -$40.00."""
    sign = "-" if amount < 0 else ""
    return f"{sign}${abs(amount):,.2f}"


def add_custom_expense():
    """Button callback: add a student-typed expense and select it automatically."""
    name = st.session_state.custom_expense_input.strip()
    if not name:
        return
    existing = [e.lower() for e in STANDARD_EXPENSES + st.session_state.custom_expenses]
    if name.lower() not in existing:
        st.session_state.custom_expenses.append(name)
    if name not in st.session_state.selected_expenses:
        st.session_state.selected_expenses.append(name)
    st.session_state.custom_expense_input = ""


# ---------- Saved data for this session ----------
st.session_state.setdefault("transactions", [])
st.session_state.setdefault("custom_expenses", [])
st.session_state.setdefault("selected_expenses", [])

# ---------- Page header ----------
st.title("College Student Budget Tracker")
st.write(
    "Build a budget around the things *you* are responsible for paying, "
    "track your spending, and save toward something big. "
    "Start with step 1 and work through the tabs."
)

today = datetime.date.today()
month_name = st.selectbox(
    "Which month are you budgeting for?", MONTHS, index=today.month - 1
)
month_number = MONTHS.index(month_name) + 1
month_key = f"{today.year}-{month_number:02d}"

tab_setup, tab_track, tab_summary = st.tabs(
    ["1. Set up your budget", "2. Track expenses", "3. Monthly summary"]
)

# =====================================================================
# TAB 1: SET UP
# =====================================================================
with tab_setup:
    # ----- Income -----
    st.header("Your income")

    earns_money = st.radio(
        "Do you earn money during the school year (job, work-study, etc.)?",
        ["Yes", "No"],
        index=None,
        horizontal=True,
    )
    job_income = 0.0
    if earns_money == "Yes":
        job_income = st.number_input(
            "About how much do you earn per month? ($)",
            min_value=0.0, value=0.0, step=25.0, format="%.2f",
        )

    income_sources = st.multiselect(
        "Do you get money from any of these other sources? (pick all that apply)",
        OTHER_INCOME_SOURCES,
    )
    other_income = 0.0
    for source in income_sources:
        other_income += st.number_input(
            f"{source}: amount per month ($)",
            min_value=0.0, value=0.0, step=25.0, format="%.2f",
            key=f"income_{source}",
        )

    # ----- Savings to spend -----
    has_savings = st.radio(
        "Do you have money saved up that you're willing to spend from?",
        ["Yes", "No"],
        index=None,
        horizontal=True,
    )
    savings_to_spend = 0.0
    if has_savings == "Yes":
        savings_to_spend = st.number_input(
            f"How much of your savings do you want to use in {month_name}? ($)",
            min_value=0.0, value=0.0, step=25.0, format="%.2f",
        )

    # ----- Expenses -----
    st.header("What are you responsible for paying?")
    st.caption(
        "Only pick the things you pay for yourself. If a parent covers your rent, "
        "for example, leave it unchecked."
    )

    selected_expenses = st.multiselect(
        "Choose your expenses",
        STANDARD_EXPENSES + st.session_state.custom_expenses,
        key="selected_expenses",
    )

    col_text, col_button = st.columns([3, 1], vertical_alignment="bottom")
    with col_text:
        st.text_input(
            "Something not on the list? Type it here (for example: Pet care)",
            key="custom_expense_input",
        )
    with col_button:
        st.button("Add to my list", on_click=add_custom_expense)

    budgets = {}
    if selected_expenses:
        st.subheader(f"Your {month_name} budget for each expense")
        for expense in selected_expenses:
            budgets[expense] = st.number_input(
                f"{expense}: how much do you plan to spend? ($)",
                min_value=0.0, value=0.0, step=10.0, format="%.2f",
                key=f"budget_{expense}",
            )
    else:
        st.info("Pick at least one expense above to start building your budget.")

    # ----- Savings goal -----
    st.header("Saving for something big?")
    has_goal = st.checkbox("Yes, I'm saving toward a goal")

    goal_name, goal_cost, goal_saved = "", 0.0, 0.0
    goal_contribution, goal_monthly_needed = 0.0, 0.0
    if has_goal:
        goal_name = st.text_input("What are you saving for?", placeholder="Spring break trip")
        goal_cost = st.number_input(
            "How much does it cost in total? ($)",
            min_value=0.0, value=0.0, step=50.0, format="%.2f",
        )
        goal_saved = st.number_input(
            "How much have you already saved toward it? ($)",
            min_value=0.0, value=0.0, step=50.0, format="%.2f",
        )
        goal_date = st.date_input(
            "When do you need the money by?",
            value=today + datetime.timedelta(days=90),
            min_value=today,
        )

        months_left = max(
            1, (goal_date.year - today.year) * 12 + goal_date.month - today.month
        )
        still_needed = max(goal_cost - goal_saved, 0.0)
        goal_monthly_needed = still_needed / months_left

        if goal_cost > 0:
            st.write(
                f"You still need **{money(still_needed)}** and have about "
                f"**{months_left} month(s)** left. To get there on time, "
                f"set aside about **{money(goal_monthly_needed)} per month**."
            )
        goal_contribution = st.number_input(
            f"How much will you put toward this goal in {month_name}? ($)",
            min_value=0.0, value=0.0, step=10.0, format="%.2f",
        )

# ---------- Calculations used by the other tabs ----------
total_income = job_income + other_income
money_available = total_income + savings_to_spend
total_budgeted = sum(budgets.values()) + goal_contribution
unassigned = money_available - total_budgeted

month_transactions = [
    t for t in st.session_state.transactions if t["Month"] == month_key
]
spent = {name: 0.0 for name in budgets}
for t in month_transactions:
    if t["Category"] in spent:
        spent[t["Category"]] += t["Amount"]
total_spent = sum(spent.values())

# =====================================================================
# TAB 2: TRACK EXPENSES
# =====================================================================
with tab_track:
    st.header(f"Money left in each budget ({month_name})")

    if not budgets:
        st.info("Go to step 1 and choose your expenses first. They will show up here.")
    else:
        columns = st.columns(2)
        for i, (name, budget) in enumerate(budgets.items()):
            left = budget - spent[name]
            with columns[i % 2].container(border=True):
                st.markdown(f"**{name}**")
                st.metric(
                    "Left to spend",
                    money(left),
                    delta=f"{money(spent[name])} spent of {money(budget)}",
                    delta_color="off",
                )
                if budget > 0:
                    st.progress(min(spent[name] / budget, 1.0))
                if left < 0:
                    st.error(f"Over budget by {money(abs(left))}")

        # ----- Add a transaction -----
        st.header("Add an expense")
        month_start = datetime.date(today.year, month_number, 1)
        month_end = datetime.date(
            today.year, month_number, calendar.monthrange(today.year, month_number)[1]
        )
        default_date = today if month_start <= today <= month_end else month_start

        with st.form("expense_form", clear_on_submit=True):
            category = st.selectbox("Which budget does this belong to?", list(budgets))
            amount = st.number_input(
                "Amount spent ($)", min_value=0.0, value=0.0, step=1.0, format="%.2f"
            )
            date = st.date_input(
                "Date", value=default_date, min_value=month_start, max_value=month_end
            )
            note = st.text_input("Note (optional)", placeholder="Trader Joe's run")
            submitted = st.form_submit_button("Add expense")

        if submitted:
            if amount <= 0:
                st.warning("Enter an amount greater than $0.")
            else:
                st.session_state.transactions.append(
                    {"Month": month_key, "Date": date, "Category": category,
                     "Amount": amount, "Note": note}
                )
                st.rerun()

        # ----- Transaction list -----
        st.header(f"Your {month_name} expenses")
        if month_transactions:
            table = pd.DataFrame(month_transactions).drop(columns="Month")
            table = table.sort_values("Date").reset_index(drop=True)
            st.dataframe(table, width="stretch", hide_index=True)

            with st.expander("Made a mistake? Delete an expense"):
                all_transactions = st.session_state.transactions
                options = [
                    i for i, t in enumerate(all_transactions) if t["Month"] == month_key
                ]
                to_delete = st.selectbox(
                    "Choose the expense to delete",
                    options,
                    format_func=lambda i: (
                        f"{all_transactions[i]['Date']} | {all_transactions[i]['Category']} | "
                        f"{money(all_transactions[i]['Amount'])} {all_transactions[i]['Note']}"
                    ),
                )
                if st.button("Delete this expense"):
                    all_transactions.pop(to_delete)
                    st.rerun()
        else:
            st.write("No expenses added for this month yet.")

# =====================================================================
# TAB 3: MONTHLY SUMMARY
# =====================================================================
with tab_summary:
    st.header(f"Your {month_name} money picture")

    if money_available == 0 and not budgets:
        st.info("Finish step 1 (income and expenses) to see your summary.")
    else:
        c1, c2, c3 = st.columns(3)
        c1.metric("Money available", money(money_available))
        c2.metric("Total budgeted", money(total_budgeted))
        c3.metric("Not yet assigned", money(unassigned))

        st.write(
            f"Income: **{money(total_income)}** | "
            f"Savings you're using: **{money(savings_to_spend)}** | "
            f"Spent so far: **{money(total_spent)}**"
        )

        # Recommendation that changes with the student's numbers
        overspent = [name for name in budgets if spent[name] > budgets[name]]
        if unassigned < 0:
            st.error(
                f"You've planned to spend {money(abs(unassigned))} more than you have. "
                "Lower a budget or your goal contribution, or add income."
            )
        elif overspent:
            st.warning("You're over budget in: " + ", ".join(overspent) + ".")
        elif money_available > 0:
            st.success(
                f"You're on track! You have {money(unassigned)} not assigned to anything yet."
            )

        if budgets:
            st.subheader("Budget vs. actual spending")
            summary = pd.DataFrame(
                {
                    "Category": list(budgets),
                    "Budgeted": list(budgets.values()),
                    "Spent": [spent[name] for name in budgets],
                }
            )
            summary["Left"] = summary["Budgeted"] - summary["Spent"]
            st.bar_chart(summary.set_index("Category")[["Budgeted", "Spent"]])
            st.dataframe(summary, width="stretch", hide_index=True)

        if has_goal and goal_cost > 0:
            st.subheader(f"Savings goal: {goal_name or 'My goal'}")
            after_month = goal_saved + goal_contribution
            st.progress(min(after_month / goal_cost, 1.0))
            st.write(
                f"Saved so far: **{money(goal_saved)}**. After this month's contribution: "
                f"**{money(after_month)}** of **{money(goal_cost)}** "
                f"({min(after_month / goal_cost, 1.0) * 100:.0f}%)."
            )
            if goal_contribution < goal_monthly_needed:
                st.info(
                    f"To stay on schedule, aim for {money(goal_monthly_needed)} per month."
                )
