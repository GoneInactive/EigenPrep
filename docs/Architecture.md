# 🏛️ EigenPrep Architecture

## Overview

EigenPrep is a modular, local-first Python application for practicing quantitative finance and brain teaser interview questions. It is built with PyQt5 for the UI, uses CSV files for question storage, and is designed for easy extension and customization.

---

## High-Level Structure

```
EigenPrep/
├── assets/           # Images, logo, icons
├── config/           # YAML config files
├── data/             # CSV files for each question category
├── docs/             # Documentation
├── src/
│   └── ui/           # PyQt5 UI modules
│       ├── main_window.py
│       └── quiz.py
├── requirements.txt  # Python dependencies
└── run_me.bat        # Windows launcher
```

---

## Main Components

### 1. User Interface (PyQt5)
- **src/ui/main_window.py**
  - Main menu: logo, info, and navigation buttons (Quiz, OA, Stats, Settings, Quit)
  - Handles launching the quiz window and returning to the menu
- **src/ui/quiz.py**
  - Launch page: logo, category selection, start button
  - Quiz flow: 5 random questions, timer, answer input, feedback, override button
  - End-of-quiz summary: score and time

### 2. Data Storage
- **data/**
  - Each CSV file represents a question category (e.g., `brain-teasers.csv`, `finance.csv`)
  - CSV columns: `category`, `question`, `answer`, `type`
- **config/config.yaml**
  - App configuration (version, debug mode, etc.)

### 3. Assets
- **assets/eigenprep.png**: Main logo
- **assets/**: Other icons, images, or fonts

---

## UI Flow

```mermaid
graph TD;
    MainMenu[Main Menu]
    QuizLaunch[Quiz Launch Page]
    QuizSession[Quiz Session (5 Questions)]
    QuizEnd[Quiz End (Score & Time)]
    MainMenu -->|Quiz| QuizLaunch
    QuizLaunch -->|Start Quiz| QuizSession
    QuizSession -->|Finish| QuizEnd
    QuizEnd -->|Close| MainMenu
```

---

## Data Flow

1. **Startup:**
   - Main window loads, scans `data/` for available categories (CSV files).
2. **Quiz Start:**
   - User selects a category; app loads questions from the corresponding CSV.
   - 5 questions are randomly selected for the session.
3. **Quiz Session:**
   - User answers each question; feedback is shown instantly.
   - Timer counts up from 0.
   - User can override and mark any question correct.
4. **Quiz End:**
   - Score and time are displayed.

---

## Extensibility Points

- **Add new categories:** Place a new CSV in `data/`.
- **Add new UI features:** Extend or add modules in `src/ui/`.
- **Change branding:** Replace images in `assets/`.
- **Change config:** Edit `config/config.yaml`.
- **Add new quiz types:** Create new windows or dialogs in `src/ui/` and link from the main menu.

---

## Example: Adding a New Category
1. Create a new CSV file in `data/` (e.g., `probability.csv`).
2. Use the columns: `category,question,answer,type`.
3. The new category will appear in the quiz category dropdown automatically.

---

## Example: Adding a New UI Feature
1. Create a new Python file in `src/ui/` (e.g., `stats.py`).
2. Implement your PyQt5 window or dialog.
3. Import and launch it from `main_window.py` (e.g., from the Stats button).

---

## Design Principles
- **Modularity:** Each feature is in its own file/module.
- **Transparency:** All data is local and human-readable.
- **Extensibility:** Easy to add new categories, features, or UI windows.
- **Modern UX:** Clean, accessible, and visually appealing interface.

---

## License

MIT 