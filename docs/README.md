# 📖 EigenPrep Documentation

## Overview

**EigenPrep** is a modern, local-first Python application for practicing quantitative finance and brain teaser interview questions. It features a beautiful PyQt5 interface, category-based quizzes, instant feedback, and easy extensibility.

---

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Running the App](#running-the-app)
- [Usage Guide](#usage-guide)
- [Data Format](#data-format)
- [Customization](#customization)
- [Extending the App](#extending-the-app)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Modern PyQt5 UI**: Clean, responsive, and branded interface.
- **Quiz Mode**: Select a category, get a 5-question quiz, timer counts up, instant feedback, and an override button to mark any question correct.
- **Easy Data Editing**: All questions are stored in CSV files for transparency and easy editing.
- **No Cloud, No Accounts**: All data and progress are local for privacy and speed.
- **Customizable**: Add your own questions, categories, or extend the UI.

---

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/CUQuants/EigenPrep.git
   cd EigenPrep
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

---

## Running the App

- **From the command line:**
  ```sh
  python -m src.main
  ```
- Or use the provided `run_me.bat` on Windows.

---

## Usage Guide

### Main Menu
- **Quiz**: Start a new quiz. Select a category, then answer 5 random questions. Timer counts up. See your score and time at the end. Use the **Override: Mark Correct** button if you want to manually mark a question correct.
- **Online Assessment, Stats, Settings**: (Planned features)
- **Quit**: Exit the application.

### Quiz Flow
1. **Select a category** from the dropdown.
2. **Click Start Quiz**.
3. **Answer each question**. Submit your answer and receive instant feedback.
4. If you believe your answer should be accepted, use the **Override: Mark Correct** button.
5. **Proceed to the next question**. After 5 questions, see your score and time.

---

## Data Format

- All questions are stored in CSV files in the `data/` directory.
- Each file represents a category (e.g., `brain-teasers.csv`, `finance.csv`).
- **CSV columns:**
  - `category`: The category name (e.g., "Brain Teaser")
  - `question`: The question text
  - `answer`: The correct answer (as a string)
  - `type`: The question type (e.g., "text")

**Example:**
```csv
category,question,answer,type
Brain Teaser,"What is 2+2?",4,text
```

---

## Customization

- **Add new questions:**
  - Edit or add CSV files in the `data/` directory.
  - Follow the same column format as above.
- **Change the logo:**
  - Replace `assets/eigenprep.png` with your own PNG file.
- **Change app settings:**
  - Edit `config/config.yaml` (e.g., version, debug mode).

---

## Extending the App

- **Add new quiz types or features:**
  - Extend the PyQt5 UI in `src/ui/` (e.g., add new windows or dialogs).
- **Add new categories:**
  - Add new CSV files to `data/` and they will appear in the category dropdown.
- **Contribute code:**
  - Fork the repo, make your changes, and submit a pull request.

---

## Troubleshooting

- **App doesn't launch:**
  - Ensure all dependencies are installed (`pip install -r requirements.txt`).
  - Run with `python -m src.main` from the project root.
- **No categories appear:**
  - Make sure there are CSV files in the `data/` directory.
- **GUI issues:**
  - Try updating PyQt5: `pip install --upgrade PyQt5`.

---

## Contributing

Pull requests are welcome! Please ensure new features are modular and maintain the app's speed and simplicity.

---

## License

MIT 