## Project Overview: MMDT Tic-Tac-Toe AI Visualizer

In this project, you will implement, test, and deploy an intelligent Game AI system for Tic-Tac-Toe powered by classical Adversarial Search strategies: **Minimax Search with Alpha-Beta Pruning**, **Heuristic Priority Evaluation**, and **Random baseline agents**, coupled with a full-stack interactive Flask web visualizer.

The final outcome of this project is a fully functional web application deployed to a public, live URL.

---

### Learning Objectives

1. **Game Theory & Adversarial Search:** Master zero-sum game trees and the Minimax decision principle.
2. **Search Optimization:** Implement Alpha-Beta pruning to eliminate redundant search branches without sacrificing optimal play.
3. **Agent Design & Heuristics:** Implement rule-based priority heuristics and evaluate agent performance against baselines.
4. **Interactive Visualization & Web Backend:** Build and deploy a modern web visualizer with real-time candidate move scores and bot benchmarking.
5. **AI Reasoning Connections:** Relate classical game search with modern LLM reasoning search paradigms (MCTS, Tree of Thoughts, Process Reward Models).

---

## Project Structure

You are expected to organize and implement your project according to the following structure:

```text
├── app.py                      # Flask server and game API endpoints
├── game.py                     # TicTacToe game engine, rules, and board representation
├── agent.py                    # AI Search Agents: Minimax, Heuristic, Random
├── templates/
│   └── index.html              # Interactive web frontend & Minimax visualizer
├── requirements.txt            # Python dependencies (flask, pytest, gunicorn)
├── Procfile                    # Web service deployment configuration (e.g., Render)
├── report.md                   # Submission report template
├── AI_declaration.png          # AI use declaration image
├── pytest.ini                  # Pytest configuration
├── tests/
│   ├── conftest.py             # Scorecard generator
│   ├── test_files.py           # Project structure verification
│   ├── test_game.py            # Game engine unit tests
│   ├── test_agent.py           # AI agent & Minimax unbeatability tests
│   └── test_report.py          # Report completeness verification
├── Project_Guidelines.md       # Detailed assignment guidelines & marking scheme
└── README.md                   # This file
```

---

## Submission Guidelines

To submit your project, please ensure you complete all required tasks and follow these instructions carefully.

### 1. Preparation Checklist
Before pushing your final submission, verify that:
* [ ] You have implemented the game mechanics in `game.py`.
* [ ] You have implemented all three AI agents in `agent.py` (`RandomAgent`, `HeuristicAgent`, `MinimaxAgent` with Alpha-Beta pruning).
* [ ] You have verified that Minimax is mathematically unbeatable via `pytest tests/test_agent.py`.
* [ ] You have built the Flask backend in `app.py` and UI in `templates/index.html`.
* [ ] You have completed the AI Student Declaration on [PETRA AI](https://www.petraai.org/student) and saved it as `AI_declaration.png` in the repository root.
* [ ] You have completed all sections in `report.md` (with your Name, MMDT ID, live deployment URL, video presentation link, and discussion answers). Do not alter the structure of `report.md`.
* [ ] You have deployed your application live (e.g. Render) and recorded a 5–7 minute video presentation (.mp4, face visible) demonstrating the application, and uploaded it to YouTube, Google Drive, or Dropbox (with public view access).

### 2. How to Submit
Once everything is ready, commit and push your code to your GitHub repository's `main` or `master` branch:
```bash
git add .
git commit -m "Submit Project: MMDT Tic-Tac-Toe AI"
git push origin main
```
The automated autograding system will automatically run tests upon pushing to the `main` or `master` branch.

---

## Checking Grades

You can check your project grades both locally and online via GitHub Actions.

### 1. Locally (Before Submitting)
You can run the autograding tests on your local machine:
1. Make sure you have installed all dependencies listed in `requirements.txt`:
   ```bash
   pip install -r requirements.txt
   ```
2. Run `pytest` inside the project root:
   ```bash
   pytest tests/
   ```
3. A scorecard summarizing your earned marks will be outputted directly in the terminal under the section **"AUTOGRADING SCORECARD"**.

### 2. On GitHub (After Submitting)
Every push to the repository triggers the online autograder.
1. Go to the **Actions** tab of your GitHub repository.
2. Select the latest run (e.g., "Autograder Check" or your commit message).
3. Under the run details, view the **Autograding Scorecard** step summary, which details your score out of 70 marks.

---

## Grading Details & Passing Requirements

* **Autograded Score:** **70 marks** (40 marks for implementation tasks, 30 marks for `report.md` completion).
* **Manually Graded Score:** **30 marks** (Live deployment verification, visualizer correctness, and video presentation).
* **Total Coursework Marks:** **100 marks**.
* **Deadline:** **October 11, 2026, at 23:59:59**.
* **Late Submission Policy:** A penalty of **-10 marks per day** will be applied for late submissions.
* **Commitment Fee:** Any late, missing, or failed project (score < 70%) will carry a **30,000 MMK commitment fee**, calculated and collected at the end of the 10-week challenge.
