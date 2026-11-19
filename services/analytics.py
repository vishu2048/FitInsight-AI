
from datetime import date, timedelta

from database import get_daily_logs


# =========================================================
# GET CHECK-INS FROM LAST 7 CALENDAR DAYS
# =========================================================

def get_last_7_days(user_id=1):

    today = date.today()
    start_date = today - timedelta(days=6)

    logs = get_daily_logs(user_id)

    filtered_logs = []

    for log in logs:

        try:
            log_date = date.fromisoformat(log["date"])

            if start_date <= log_date <= today:
                filtered_logs.append(log)

        except (ValueError, TypeError):
            continue

    return filtered_logs


# =========================================================
# CALCULATE AVERAGE
# =========================================================

def calculate_average(values):

    valid_values = [
        value for value in values
        if value is not None
    ]

    if not valid_values:
        return 0

    return sum(valid_values) / len(valid_values)


# =========================================================
# GET ANALYTICS SUMMARY
# =========================================================

def get_analytics_summary(user_id=1):

    logs = get_last_7_days(user_id)

    if not logs:
        return {
            "days": 0,
            "average_weight": 0,
            "average_steps": 0,
            "average_sleep": 0,
            "average_workout": 0,
            "weight_change": 0,
            "starting_weight": None,
            "latest_weight": None,
        }

    weights = [
        log["weight"]
        for log in logs
        if log["weight"] is not None
    ]

    steps = [
        log["steps"]
        for log in logs
        if log["steps"] is not None
    ]

    sleep = [
        log["sleep_duration"]
        for log in logs
        if log["sleep_duration"] is not None
    ]

    workouts = [
        log["workout_duration"]
        for log in logs
        if log["workout_duration"] is not None
    ]

    starting_weight = weights[0] if weights else None
    latest_weight = weights[-1] if weights else None

    weight_change = (
        latest_weight - starting_weight
        if len(weights) >= 2 else 0
    )

    return {
        "days": len(logs),
        "average_weight": calculate_average(weights),
        "average_steps": calculate_average(steps),
        "average_sleep": calculate_average(sleep),
        "average_workout": calculate_average(workouts),
        "weight_change": weight_change,
        "starting_weight": starting_weight,
        "latest_weight": latest_weight,
    }


# =========================================================
# GET WEIGHT PROGRESS
# =========================================================

def get_weight_progress(user_id=1):

    logs = get_last_7_days(user_id)

    weight_logs = [
        log for log in logs
        if log["weight"] is not None
    ]

    if not weight_logs:
        return {
            "records": 0,
            "starting_weight": None,
            "latest_weight": None,
            "change": None,
        }

    starting_weight = weight_logs[0]["weight"]
    latest_weight = weight_logs[-1]["weight"]

    return {
        "records": len(weight_logs),
        "starting_weight": starting_weight,
        "latest_weight": latest_weight,
        "change": latest_weight - starting_weight,
    }
