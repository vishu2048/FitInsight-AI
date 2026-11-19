
from datetime import date
from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QFrame,
    QMessageBox,
    QTextEdit,
)

from database import get_connection


class DailyCheckinPage(QWidget):

    # Automatically refresh other pages after successful save
    checkin_saved = Signal()

    def __init__(self):
        super().__init__()
        self.create_ui()

    # =========================================================
    # CREATE UI
    # =========================================================

    def create_ui(self):

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(40, 35, 40, 35)
        main_layout.setSpacing(20)

        title = QLabel("Daily Check-in")
        title.setObjectName("page_title")

        description = QLabel(
            "Record your fitness activity for today."
        )
        description.setObjectName("description")

        main_layout.addWidget(title)
        main_layout.addWidget(description)

        self.date_label = QLabel(
            f"Date: {date.today().strftime('%d %B %Y')}"
        )
        self.date_label.setObjectName("date_label")

        main_layout.addWidget(self.date_label)

        card = QFrame()
        card.setObjectName("card")

        card_layout = QVBoxLayout(card)
        card_layout.setContentsMargins(25, 25, 25, 25)
        card_layout.setSpacing(12)

        self.weight_input = self.create_input(
            card_layout, "Weight (kg)", "Example: 68"
        )

        self.steps_input = self.create_input(
            card_layout, "Steps", "Example: 8000"
        )

        self.sleep_input = self.create_input(
            card_layout, "Sleep Duration (hours)", "Example: 7.5"
        )

        self.workout_input = self.create_input(
            card_layout, "Workout Duration (minutes)", "Example: 45"
        )

        self.calories_burned_input = self.create_input(
            card_layout, "Calories Burned", "Example: 500"
        )

        self.calories_consumed_input = self.create_input(
            card_layout, "Calories Consumed", "Example: 2000"
        )

        self.water_input = self.create_input(
            card_layout, "Water Intake (litres)", "Example: 2.5"
        )

        notes_label = QLabel("Notes")

        self.notes_input = QTextEdit()
        self.notes_input.setPlaceholderText(
            "Write anything about today's workout, "
            "energy level, meals, etc."
        )
        self.notes_input.setMaximumHeight(100)

        card_layout.addWidget(notes_label)
        card_layout.addWidget(self.notes_input)

        self.save_button = QPushButton("Save Today's Check-in")
        self.save_button.setObjectName("primary_button")
        self.save_button.clicked.connect(self.save_checkin)

        card_layout.addWidget(self.save_button)

        main_layout.addWidget(card)
        main_layout.addStretch()

    # =========================================================
    # CREATE INPUT
    # =========================================================

    def create_input(self, layout, label_text, placeholder):

        label = QLabel(label_text)

        input_box = QLineEdit()
        input_box.setPlaceholderText(placeholder)

        layout.addWidget(label)
        layout.addWidget(input_box)

        return input_box

    # =========================================================
    # SAVE CHECK-IN
    # =========================================================

    def save_checkin(self):

        # Get input values
        weight_text = self.weight_input.text().strip()
        steps_text = self.steps_input.text().strip()
        sleep_text = self.sleep_input.text().strip()
        workout_text = self.workout_input.text().strip()
        calories_burned_text = self.calories_burned_input.text().strip()
        calories_consumed_text = self.calories_consumed_input.text().strip()
        water_text = self.water_input.text().strip()
        notes = self.notes_input.toPlainText().strip()

        # Validate required fields
        if not weight_text:
            self.show_error("Please enter your weight.")
            return

        if not steps_text:
            self.show_error("Please enter your steps.")
            return

        if not sleep_text:
            self.show_error("Please enter your sleep duration.")
            return

        # Convert values
        try:
            weight = float(weight_text)
            steps = int(steps_text)
            sleep_duration = float(sleep_text)

            workout_duration = (
                float(workout_text) if workout_text else 0
            )

            calories_burned = (
                float(calories_burned_text)
                if calories_burned_text else 0
            )

            calories_consumed = (
                float(calories_consumed_text)
                if calories_consumed_text else 0
            )

            water_intake = (
                float(water_text) if water_text else 0
            )

        except ValueError:
            self.show_error(
                "Please enter valid numerical values. "
                "Steps must be a whole number."
            )
            return

        # Validate ranges
        if weight <= 0 or weight > 500:
            self.show_error("Please enter a valid weight.")
            return

        if steps < 0:
            self.show_error("Steps cannot be negative.")
            return

        if sleep_duration < 0 or sleep_duration > 24:
            self.show_error(
                "Sleep duration must be between 0 and 24 hours."
            )
            return

        if workout_duration < 0:
            self.show_error("Workout duration cannot be negative.")
            return

        if calories_burned < 0 or calories_consumed < 0:
            self.show_error("Calories cannot be negative.")
            return

        if water_intake < 0:
            self.show_error("Water intake cannot be negative.")
            return

        # Today's date and user ID
        today = date.today().isoformat()
        user_id = 1

        connection = None

        try:
            connection = get_connection()
            cursor = connection.cursor()

            # Check whether today's check-in already exists
            cursor.execute(
                """
                SELECT id
                FROM daily_logs
                WHERE user_id = ? AND date = ?
                LIMIT 1
                """,
                (user_id, today)
            )

            existing_checkin = cursor.fetchone()

            if existing_checkin:
                QMessageBox.warning(
                    self,
                    "Check-in Already Exists",
                    "You have already submitted today's check-in.\n\n"
                    "Only one check-in per day is allowed."
                )
                return

            # Insert new check-in
            cursor.execute(
                """
                INSERT INTO daily_logs (
                    user_id,
                    date,
                    weight,
                    steps,
                    sleep_duration,
                    workout_duration,
                    calories_burned,
                    calories_consumed,
                    water_intake,
                    notes
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    user_id,
                    today,
                    weight,
                    steps,
                    sleep_duration,
                    workout_duration,
                    calories_burned,
                    calories_consumed,
                    water_intake,
                    notes
                )
            )

            connection.commit()

            QMessageBox.information(
                self,
                "Success",
                "Today's check-in was saved successfully!"
            )

            self.clear_form()

            # Refresh dashboard, analytics and prediction pages
            self.checkin_saved.emit()

        except Exception as error:

            if connection:
                connection.rollback()

            QMessageBox.critical(
                self,
                "Database Error",
                f"Could not save your check-in.\n\n{error}"
            )

        finally:
            if connection:
                connection.close()

    # =========================================================
    # ERROR MESSAGE
    # =========================================================

    def show_error(self, message):

        QMessageBox.warning(
            self,
            "Invalid Information",
            message
        )

    # =========================================================
    # CLEAR FORM
    # =========================================================

    def clear_form(self):

        self.weight_input.clear()
        self.steps_input.clear()
        self.sleep_input.clear()
        self.workout_input.clear()
        self.calories_burned_input.clear()
        self.calories_consumed_input.clear()
        self.water_input.clear()
        self.notes_input.clear()
