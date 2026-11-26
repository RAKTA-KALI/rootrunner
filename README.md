# RootRunner: Terminal Trials — Linux & Kali Linux Command Learning Game (CLI, Python)

**RootRunner** is a free, open-source **terminal-based Linux command game** that helps you learn real **Linux commands** and **Kali Linux commands** by playing — not by memorizing. It runs as a single Python script with **zero dependencies** on **Kali Linux, Ubuntu, Debian, and Termux (Android)**, making it one of the only CLI games built specifically for people learning **Linux for cybersecurity, ethical hacking, ethical hacking practice, ethical hacking commands, and penetration testing basics**.

If you've searched for a *Linux command learning game*, a *Kali Linux terminal game*, a *CLI game to learn hacking commands*, or a *Termux game for learning Linux*, this project was built for exactly that.

![Python](https://img.shields.io/badge/Python-3.x-blue)
![Platform](https://img.shields.io/badge/Platform-Kali%20%7C%20Ubuntu%20%7C%20Termux-green)
![License](https://img.shields.io/badge/License-MIT-yellow)
![No Dependencies](https://img.shields.io/badge/Dependencies-None-success)

---

## 📑 Table of Contents

- [What is RootRunner?](#-what-is-rootrunner)
- [Why This Linux Command Game Is Different](#-why-this-linux-command-game-is-different)
- [Features](#-features)
- [Installation on Kali Linux / Ubuntu / Debian](#-installation-on-kali-linux--ubuntu--debian)
- [Installation on Termux (Android)](#-installation-on-termux-android)
- [How to Play](#-how-to-play)
- [Game Modes](#-game-modes)
- [Achievements](#-achievements)
- [Frequently Asked Questions](#-frequently-asked-questions)
- [Tech Stack](#️-tech-stack)
- [Contributing](#-contributing)
- [Author](#-author)
- [License](#-license)

---

## 🧠 What is RootRunner?

**RootRunner: Terminal Trials** is a gamified **Linux command trainer** and **Kali Linux learning tool** that turns real commands — `nmap`, `chmod`, `grep`, `hydra`, `awk`, `ss`, `john`, and 40+ more — into fast, timed missions. Instead of reading a static cheat sheet, you type the actual command under pressure, earn points for speed and accuracy, and get an instant explanation of what that command does — whether your answer was right or wrong.

It's designed for:
- Beginners learning **Linux terminal commands** for the first time
- Students preparing for **cybersecurity**, **ethical hacking**, or **CEH / OSCP-style** command recall
- Anyone practicing **Kali Linux commands** without risking a real system
- People who want a **fun CLI game** instead of a boring manual

## 🚀 Why This Linux Command Game Is Different

Most "learn Linux commands" resources are either static cheat sheets or dry tutorials. RootRunner is different because it combines, in one tool:

1. A **survival roguelike mode** with lives, streaks, and scaling difficulty
2. A **daily challenge mode** — the same 10 commands for every player, every day
3. A **boss rush speed mode** for rapid-fire command recall
4. **Explain-as-you-play** feedback on every single answer
5. A **persistent achievement and profile system**
6. A **built-in cheat sheet** for revision — no external website needed

No single existing Termux game, Kali Linux practice tool, or Linux command quiz combines all of this in one dependency-free Python file — which is what makes RootRunner a genuinely original **Linux learning game for the terminal**.

## ✨ Features

### 🎮 Three Game Modes
- **Survival Mode** — 3 lives, endless rounds, score-based difficulty scaling, fire-emoji streak multipliers
- **Daily Challenge** — the same 10 Linux/Kali commands for everyone, every day (date-seeded) with its own leaderboard
- **Boss Rush** — 5 rapid-fire, no-hint, no-skip commands with a huge perfect-clear bonus

### 💡 Explain-As-You-Play
Every answer — right **or wrong** — shows what the real command does and why. You learn Linux commands by understanding them, not just guessing.

### 🏆 Achievements & Profiles
10 unlockable achievements (First Blood, Speed Demon, Perfect Ten, Comeback Kid, Boss Slayer, and more), tracked per player with persistent stats: games played, accuracy %, best score, best streak.

### 📖 Study / Cheat-Sheet Mode
Every command in the game, grouped by category (Recon, Networking, Files & Permissions, System, Pentest Tools, Text Processing, Package Management), with its explanation — a built-in Linux command reference.

### 📊 Separate Leaderboards
Survival, Daily Challenge, and Boss Rush each keep their own local top-10 leaderboard.

### 🔥 Other Touches
- Speed bonuses for fast, correct answers
- Streak multipliers
- Optional terminal-bell sound feedback
- Full ANSI color terminal UI
- Pure Python 3 standard library — no `pip install` required

## 📦 Installation on Kali Linux / Ubuntu / Debian

```bash
git clone https://github.com/RAKTA-KALI/rootrunner.git
cd rootrunner
python3 rootrunner.py
```

## 📱 Installation on Termux (Android)

```bash
pkg install python git -y
git clone https://github.com/RAKTA-KALI/rootrunner.git
cd rootrunner
python rootrunner.py
```

No other packages, libraries, or root access needed — RootRunner is a pure Python 3 Linux command game that runs out of the box.

## 🎮 How to Play

1. Enter a codename — your stats and achievements save under it.
2. Pick a mode: Survival, Daily Challenge, or Boss Rush.
3. You'll see a mission, e.g. *"Show all active network interfaces and IPs"*.
4. Type the real Linux/Kali command (`ip a`, for example) as fast as you can.
5. Get an instant explanation of the command — whether you got it right or wrong.
6. In Survival Mode, type `hint` for a clue (costs points) or `skip` to forfeit a life.
7. Use **Study / Cheat Sheet** any time to review every command and its explanation.
8. Check **Profile & Achievements** to track your Linux command mastery over time.

## 🕹️ Game Modes

| Mode | Description |
|---|---|
| **Survival** | 3 lives, endless rounds, increasing difficulty, streak bonuses |
| **Daily Challenge** | Same 10 commands worldwide, every day — compare scores on that day's leaderboard |
| **Boss Rush** | 5 rapid-fire commands, no hints, no skips, big perfect-clear bonus |

## 🏅 Achievements

| Achievement | How to Unlock |
|---|---|
| First Blood | Score your first correct answer ever |
| Hint-Free Hero | Finish a Survival run scoring 100+ using zero hints |
| Speed Demon | Land 5 lightning-fast answers in a row |
| Perfect Ten | Reach a 10-answer correct streak |
| Comeback Kid | Survive on your last life and add 150+ more points |
| Root Runner | Reach 800+ score in one run |
| Legend Rising | Reach 1200+ score in one run |
| Daily Grinder | Complete a Daily Challenge |
| Boss Slayer | Clear a Boss Rush with a perfect 5/5 |
| Command Scholar | Open Study / Cheat Sheet mode once |

## ❓ Frequently Asked Questions

**Is RootRunner a hacking tool?**
No. RootRunner does not exploit, attack, or access any system. It is strictly an educational **Linux and Kali Linux command-learning game** — it only teaches command syntax and what each command does.

**Does it work on Termux without root?**
Yes. RootRunner needs no root access — just Python 3, which Termux installs via `pkg install python`.

**Do I need internet access to play?**
No. All gameplay, scoring, and the cheat sheet work fully offline after you clone the repository.

**What Linux commands does it teach?**
Commands across Recon (`whoami`, `uname -a`), Networking (`nmap`, `ping`, `tcpdump`), Files & Permissions (`chmod`, `chown`, `find`), System (`ps aux`, `top`, `kill`), Pentest Tools (`msfconsole`, `searchsploit`, `john`, `hydra`), Text Processing (`grep`, `sed`, `awk`), and Package Management (`apt`, `pkg`).

**Is this beginner-friendly?**
Yes. Difficulty scales automatically with your score, so beginners start with easy commands (`pwd`, `ls -la`) and gradually face harder ones (`nmap -sV`, `awk`).

## 🛠️ Tech Stack

- **Language:** Python 3 (standard library only — `os`, `sys`, `json`, `time`, `random`, `pathlib`, `textwrap`, `datetime`)
- **Dependencies:** None
- **Platforms:** Kali Linux, Ubuntu, Debian, Termux (Android)
- **Storage:** Local JSON files for scores (`rootrunner_scores.json`) and profiles (`rootrunner_profiles.json`), auto-created and git-ignored

## 🤝 Contributing

Pull requests adding more Linux/Kali commands, new categories, or new modes (multiplayer duels? a weekly boss ladder?) are welcome. Star ⭐ the repo if you found it useful for learning Linux commands!

## 👤 Author

**Aaryan Batham**
GitHub: [@RAKTA-KALI](https://github.com/RAKTA-KALI)

This is my first open-source project — feedback, stars, and pull requests are all welcome!

## 📄 License

MIT License — free to use, modify, and share. See [LICENSE](LICENSE) for details.

---

**Keywords:** linux command game, kali linux game, learn linux commands, terminal game python, cli game linux, termux game, ethical hacking practice tool, cybersecurity learning game, linux command trainer, kali linux terminal trainer
