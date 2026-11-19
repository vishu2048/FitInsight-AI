from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QPushButton,
    QMessageBox,
)

from database import get_latest_daily_log
from services.prediction import predict_weight


class PredictionPage(QWidget):

    def __init__(self):
        super().__init__()

        self.create_ui()
        self.load_latest_data()

    def create_ui(self):

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            40, 35, 40, 35
        )

        main_layout.setSpacing(20)

        # ==============================
        # PAGE HEADER
        # ==============================

        title = QLabel("ML Weight Prediction")
        title.setObjectName("page_title")

        description = QLabel(
            "Use your latest fitness data to predict your future weight."
        )
        description.setObjectName("description")

        main_layout.addWidget(title)
        main_layout.addWidget(description)

        # ==============================
        # DATA CARD
        # ==============================

        data_card = QFrame()
        data_card.setObjectName("card")

        data_layout = QVBoxLayout(data_card)

        data_title = QLabel(
            "Latest Fitness Data"
        )
        data_title.setObjectName("card_title")

        self.data_label = QLabel(
            "Loading data..."
        )
        self.data_label.setObjectName("card_text")
        self.data_label.setWordWrap(True)

        data_layout.addWidget(data_title)
        data_layout.addWidget(self.data_label)

        main_layout.addWidget(data_card)

        # ==============================
        # PREDICTION BUTTON
        # ==============================

        self.predict_button = QPushButton(
            "Predict Future Weight"
        )

        self.predict_button.setObjectName(
            "primary_button"
        )

        self.predict_button.clicked.connect(
            self.make_prediction
        )

        main_layout.addWidget(
            self.predict_button
        )

        # ==============================
        # RESULT CARD
        # ==============================

        result_card = QFrame()
        result_card.setObjectName("card")

        result_layout = QVBoxLayout(result_card)

        result_title = QLabel(
            "Prediction Result"
        )
        result_title.setObjectName("card_title")

        self.result_label = QLabel(
            "Click the button to generate a prediction."
        )

        self.result_label.setObjectName(
            "prediction_result"
        )

        self.result_label.setWordWrap(True)

        result_layout.addWidget(
            result_title
        )

        result_layout.addWidget(
            self.result_label
        )

        main_layout.addWidget(
            result_card
        )

        # ==============================
        # MODEL INFORMATION
        # ==============================

        model_card = QFrame()
        model_card.setObjectName("card")

        model_layout = QVBoxLayout(model_card)

        model_title = QLabel(
            "About the ML Model"
        )
        model_title.setObjectName("card_title")

        model_info = QLabel(
            "Algorithm: Random Forest Regression\n"
            "Framework: scikit-learn\n"
            "Model persistence: Joblib\n"
            "Input: Fitness and lifestyle features\n"
            "Output: Predicted future weight"
        )

        model_info.setObjectName(
            "card_text"
        )

        model_info.setWordWrap(True)

        model_layout.addWidget(
            model_title
        )

        model_layout.addWidget(
            model_info
        )

        main_layout.addWidget(
            model_card
        )

        main_layout.addStretch()

    def load_latest_data(self):

        log = get_latest_daily_log(1)

        if not log:

            self.data_label.setText(
                "No daily check-in data available.\n\n"
                "Please complete a Daily Check-in first."
            )

            self.predict_button.setEnabled(
                False
            )

            return

        self.latest_log = log

        self.data_label.setText(
            f"Date: {log['date']}\n"
            f"Weight: {log['weight']} kg\n"
            f"Steps: {log['steps']}\n"
            f"Sleep: {log['sleep_duration']} hours\n"
            f"Workout: {log['workout_duration']} minutes\n"
            f"Calories burned: {log['calories_burned']}\n"
            f"Calories consumed: {log['calories_consumed']}\n"
            f"Water intake: {log['water_intake']} L"
        )

    def make_prediction(self):

        if not hasattr(self, "latest_log"):

            QMessageBox.warning(
                self,
                "No Data",
                "Please complete a Daily Check-in first."
            )

            return

        log = self.latest_log

        try:

            predicted_weight = predict_weight(
                weight=log["weight"],
                steps=log["steps"],
                sleep_duration=log["sleep_duration"],
                workout_duration=log["workout_duration"],
                calories_burned=log["calories_burned"],
                calories_consumed=log["calories_consumed"],
                water_intake=log["water_intake"]
            )

            current_weight = log["weight"]

            difference = (
                predicted_weight -
                current_weight
            )

            if difference < 0:

                trend = (
                    f"Predicted decrease of "
                    f"{abs(difference):.2f} kg."
                )

            elif difference > 0:

                trend = (
                    f"Predicted increase of "
                    f"{difference:.2f} kg."
                )

            else:

                trend = (
                    "Predicted weight remains "
                    "approximately stable."
                )

            self.result_label.setText(
                f"Predicted Future Weight\n\n"
                f"{predicted_weight:.2f} kg\n\n"
                f"{trend}\n\n"
                f"This prediction is generated by "
                f"the local Random Forest model."
            )

        except Exception as error:

            QMessageBox.critical(
                self,
                "Prediction Error",
                str(error)
            )

    def refresh_data(self):

        self.load_latest_data()

        self.result_label.setText(
            "Click the button to generate a prediction."
        )