# Gagan Bhusal — Robotics & ML Portfolio

Personal portfolio website of **Gagan Bhusal**, showcasing robotics, sim-to-real reinforcement learning, humanoid locomotion, and edge intelligence research.

Live at: **[gaganbhusal.github.io](https://gaganbhusal.github.io/)**

---

## 📁 Modular Structure

Everything is split into standalone files so you can easily edit one piece at a time:

```text
portfolio/
├── sections/               # Standalone sections for homepage
│   ├── bio.html            # Hero introduction, status badges, social links
│   ├── experience.html     # RAN Intern, Satellite RA, Third World Nerd
│   ├── education.html      # IOE Pulchowk Campus degree
│   └── skills.html         # Technical skills categories & stack pills
│
├── projects/               # Standalone HTML pages for each project
│   ├── unitree-go2.html    # Sim-to-Real Quadruped Locomotion
│   ├── unitree-g1.html     # Humanoid Motion Imitation
│   ├── alphazero.html      # Self-Play RL Connect-4 Agent
│   ├── ghost-net.html      # Edge AI Forest Bioacoustics
│   ├── satellite-sr.html   # Satellite Image Super-Resolution
│   ├── pinn.html           # Physics-Informed Neural Networks
│   ├── stem-quadruped.html # 8-DOF Open-Source Quadruped
│   └── transformer.html    # English-Nepali Machine Translation
│
├── css/
│   └── portfolio.css       # Shared unified stylesheet
├── template.html           # Homepage shell & modal logic
├── build.py (or build.sh)  # Instant compiler (python3 build.py)
└── index.html              # Compiled standalone page for GitHub Pages
```

---

## 🛠️ How to Edit

### 1. Edit Any Project
Open the specific file in `projects/` (e.g. `projects/unitree-go2.html`):
- Change any text, add new paragraphs, update metrics or links.
- You can open `projects/unitree-go2.html` directly in your browser to view it as a dedicated full-page write-up.

### 2. Edit Bio, Experience, Education, or Skills
Open the corresponding file in `sections/` (e.g. `sections/bio.html` or `sections/skills.html`).

### 3. Build & Publish
Whenever you commit with git, the pre-commit hook automatically runs `python3 build.py` and stages `index.html`.

You can also run it manually anytime:
```bash
./build.sh
```
Or:
```bash
python3 build.py
```
Then simply push:
```bash
git add .
git commit -m "Update Go2 project details"
git push
```

