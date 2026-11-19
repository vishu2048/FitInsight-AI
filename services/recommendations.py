def generate_recommendations(summary):

    recommendations = []

    average_steps = summary["average_steps"]
    average_sleep = summary["average_sleep"]
    average_workout = summary["average_workout"]
    weight_change = summary["weight_change"]

    # ---------------------------------------------------------
    # STEPS
    # ---------------------------------------------------------

    if average_steps < 5000:

        recommendations.append(
            "Try gradually increasing your daily steps."
        )

    elif average_steps < 8000:

        recommendations.append(
            "Your activity is moderate. "
            "Try moving toward 8,000+ steps per day."
        )

    else:

        recommendations.append(
            "Your average daily activity is strong. "
            "Keep maintaining it."
        )

    # ---------------------------------------------------------
    # SLEEP
    # ---------------------------------------------------------

    if average_sleep < 6:

        recommendations.append(
            "Your average sleep is low. "
            "Try creating a more consistent sleep schedule."
        )

    elif average_sleep < 7:

        recommendations.append(
            "Try increasing your average sleep toward "
            "7 or more hours."
        )

    else:

        recommendations.append(
            "Your average sleep duration is good. "
            "Keep it consistent."
        )

    # ---------------------------------------------------------
    # WORKOUT
    # ---------------------------------------------------------

    if average_workout < 20:

        recommendations.append(
            "Consider adding regular workout sessions "
            "to your weekly routine."
        )

    elif average_workout < 40:

        recommendations.append(
            "Your workouts are consistent. "
            "Gradually increasing duration may help."
        )

    else:

        recommendations.append(
            "Your workout activity is consistent. "
            "Keep following your routine."
        )

    # ---------------------------------------------------------
    # WEIGHT
    # ---------------------------------------------------------

    if weight_change < 0:

        recommendations.append(
            "Your recorded weight has decreased "
            "over this period."
        )

    elif weight_change > 0:

        recommendations.append(
            "Your recorded weight has increased "
            "over this period. Review your activity "
            "and nutrition trends."
        )

    else:

        recommendations.append(
            "Your recorded weight has remained relatively stable."
        )

    return recommendations