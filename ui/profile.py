from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QComboBox,
    QPushButton,
    QFrame,
    QMessageBox,
)

from database import add_user, get_user, update_user


class ProfilePage(QWidget):

    def __init__(self):

        super().__init__()

        self.user_id = None

        self.create_ui()

        self.load_user()

    # ==========================================
    # CREATE UI
    # ==========================================

    def create_ui(self):

        main_layout = QVBoxLayout(self)

        main_layout.setContentsMargins(
            40,
            35,
            40,
            35
        )

        main_layout.setSpacing(20)

        # --------------------------------------
        # TITLE
        # --------------------------------------

        title = QLabel("Profile")

        title.setObjectName("page_title")

        description = QLabel(
            "Enter your personal fitness information."
        )

        description.setObjectName("description")

        main_layout.addWidget(title)
        main_layout.addWidget(description)

        # --------------------------------------
        # CARD
        # --------------------------------------

        card = QFrame()

        card.setObjectName("card")

        card_layout = QVBoxLayout(card)

        card_layout.setSpacing(15)

        # --------------------------------------
        # NAME
        # --------------------------------------

        self.name_input = self.create_input(
            card_layout,
            "Full Name"
        )

        # --------------------------------------
        # AGE
        # --------------------------------------

        self.age_input = self.create_input(
            card_layout,
            "Age"
        )

        # --------------------------------------
        # GENDER
        # --------------------------------------

        gender_label = QLabel("Gender")

        self.gender_input = QComboBox()

        self.gender_input.addItems([
            "Select Gender",
            "Male",
            "Female",
            "Other"
        ])

        card_layout.addWidget(gender_label)
        card_layout.addWidget(self.gender_input)

        # --------------------------------------
        # HEIGHT
        # --------------------------------------

        self.height_input = self.create_input(
            card_layout,
            "Height (cm)"
        )

        # --------------------------------------
        # WEIGHT
        # --------------------------------------

        self.weight_input = self.create_input(
            card_layout,
            "Current Weight (kg)"
        )

        # --------------------------------------
        # ACTIVITY
        # --------------------------------------

        activity_label = QLabel("Activity Level")

        self.activity_input = QComboBox()

        self.activity_input.addItems([
            "Select Activity Level",
            "Sedentary",
            "Light",
            "Moderate",
            "Active",
            "Very Active"
        ])

        card_layout.addWidget(activity_label)
        card_layout.addWidget(self.activity_input)

        # --------------------------------------
        # GOAL
        # --------------------------------------

        goal_label = QLabel("Fitness Goal")

        self.goal_input = QComboBox()

        self.goal_input.addItems([
            "Select Goal",
            "Weight Loss",
            "Weight Gain",
            "Maintain Weight",
            "Build Muscle"
        ])

        card_layout.addWidget(goal_label)
        card_layout.addWidget(self.goal_input)

        # --------------------------------------
        # TARGET WEIGHT
        # --------------------------------------

        self.target_weight_input = self.create_input(
            card_layout,
            "Target Weight (kg)"
        )

        # --------------------------------------
        # SAVE BUTTON
        # --------------------------------------

        save_button = QPushButton(
            "Save Profile"
        )

        save_button.setObjectName(
            "primary_button"
        )

        save_button.clicked.connect(
            self.save_profile
        )

        card_layout.addWidget(save_button)

        main_layout.addWidget(card)

        main_layout.addStretch()

    # ==========================================
    # CREATE INPUT
    # ==========================================

    def create_input(self, layout, label_text):

        label = QLabel(label_text)

        input_box = QLineEdit()

        input_box.setPlaceholderText(
            f"Enter {label_text.lower()}"
        )

        layout.addWidget(label)
        layout.addWidget(input_box)

        return input_box

    # ==========================================
    # SAVE PROFILE
    # ==========================================

    def save_profile(self):

        name = self.name_input.text().strip()

        age_text = self.age_input.text().strip()

        height_text = self.height_input.text().strip()

        weight_text = self.weight_input.text().strip()

        target_weight_text = (
            self.target_weight_input
            .text()
            .strip()
        )

        gender = self.gender_input.currentText()

        activity = self.activity_input.currentText()

        goal = self.goal_input.currentText()

        # --------------------------------------
        # VALIDATION
        # --------------------------------------

        if not name:

            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter your name."
            )

            return

        if not age_text:

            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter your age."
            )

            return

        if not height_text:

            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter your height."
            )

            return

        if not weight_text:

            QMessageBox.warning(
                self,
                "Missing Information",
                "Please enter your current weight."
            )

            return

        try:

            age = int(age_text)

            height = float(height_text)

            weight = float(weight_text)

            target_weight = float(
                target_weight_text
            )

        except ValueError:

            QMessageBox.warning(
                self,
                "Invalid Input",
                "Please enter valid numbers."
            )

            return

        # --------------------------------------
        # SAVE TO DATABASE
        # --------------------------------------

        if self.user_id is None:

            self.user_id = add_user(
                name,
                age,
                gender,
                height,
                weight,
                activity,
                goal,
                target_weight
            )

        else:

            update_user(
                self.user_id,
                name,
                age,
                gender,
                height,
                weight,
                activity,
                goal,
                target_weight
            )

        QMessageBox.information(
            self,
            "Success",
            "Profile saved successfully!"
        )

    # ==========================================
    # LOAD USER
    # ==========================================

    def load_user(self):

        user = get_user(1)

        if user is None:

            return

        self.user_id = user["id"]

        self.name_input.setText(
            user["name"] or ""
        )

        if user["age"] is not None:

            self.age_input.setText(
                str(user["age"])
            )

        if user["gender"]:

            index = self.gender_input.findText(
                user["gender"]
            )

            if index >= 0:

                self.gender_input.setCurrentIndex(
                    index
                )

        if user["height"] is not None:

            self.height_input.setText(
                str(user["height"])
            )

        if user["weight"] is not None:

            self.weight_input.setText(
                str(user["weight"])
            )

        if user["activity_level"]:

            index = self.activity_input.findText(
                user["activity_level"]
            )

            if index >= 0:

                self.activity_input.setCurrentIndex(
                    index
                )

        if user["goal"]:

            index = self.goal_input.findText(
                user["goal"]
            )

            if index >= 0:

                self.goal_input.setCurrentIndex(
                    index
                )

        if user["target_weight"] is not None:

            self.target_weight_input.setText(
                str(user["target_weight"])
            )