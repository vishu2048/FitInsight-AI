<<<<<<< HEAD
# FitInsight AI — Fitness Analytics Desktop Application

FitInsight AI is a desktop application for recording daily fitness activity, viewing trends, receiving rule-based recommendations, and demonstrating a Random Forest regression workflow for weight estimation.

## Features

- **Dashboard:** current recorded metrics, profile overview, daily fitness score, rule-based insights, and an experimental model estimate.
- **Profile:** save personal and fitness-goal information.
- **Daily Check-in:** record weight, steps, sleep, workout duration, calories, water intake, and notes. The application prevents a second check-in for the same user and date.
- **Analytics:** seven-calendar-day summary, weight progress, recommendations, model evaluation metrics, and weight/steps/sleep/workout charts.
- **ML Prediction:** estimate future weight from the latest check-in using the locally saved Random Forest model.
- **Local storage:** SQLite database stored in `database/fitinsight.db`.

## Technology

- Python
- PySide6
- SQLite
- Pandas and NumPy
- Matplotlib
- scikit-learn
- Joblib

## Setup (Windows / VS Code)

1. Install Python 3.11 or newer.
2. Extract the project ZIP.
3. Open the extracted `FitInsight-AI-Submission` folder in VS Code.
4. Open a terminal in that folder.
5. Create a virtual environment:

   ```powershell
   py -m venv venv
   ```

6. Activate it:

   ```powershell
   .\venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, use the interpreter directly in the next steps.

7. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

8. Run the application:

   ```powershell
   python main.py
   ```

   Or, without activating the environment:

   ```powershell
   .\venv\Scripts\python.exe main.py
   ```

## Machine-learning model

The application loads `ml/weight_model.pkl`. The supplied model is included in the submission.

To retrain it:

```powershell
python ml/train_model.py
```

The training script expects `data/fitness_dataset.csv` with these columns:

- `weight`
- `steps`
- `sleep_duration`
- `workout_duration`
- `calories_burned`
- `calories_consumed`
- `water_intake`
- `future_weight`

The model's saved evaluation metrics are displayed in Analytics.

### Important model limitation

The supplied dataset is synthetic/demo data. Its test metrics are useful for demonstrating the training and evaluation pipeline, but they do **not** establish real-world medical or fitness prediction accuracy. Predictions should be treated as experimental estimates, not health advice.

## Project structure

```text
FitInsight-AI-Submission/
├── main.py
├── database.py
├── models.py
├── requirements.txt
├── README.md
├── .gitignore
├── assets/
├── data/
│   └── fitness_dataset.csv
├── database/
│   └── fitinsight.db
├── ml/
│   ├── model.py
│   ├── train_model.py
│   └── weight_model.pkl
├── services/
│   ├── ai_insights.py
│   ├── analytics.py
│   ├── prediction.py
│   └── recommendations.py
└── ui/
    ├── analytics.py
    ├── daily_checkin.py
    ├── dashboard.py
    ├── main_window.py
    ├── prediction.py
    └── profile.py
```

## Data and privacy

The application stores profile and check-in information locally in SQLite. Keep a backup of `database/fitinsight.db` before making manual database changes or moving the project to another computer.

## Submission checklist

- [ ] Install dependencies successfully.
- [ ] Run `python main.py`.
- [ ] Open Profile and verify the saved profile.
- [ ] Save a daily check-in.
- [ ] Confirm Dashboard and Analytics refresh.
- [ ] Open ML Prediction and generate an estimate.
- [ ] Keep the synthetic-data limitation in the project report/presentation.
=======
# FitInsight-AI
AI-powered fitness analytics and weight prediction desktop application using Python, PySide6, SQLite and Machine Learning.
>>>>>>> 84da2526307df0a8d0198dda6ae73ee52550bcc0
