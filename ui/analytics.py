
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QFrame,
    QScrollArea,
)

from matplotlib.backends.backend_qtagg import (
    FigureCanvasQTAgg as FigureCanvas,
)
from matplotlib.figure import Figure

from database import get_daily_logs

from services.analytics import (
    get_analytics_summary,
    get_weight_progress,
)
from services.recommendations import generate_recommendations
from services.prediction import get_model_metrics


class AnalyticsPage(QWidget):

    def __init__(self):
        super().__init__()

        self.create_ui()
        self.load_data()

    # ==========================================
    # CREATE UI
    # ==========================================

    def create_ui(self):

        outer_layout = QVBoxLayout(self)
        outer_layout.setContentsMargins(0, 0, 0, 0)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)

        content = QWidget()
        main_layout = QVBoxLayout(content)

        main_layout.setContentsMargins(35, 30, 35, 30)
        main_layout.setSpacing(18)

        # Page header
        title = QLabel("Analytics")
        title.setObjectName("page_title")

        description = QLabel(
            "Understand your fitness trends, progress, "
            "and machine-learning model performance."
        )
        description.setObjectName("description")
        description.setWordWrap(True)

        main_layout.addWidget(title)
        main_layout.addWidget(description)

        # ======================================
        # 7-DAY SUMMARY
        # ======================================

        summary_card = QFrame()
        summary_card.setObjectName("card")

        summary_layout = QVBoxLayout(summary_card)
        summary_layout.setContentsMargins(22, 20, 22, 20)
        summary_layout.setSpacing(12)

        summary_title = QLabel("7-Day Fitness Summary")
        summary_title.setObjectName("card_title")

        self.summary_label = QLabel("Loading summary...")
        self.summary_label.setObjectName("card_text")
        self.summary_label.setWordWrap(True)

        summary_layout.addWidget(summary_title)
        summary_layout.addWidget(self.summary_label)

        main_layout.addWidget(summary_card)

        # ======================================
        # WEIGHT PROGRESS
        # ======================================

        weight_progress_card = QFrame()
        weight_progress_card.setObjectName("card")

        weight_progress_layout = QVBoxLayout(
            weight_progress_card
        )
        weight_progress_layout.setContentsMargins(
            22, 20, 22, 20
        )
        weight_progress_layout.setSpacing(12)

        weight_progress_title = QLabel("Weight Progress")
        weight_progress_title.setObjectName("card_title")

        self.weight_progress_label = QLabel(
            "Loading weight progress..."
        )
        self.weight_progress_label.setObjectName("card_text")
        self.weight_progress_label.setWordWrap(True)

        weight_progress_layout.addWidget(weight_progress_title)
        weight_progress_layout.addWidget(
            self.weight_progress_label
        )

        main_layout.addWidget(weight_progress_card)

        # ======================================
        # RECOMMENDATIONS
        # ======================================

        recommendation_card = QFrame()
        recommendation_card.setObjectName("card")

        recommendation_layout = QVBoxLayout(
            recommendation_card
        )
        recommendation_layout.setContentsMargins(
            22, 20, 22, 20
        )
        recommendation_layout.setSpacing(12)

        recommendation_title = QLabel(
            "Fitness Recommendations"
        )
        recommendation_title.setObjectName("card_title")

        self.recommendation_label = QLabel(
            "Loading recommendations..."
        )
        self.recommendation_label.setObjectName("card_text")
        self.recommendation_label.setWordWrap(True)

        recommendation_layout.addWidget(
            recommendation_title
        )
        recommendation_layout.addWidget(
            self.recommendation_label
        )

        main_layout.addWidget(recommendation_card)

        # ======================================
        # ML MODEL PERFORMANCE
        # ======================================

        model_card = QFrame()
        model_card.setObjectName("card")

        model_layout = QVBoxLayout(model_card)
        model_layout.setContentsMargins(22, 20, 22, 20)
        model_layout.setSpacing(12)

        model_title = QLabel("ML Model Performance")
        model_title.setObjectName("card_title")

        self.model_metrics_label = QLabel(
            "Loading model evaluation metrics..."
        )
        self.model_metrics_label.setObjectName("card_text")
        self.model_metrics_label.setWordWrap(True)

        model_layout.addWidget(model_title)
        model_layout.addWidget(self.model_metrics_label)

        main_layout.addWidget(model_card)

        # ======================================
        # WEIGHT AND STEPS CHARTS
        # ======================================

        first_row = QHBoxLayout()
        first_row.setSpacing(15)

        weight_card = self.create_chart_card("Weight Trend")
        self.weight_figure = weight_card.figure
        self.weight_canvas = weight_card.canvas
        first_row.addWidget(weight_card)

        steps_card = self.create_chart_card("Steps Trend")
        self.steps_figure = steps_card.figure
        self.steps_canvas = steps_card.canvas
        first_row.addWidget(steps_card)

        main_layout.addLayout(first_row)

        # ======================================
        # SLEEP AND WORKOUT CHARTS
        # ======================================

        second_row = QHBoxLayout()
        second_row.setSpacing(15)

        sleep_card = self.create_chart_card("Sleep Trend")
        self.sleep_figure = sleep_card.figure
        self.sleep_canvas = sleep_card.canvas
        second_row.addWidget(sleep_card)

        workout_card = self.create_chart_card("Workout Trend")
        self.workout_figure = workout_card.figure
        self.workout_canvas = workout_card.canvas
        second_row.addWidget(workout_card)

        main_layout.addLayout(second_row)

        main_layout.addStretch()

        scroll_area.setWidget(content)
        outer_layout.addWidget(scroll_area)

    # ==========================================
    # CREATE CHART CARD
    # ==========================================

    def create_chart_card(self, title):

        card = QFrame()
        card.setObjectName("card")
        card.setMinimumWidth(0)

        layout = QVBoxLayout(card)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)

        title_label = QLabel(title)
        title_label.setObjectName("card_title")

        figure = Figure(figsize=(5, 3), dpi=100)
        figure.patch.set_facecolor("#FFFFFF")

        canvas = FigureCanvas(figure)
        canvas.setMinimumHeight(220)
        canvas.setStyleSheet(
            "background-color: #FFFFFF; border: 0px;"
        )

        layout.addWidget(title_label)
        layout.addWidget(canvas)

        card.figure = figure
        card.canvas = canvas

        return card

    # ==========================================
    # LOAD ML MODEL METRICS
    # ==========================================

    def load_model_metrics(self):

        try:
            metrics = get_model_metrics()

            if not metrics:
                self.model_metrics_label.setText(
                    "No evaluation metrics are stored yet.\n"
                    "Train the model to generate metrics."
                )
                return

            mae = metrics.get("mae")
            rmse = metrics.get("rmse")
            r2 = metrics.get("r2")

            mae_text = (
                f"{mae:.4f} kg"
                if mae is not None
                else "Unavailable"
            )

            rmse_text = (
                f"{rmse:.4f} kg"
                if rmse is not None
                else "Unavailable"
            )

            r2_text = (
                f"{r2:.4f}"
                if r2 is not None
                else "Unavailable"
            )

            self.model_metrics_label.setText(
                "Algorithm: Random Forest Regression\n"
                f"Mean Absolute Error (MAE): {mae_text}\n"
                f"Root Mean Squared Error (RMSE): {rmse_text}\n"
                f"R² Score: {r2_text}\n\n"
                "These metrics come from synthetic training data "
                "and do not demonstrate validated real-world "
                "prediction accuracy."
            )

        except Exception as error:
            self.model_metrics_label.setText(
                f"Model metrics unavailable: {error}"
            )

    # ==========================================
    # LOAD WEIGHT PROGRESS
    # ==========================================

    def load_weight_progress(self):

        progress = get_weight_progress(1)

        if progress["records"] == 0:
            self.weight_progress_label.setText(
                "No weight records available yet. "
                "Complete a Daily Check-in to start tracking."
            )
            return

        starting_weight = progress["starting_weight"]
        latest_weight = progress["latest_weight"]
        change = progress["change"]
        records = progress["records"]

        if change is None:
            change_text = (
                "Not enough records to calculate weight change."
            )
        elif change < 0:
            change_text = (
                f"Recorded weight decreased by "
                f"{abs(change):.1f} kg."
            )
        elif change > 0:
            change_text = (
                f"Recorded weight increased by "
                f"{change:.1f} kg."
            )
        else:
            change_text = (
                "Recorded weight remained unchanged."
            )

        self.weight_progress_label.setText(
            f"Recorded entries: {records} "
            "(within the latest seven check-ins)\n"
            f"Starting weight: {starting_weight:.1f} kg\n"
            f"Latest weight: {latest_weight:.1f} kg\n"
            f"{change_text}"
        )

    # ==========================================
    # LOAD ANALYTICS DATA
    # ==========================================

    def load_data(self):

        self.load_model_metrics()
        self.load_weight_progress()

        summary = get_analytics_summary(1)

        if summary["days"] > 0:

            self.summary_label.setText(
                f"Recorded check-ins: {summary['days']}\n"
                f"Average weight: "
                f"{summary['average_weight']:.1f} kg\n"
                f"Average steps: "
                f"{summary['average_steps']:.0f}\n"
                f"Average sleep: "
                f"{summary['average_sleep']:.1f} hours\n"
                f"Average workout: "
                f"{summary['average_workout']:.0f} minutes\n"
                f"Weight change: "
                f"{summary['weight_change']:+.1f} kg"
            )

        else:
            self.summary_label.setText(
                "No fitness data available yet.\n"
                "Complete daily check-ins to see your summary."
            )

        recommendations = generate_recommendations(summary)

        if recommendations:
            self.recommendation_label.setText(
                "\n".join(
                    f"{index}. {recommendation}"
                    for index, recommendation in enumerate(
                        recommendations,
                        start=1,
                    )
                )
            )
        else:
            self.recommendation_label.setText(
                "Complete more check-ins to receive recommendations."
            )

        logs = get_daily_logs(1)

        if not logs:
            self.show_empty_charts()
            return

        dates = []
        weights = []
        steps = []
        sleep = []
        workouts = []

        for log in logs:

            dates.append(log["date"])

            weights.append(
                log["weight"]
                if log["weight"] is not None
                else None
            )

            steps.append(
                log["steps"]
                if log["steps"] is not None
                else None
            )

            sleep.append(
                log["sleep_duration"]
                if log["sleep_duration"] is not None
                else None
            )

            workouts.append(
                log["workout_duration"]
                if log["workout_duration"] is not None
                else None
            )

        self.draw_chart(
            self.weight_figure,
            self.weight_canvas,
            dates,
            weights,
            "Weight (kg)",
        )

        self.draw_chart(
            self.steps_figure,
            self.steps_canvas,
            dates,
            steps,
            "Steps",
        )

        self.draw_chart(
            self.sleep_figure,
            self.sleep_canvas,
            dates,
            sleep,
            "Sleep (hours)",
        )

        self.draw_chart(
            self.workout_figure,
            self.workout_canvas,
            dates,
            workouts,
            "Workout (minutes)",
        )

    # ==========================================
    # DRAW CHART
    # ==========================================

    def draw_chart(
        self,
        figure,
        canvas,
        dates,
        values,
        y_label,
    ):

        figure.clear()
        ax = figure.add_subplot(111)

        valid_points = [
            (date, value)
            for date, value in zip(dates, values)
            if value is not None
        ]

        if not valid_points:

            ax.text(
                0.5,
                0.5,
                f"No {y_label.lower()} data yet",
                ha="center",
                va="center",
                transform=ax.transAxes,
            )

            ax.set_xticks([])
            ax.set_yticks([])

        else:

            plot_dates = [
                point[0] for point in valid_points
            ]

            plot_values = [
                point[1] for point in valid_points
            ]

            ax.plot(
                plot_dates,
                plot_values,
                marker="o",
                linewidth=2,
            )

            ax.set_ylabel(y_label)
            ax.tick_params(axis="x", rotation=45)
            ax.grid(alpha=0.2)

        ax.set_facecolor("#FFFFFF")
        ax.tick_params(colors="#526581", labelsize=9)
        ax.xaxis.label.set_color("#243653")
        ax.yaxis.label.set_color("#243653")
        ax.title.set_color("#172B55")
        for spine in ax.spines.values():
            spine.set_color("#DCE4F0")
        ax.grid(alpha=0.22, color="#AAB8CC")

        figure.tight_layout()
        canvas.draw()

    # ==========================================
    # EMPTY CHARTS
    # ==========================================

    def show_empty_charts(self):

        self.show_empty_chart(
            self.weight_figure,
            self.weight_canvas,
            "No weight data yet",
        )

        self.show_empty_chart(
            self.steps_figure,
            self.steps_canvas,
            "No steps data yet",
        )

        self.show_empty_chart(
            self.sleep_figure,
            self.sleep_canvas,
            "No sleep data yet",
        )

        self.show_empty_chart(
            self.workout_figure,
            self.workout_canvas,
            "No workout data yet",
        )

    def show_empty_chart(
        self,
        figure,
        canvas,
        message,
    ):

        figure.clear()
        ax = figure.add_subplot(111)

        ax.text(
            0.5,
            0.5,
            message,
            ha="center",
            va="center",
            transform=ax.transAxes,
        )

        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_facecolor("#FFFFFF")
        ax.tick_params(colors="#526581", labelsize=9)
        ax.xaxis.label.set_color("#243653")
        ax.yaxis.label.set_color("#243653")
        ax.title.set_color("#172B55")
        for spine in ax.spines.values():
            spine.set_color("#DCE4F0")
        ax.grid(alpha=0.22, color="#AAB8CC")

        figure.tight_layout()
        canvas.draw()

    # ==========================================
    # REFRESH ANALYTICS
    # ==========================================

    def refresh_data(self):
        self.load_data()
