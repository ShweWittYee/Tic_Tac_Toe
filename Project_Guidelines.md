## AI Policy: Use & Declaration
- **Limited AI Use:** AI coding assistants (e.g., GitHub Copilot) may be used for syntax suggestions, debugging, coding support, and learning assistance.
- **Prohibited:** Do not paste project prompts, guidelines, problem statements, or substantial portions of project materials into AI systems for code generation, completion, or debugging.
- **Responsibility:** Submitted work must reflect your own understanding, implementation, and problem-solving effort.

### AI Use Declaration

1. Complete the [PETRA AI Student Declaration](https://www.petraai.org/student) based on your actual AI use for this project.
2. Generate and save the declaration image as **`AI_declaration.png`**.
3. Include **`AI_declaration.png`** in your project repository root.

> **Required:** Your declaration must accurately reflect how you used AI tools for this project.

---

## Project Overview: Adversarial Search & Tic-Tac-Toe AI Visualizer

In this project, you will design, implement, and deploy an intelligent Game AI system for Tic-Tac-Toe using classical Adversarial Search strategies (Minimax with Alpha-Beta Pruning, Heuristic Priority Evaluation, and Random baselines), coupled with a full-stack interactive web visualizer.

The final outcome of this project is a fully functional web application deployed to a public, live URL.

---

### Learning Objectives

1. **Game Theory & Adversarial Search:** Master the Minimax decision rule for zero-sum, perfect information games.
2. **Search Optimization:** Implement Alpha-Beta pruning to minimize evaluated game tree nodes without compromising optimal play.
3. **Heuristic Evaluation:** Design rule-based priority evaluation functions for intermediate game state decision making.
4. **Web Development & Visualization:** Build a responsive Flask web application that visualizes decision trees, candidate move scores, and bot benchmarking.
5. **Generative AI Connections:** Connect classical adversarial game tree search with modern LLM reasoning concepts (MCTS, Tree of Thoughts, Process Reward Models).

---

## Your Job

1. Design and implement the core game state representation, move execution, win condition evaluation, and draw detection in `game.py`.
2. Implement AI search agents in `agent.py`:
   - `RandomAgent`: Uniform random move baseline (Easy).
   - `HeuristicAgent`: Rule-based priority strategy (Medium).
   - `MinimaxAgent`: Unbeatable Minimax agent with Alpha-Beta pruning (Hard/Unbeatable).
3. Connect the game engine and AI search agents to the Flask backend in `app.py`.
4. Build the interactive visualizer in `templates/index.html` with real-time score matrices, nodes explored, and bot vs bot benchmarking.
5. Complete `report.md` with your student information, agent configuration, search tree analysis, and technical discussion.
6. Deploy the completed application to a live hosting service (e.g., Render) so that it is publicly accessible.
7. Record a 5–7 minute video presentation demonstrating your application and explaining your implementation.

---

### 📋 Task 1: Game Engine & Rules (`game.py`)
Implement the `TicTacToe` game engine:
- 3x3 board representation with players `'X'` and `'O'`.
- Querying available legal moves (`get_available_moves()`).
- Executing legal moves (`make_move(pos, player)`) and backtracking / undoing moves (`undo_move(pos)`).
- Win condition evaluation (`check_winner()`, `get_winning_line()`) across all rows, columns, and diagonals.
- Draw state detection (`is_draw()`) and game over checks (`is_game_over()`).

---

### 📋 Task 2: AI Search Agents & Minimax (`agent.py`)
Implement three distinct AI strategies:
1. **Random Agent (`RandomAgent`):**
   - Uniformly samples from available legal positions.
2. **Heuristic Agent (`HeuristicAgent`):**
   - Implements a rule-based priority hierarchy: Immediate Win > Immediate Block > Center > Corners > Edges.
3. **Minimax Agent (`MinimaxAgent`):**
   - Implements recursive Minimax search with terminal depth scoring ($+10 - \text{depth}$ for fast wins, $\text{depth} - 10$ for delayed losses).
   - Incorporates Alpha-Beta pruning optimization ($\alpha \ge \beta$ cutoffs) to eliminate redundant game tree branch evaluations.
   - Tracks search statistics (e.g., nodes visited and candidate move scores).
   - Guarantees mathematical unbeatability (0 losses across any number of simulated games).
4. **Match Simulation (`simulate_match`):**
   - Simulates multi-game matches between any two agents to benchmark win, loss, and draw rates.

---

### 📋 Task 3: Interactive Web Visualizer (`app.py` & `templates/index.html`)
Build an interactive web application that provides:
1. **Multiple Game Modes:** Human vs AI (Easy, Medium, Unbeatable), 2-Player Local, and AI vs AI.
2. **Live Decision Visualizer:** Displays candidate move score matrices and search statistics (e.g., evaluated nodes).
3. **Simulation Benchmarking:** Runs automated bot-versus-bot matches and reports win/draw rate statistics in real time.

---

### 📋 Task 4: Complete the Report (`report.md`)
Complete all required sections in [report.md](report.md):
- **Student Information:** Full Name and MMDT ID.
- **AI Agent Configuration:** Document primary algorithm, pruning technique, and heuristic strategy.
- **Complexity & Search Tree Analysis:** Maximum search depth, total reachable board states, and unbeatability guarantee.
- **Local Verification Checklist:** Mark verified algorithms, agents, and features with `[x]`.
- **Deployed and Presentation Information:** Deployment platform, live deployment URL, and video presentation link.
- **Discussion:** Detailed answers explaining Alpha-Beta pruning optimization and comparing Adversarial Search with modern Generative AI tree search (MCTS, Tree of Thoughts, Process Reward Models).

> [!WARNING]
> Do not modify the section headers, bold titles, or overall formatting of [report.md](report.md). Changes to the structure may cause the autograder tests to fail.
> Replace all bracketed placeholder text with your answers. Do not leave any placeholders in the final report.

---

### 📋 Task 5: Record a Video Presentation

Record a **5–7 minute video presentation** explaining your project implementation:
- **Game Engine & Board Representation:** Explain how board state, move execution, win conditions, and undo mechanics are implemented.
- **AI Agents & Heuristics:** Explain how the heuristic priority hierarchy makes decisions.
- **Minimax Search & Alpha-Beta Pruning:** Explain the recursive Minimax formulation, terminal depth scoring, and how Alpha-Beta cutoffs prune redundant game tree branches.
- **Generative AI Connections:** Explain the relationship between classical adversarial search and modern LLM reasoning search (MCTS, Tree of Thoughts, PRMs).
- **Demonstration:** Demonstrate gameplay across all game modes, move score visualization, and bot benchmarking.

#### Video Requirements
- You may use tools such as Zoom, Loom, or OBS Studio to record your presentation.
- Your face must be visible during the presentation. If you are not comfortable with this requirement, please discuss it with the instructor in advance.
- The recorded video must be in `.mp4` format and must not exceed **7 minutes**.
- Upload the video to a sharing platform such as YouTube, Google Drive, or Dropbox.
- Ensure the video link is publicly accessible to the instructor.
- Add the video link to Section 4 of `report.md`.

---

## Marking Scheme (70 marks Autograde + 30 marks Manual Grade = 100 marks Total)

### 1. Implementation Tasks (40 marks) - Autograded
- **Required Files Check (10 marks):** `app.py`, `game.py`, `agent.py`, `templates/index.html`, `requirements.txt`, `report.md`, and `AI_declaration.png` present.
- **Game Engine & Rules (10 marks):** Board initialization, valid move execution, win condition evaluation, and draw state detection (`game.py`).
- **Heuristic Agent (5 marks):** Rule-based decision hierarchy (immediate wins, immediate blocks) in `agent.py`.
- **Minimax Agent & Unbeatability (15 marks):** Minimax search with Alpha-Beta pruning, optimal play, and mathematical unbeatability guarantee (0 losses) in `agent.py`.

### 2. Completion of report.md (30 marks) - Autograded
- **Student Information (5 marks):** Full Name and MMDT ID filled in.
- **AI Agent Configuration (5 marks):** Primary AI algorithm, pruning technique, and heuristic strategy documented.
- **Complexity & Search Tree Analysis (5 marks):** Search depth, total reachable board states, and unbeatability guarantee answered.
- **Local Verification Checklist (5 marks):** Checklist showing verified algorithms and features marked with `[x]`.
- **Deployment & Presentation Details (5 marks):** Provide valid live deployment platform, live URL, and video presentation link.
- **Discussion & Technical Analysis (5 marks):** Comprehensive answers explaining Alpha-Beta pruning optimization and comparing Adversarial Search with Generative AI tree search (MCTS / Tree of Thoughts / PRMs).

### 3. Live URL Verification, Correctness & Video Presentation (30 marks)
**Note:** This section is manually graded.
- **Live Deployment (5 marks):** The submitted URL is publicly accessible and the application loads successfully.
- **Application Correctness & Visualizer (15 marks):** The web application correctly supports Human vs AI (Easy, Medium, Unbeatable), 2-Player Local, and AI vs AI modes, and displays candidate move scores and search statistics.
- **Video Presentation (10 marks):** The 5–7 minute presentation clearly demonstrates the application, AI agent gameplay, and effectively explains the Minimax and Alpha-Beta pruning search concepts.

---

