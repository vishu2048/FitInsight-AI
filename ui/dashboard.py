
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
)

from database import (
    get_user,
    get_latest_daily_log,
)

from services.prediction import predict_weight


class DashboardPage(QWidget):

    def __init__(self):
        super().__init__()

        self.create_ui()
        self.load_data()

    # ==========================================
    # CREATE DASHBOARD UI
    # ==========================================

    def create_ui(self):

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            35, 30, 35, 30
        )
        main_layout.setSpacing(20)

        # Page heading
        title = QLabel("Dashboard")
        title.setObjectName("page_title")

        description = QLabel(
            "Track your fitness, monitor your progress, "
            "and explore your AI-powered insights."
        )
        description.setObjectName("description")
        description.setWordWrap(True)

        main_layout.addWidget(title)
        main_layout.addWidget(description)

        # ======================================
        # STATISTIC CARDS
        # ======================================

        stats_layout = QHBoxLayout()
        stats_layout.setSpacing(15)

        self.weight_card, self.weight_value = (
            self.create_stat_card("Current Weight", "-- kg")
        )

        self.steps_card, self.steps_value = (
            self.create_stat_card("Daily Steps", "--")
        )

        self.sleep_card, self.sleep_value = (
            self.create_stat_card("Sleep Duration", "-- hrs")
        )

        self.calories_card, self.calories_value = (
            self.create_stat_card("Calories Burned", "-- kcal")
        )

        stats_layout.addWidget(self.weight_card)
        stats_layout.addWidget(self.steps_card)
        stats_layout.addWidget(self.sleep_card)
        stats_layout.addWidget(self.calories_card)

        main_layout.addLayout(stats_layout)

        # ======================================
        # PROFILE AND FITNESS SCORE
        # ======================================

        info_layout = QHBoxLayout()
        info_layout.setSpacing(15)

        profile_card = QFrame()
        profile_card.setObjectName("card")

        profile_layout = QVBoxLayout(profile_card)
        profile_layout.setContentsMargins(22, 20, 22, 20)
        profile_layout.setSpacing(12)

        profile_title = QLabel("Profile Overview")
        profile_title.setObjectName("card_title")

        self.profile_label = QLabel(
            "Complete your profile to get started."
        )
        self.profile_label.setObjectName("card_text")
        self.profile_label.setWordWrap(True)

        profile_layout.addWidget(profile_title)
        profile_layout.addWidget(self.profile_label)

        score_card = QFrame()
        score_card.setObjectName("card")

        score_layout = QVBoxLayout(score_card)
        score_layout.setContentsMargins(22, 20, 22, 20)
        score_layout.setSpacing(12)

        score_title = QLabel("Daily Fitness Score")
        score_title.setObjectName("card_title")

        self.score_value = QLabel("-- / 100")
        self.score_value.setObjectName("fitness_score")

        self.score_description = QLabel(
            "Complete a daily check-in to calculate your score."
        )
        self.score_description.setObjectName("card_text")
        self.score_description.setWordWrap(True)

        score_layout.addWidget(score_title)
        score_layout.addWidget(self.score_value)
        score_layout.addWidget(self.score_description)

        info_layout.addWidget(profile_card, 3)
        info_layout.addWidget(score_card, 2)

        main_layout.addLayout(info_layout)

        # ======================================
        # RULE-BASED AI INSIGHTS
        # ======================================

        insight_card = QFrame()
        insight_card.setObjectName("card")

        insight_layout = QVBoxLayout(insight_card)
        insight_layout.setContentsMargins(22, 20, 22, 20)
        insight_layout.setSpacing(12)

        insight_title = QLabel("AI Fitness Insights")
        insight_title.setObjectName("card_title")

        self.insight_label = QLabel(
            "Your personalized insights will appear here."
        )
        self.insight_label.setObjectName("card_text")
        self.insight_label.setWordWrap(True)

        insight_layout.addWidget(insight_title)
        insight_layout.addWidget(self.insight_label)

        main_layout.addWidget(insight_card)

        # ======================================
        # ML PREDICTION CARD
        # ======================================

        prediction_card = QFrame()
        prediction_card.setObjectName("card")

        prediction_layout = QVBoxLayout(prediction_card)
        prediction_layout.setContentsMargins(22, 20, 22, 20)
        prediction_layout.setSpacing(12)

        prediction_title = QLabel(
            "Machine Learning Weight Prediction"
        )
        prediction_title.setObjectName("card_title")

        self.prediction_label = QLabel(
            "Prediction will appear when fitness data is available."
        )
        self.prediction_label.setObjectName("card_text")
        self.prediction_label.setWordWrap(True)

        prediction_layout.addWidget(prediction_title)
        prediction_layout.addWidget(self.prediction_label)

        main_layout.addWidget(prediction_card)

        main_layout.addStretch()

    # ==========================================
    # CREATE STATISTIC CARD
    # ==========================================

    def create_stat_card(self, title, value):

        card = QFrame()
        card.setObjectName("card")

        layout = QVBoxLayout(card)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        title_label = QLabel(title)
        title_label.setObjectName("card_text")
        title_label.setWordWrap(True)

        value_label = QLabel(value)
        value_label.setObjectName("stat_value")

        layout.addWidget(title_label)
        layout.addWidget(value_label)

        return card, value_label

    # ==========================================
    # LOAD DASHBOARD DATA
    # ==========================================

    def load_data(self):

        user = get_user(1)
        log = get_latest_daily_log(1)

        self.load_profile(user)

        if log is None:

            self.weight_value.setText("-- kg")
            self.steps_value.setText("--")
            self.sleep_value.setText("-- hrs")
            self.calories_value.setText("-- kcal")

            self.score_value.setText("-- / 100")

            self.score_description.setText(
                "Complete a daily check-in to calculate your score."
            )

            self.insight_label.setText(
                "No daily check-in found. Start tracking your "
                "steps, sleep, workouts and water intake."
            )

            self.prediction_label.setText(
                "No daily fitness data available. "
                "Complete a check-in to generate a prediction."
            )

            return

        # Statistic values
        weight = log["weight"]
        steps = log["steps"]
        sleep = log["sleep_duration"]
        calories = log["calories_burned"]

        self.weight_value.setText(
            f"{weight:.1f} kg" if weight is not None else "-- kg"
        )

        self.steps_value.setText(
            f"{steps:,}" if steps is not None else "--"
        )

        self.sleep_value.setText(
            f"{sleep:.1f} hrs" if sleep is not None else "-- hrs"
        )

        self.calories_value.setText(
            f"{calories:.0f} kcal"
            if calories is not None
            else "-- kcal"
        )

        # Fitness score
        score = self.calculate_fitness_score(log)

        self.score_value.setText(f"{score} / 100")

        if score >= 80:
            score_message = (
                "Strong daily fitness indicators. "
                "Keep maintaining consistent habits."
            )
        elif score >= 60:
            score_message = (
                "Good progress. A few consistent improvements may help."
            )
        else:
            score_message = (
                "Focus on building sustainable movement, sleep "
                "and hydration habits."
            )

        self.score_description.setText(score_message)

        # Rule-based insights
        insights = self.generate_insights(log)

        self.insight_label.setText(
            "\n".join(f"• {item}" for item in insights)
        )

        # ML prediction
        self.update_prediction(log)

    # ==========================================
    # LOAD PROFILE INFORMATION
    # ==========================================

    def load_profile(self, user):

        if user is None:
            self.profile_label.setText(
                "No profile found. Open Profile and save your details."
            )
            return

        name = user["name"] or "User"
        age = user["age"]
        gender = user["gender"] or "Not specified"
        height = user["height"]
        goal = user["goal"] or "Not specified"
        target_weight = user["target_weight"]

        age_text = (
            str(age) if age is not None else "Not specified"
        )

        height_text = (
            f"{height:.1f} cm"
            if height is not None
            else "Not specified"
        )

        target_text = (
            f"{target_weight:.1f} kg"
            if target_weight is not None
            else "Not specified"
        )

        self.profile_label.setText(
            f"Name: {name}\n"
            f"Age: {age_text}\n"
            f"Gender: {gender}\n"
            f"Height: {height_text}\n"
            f"Fitness Goal: {goal}\n"
            f"Target Weight: {target_text}"
        )

    # ==========================================
    # FITNESS SCORE
    # ==========================================

    def calculate_fitness_score(self, log):

        score = 0

        steps = log["steps"]
        sleep = log["sleep_duration"]
        workout = log["workout_duration"]
        water = log["water_intake"]

        # Steps: maximum 30
        if steps is not None:
            if steps >= 10000:
                score += 30
            elif steps >= 7500:
                score += 25
            elif steps >= 5000:
                score += 18
            else:
                score += 10

        # Sleep: maximum 25
        if sleep is not None:
            if 7 <= sleep <= 9:
                score += 25
            elif sleep >= 6:
                score += 18
            else:
                score += 10

        # Workout: maximum 25
        if workout is not None:
            if workout >= 45:
                score += 25
            elif workout >= 30:
                score += 20
            elif workout >= 15:
                score += 12
            else:
                score += 5

        # Water: maximum 20
        if water is not None:
            if water >= 3:
                score += 20
            elif water >= 2:
                score += 15
            elif water >= 1:
                score += 10
            else:
                score += 5

        return score

    # ==========================================
    # RULE-BASED AI INSIGHTS
    # ==========================================

    def generate_insights(self, log):

        insights = []

        steps = log["steps"]
        sleep = log["sleep_duration"]
        workout = log["workout_duration"]
        water = log["water_intake"]

        if steps is not None:
            if steps < 5000:
                insights.append(
                    "Try gradually increasing your daily steps."
                )
            elif steps >= 10000:
                insights.append(
                    "Excellent step count. Keep moving consistently."
                )

        if sleep is not None:
            if sleep < 7:
                insights.append(
                    "Consider aiming for 7–9 hours of sleep."
                )
            elif sleep <= 9:
                insights.append(
                    "Your recorded sleep duration is within "
                    "the recommended adult range."
                )

        if workout is not None:
            if workout < 30:
                insights.append(
                    "Consider gradually adding activity to your routine."
                )
            else:
                insights.append(
                    "Keep maintaining a consistent workout routine."
                )

        if water is not None:
            if water < 2:
                insights.append(
                    "Review your hydration and drink water regularly."
                )
            else:
                insights.append(
                    "Keep monitoring hydration alongside your activity."
                )

        if not insights:
            insights.append(
                "Record more complete fitness data for personalized insights."
            )

        insights.append(
            "These are rule-based suggestions, not a medical assessment."
        )

        return insights

    # ==========================================
    # UPDATE ML PREDICTION CARD
    # ==========================================

    def update_prediction(self, log):

        weight = log["weight"]

        if weight is None:
            self.prediction_label.setText(
                "A recorded weight is required for prediction."
            )
            return

        try:

            predicted_weight = predict_weight(
                weight=weight,
                steps=log["steps"] or 0,
                sleep_duration=log["sleep_duration"] or 0,
                workout_duration=log["workout_duration"] or 0,
                calories_burned=log["calories_burned"] or 0,
                calories_consumed=log["calories_consumed"] or 0,
                water_intake=log["water_intake"] or 0,
            )

            difference = predicted_weight - weight

            if difference < -0.005:
                trend = (
                    f"Model estimate is {abs(difference):.2f} kg "
                    "below the recorded weight."
                )
            elif difference > 0.005:
                trend = (
                    f"Model estimate is {difference:.2f} kg "
                    "above the recorded weight."
                )
            else:
                trend = (
                    "Model estimate is approximately equal "
                    "to the recorded weight."
                )

            self.prediction_label.setText(
                f"Latest recorded weight: {weight:.1f} kg\n"
                f"Model-estimated weight: {predicted_weight:.2f} kg\n"
                f"{trend}\n\n"
                "Experimental estimate based on a model trained "
                "on synthetic data. It is not a validated forecast."
            )

        except Exception as error:

            self.prediction_label.setText(
                f"Prediction unavailable: {error}"
            )

    # ==========================================
    # REFRESH DASHBOARD
    # ==========================================

    def refresh_data(self):
        self.load_data()
