#!/usr/bin/env python3
"""
RootRunner: Terminal Trials
----------------------------
The one-and-only terminal command-mastery roguelike.

A fast, addictive, EXPLAIN-AS-YOU-PLAY terminal game that teaches real
Linux & Kali Linux commands through three distinct modes, a profile +
achievement system, and a built-in cheat-sheet study mode.

Runs anywhere Python 3 runs — Kali Linux, Ubuntu, Debian, Termux.
Zero external dependencies. Zero exploit code. Pure command mastery.

Author  : Aaryan Batham
GitHub  : https://github.com/RAKTA-KALI
License : MIT
"""

import os
import sys
import json
import time
import random
import textwrap
from pathlib import Path
from datetime import date

# --------------------------------------------------------------------------
# COLORS
# --------------------------------------------------------------------------

class C:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    GREEN = "\033[92m"
    RED = "\033[91m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    MAGENTA = "\033[95m"
    BLUE = "\033[94m"
    WHITE = "\033[97m"
    ORANGE = "\033[38;5;208m"


BASE_DIR = Path(__file__).resolve().parent
SCORE_FILE = BASE_DIR / "rootrunner_scores.json"
PROFILE_FILE = BASE_DIR / "rootrunner_profiles.json"

BANNER = r"""
 ____             _   ____                            
|  _ \ ___   ___ | |_|  _ \ _   _ _ __  _ __   ___ _ __ 
| |_) / _ \ / _ \| __| |_) | | | | '_ \| '_ \ / _ \ '__|
|  _ < (_) | (_) | |_|  _ <| |_| | | | | | | |  __/ |   
|_| \_\___/ \___/ \__|_| \_\__,_|_| |_|_| |_|\___|_|   

            T E R M I N A L   T R I A L S
"""

RANKS = [
    (0,    "Script Kiddie"),
    (50,   "Shell Novice"),
    (150,  "Terminal Operator"),
    (300,  "Packet Wrangler"),
    (500,  "Grey Hat Grinder"),
    (800,  "Root Runner"),
    (1200, "Kernel Whisperer"),
    (1800, "Ghost in the Shell"),
    (2500, "Legend of /bin"),
]

# --------------------------------------------------------------------------
# COMMAND BANK
# Each entry: category, difficulty(1-3), hint, [accepted answers], explanation
# --------------------------------------------------------------------------

COMMANDS = [
    dict(cat="Recon", diff=1, hint="Show your current username",
         ans=["whoami"], why="whoami prints the username of the account currently running the shell."),
    dict(cat="Recon", diff=1, hint="Show current working directory",
         ans=["pwd"], why="pwd = 'print working directory'. Shows the absolute path you're standing in."),
    dict(cat="Recon", diff=1, hint="List files including hidden ones, long format",
         ans=["ls -la", "ls -al"], why="-l gives long (detailed) format, -a shows hidden dotfiles too."),
    dict(cat="Recon", diff=1, hint="Show system and kernel info",
         ans=["uname -a"], why="uname -a prints kernel name, version, architecture — everything in one line."),
    dict(cat="Recon", diff=2, hint="Show all active network interfaces and IPs",
         ans=["ip a", "ip addr", "ifconfig"], why="'ip a' is the modern replacement for the older 'ifconfig'."),
    dict(cat="Recon", diff=2, hint="Show currently logged in users",
         ans=["who", "w"], why="'who' lists logged in users; 'w' adds what they're currently doing."),
    dict(cat="Recon", diff=2, hint="Show OS release details",
         ans=["cat /etc/os-release"], why="/etc/os-release holds distro name, version, and ID on nearly all Linux systems."),
    dict(cat="Recon", diff=3, hint="Show listening ports with process names",
         ans=["ss -tulnp", "netstat -tulnp"], why="'ss' is the modern, faster replacement for 'netstat'; flags show TCP/UDP listening sockets with PIDs."),

    dict(cat="Networking", diff=1, hint="Ping a host 4 times",
         ans=["ping -c 4", "ping -c4"], why="-c sets the packet count so ping stops automatically instead of running forever."),
    dict(cat="Networking", diff=2, hint="Scan a target's open ports with nmap (basic)",
         ans=["nmap"], why="The base nmap command does a default TCP connect scan on common ports."),
    dict(cat="Networking", diff=2, hint="Do a stealthy SYN scan with nmap",
         ans=["nmap -sS"], why="-sS sends SYN packets without completing the handshake — faster and quieter in logs."),
    dict(cat="Networking", diff=3, hint="Nmap scan with service/version detection",
         ans=["nmap -sV"], why="-sV probes open ports to identify the actual service and version running."),
    dict(cat="Networking", diff=3, hint="Nmap scan all 65535 ports",
         ans=["nmap -p-"], why="-p- is shorthand for -p 1-65535, scanning every possible port."),
    dict(cat="Networking", diff=2, hint="Download a file from a URL via terminal",
         ans=["curl -O", "wget"], why="curl -O saves with the remote filename; wget downloads directly by default."),
    dict(cat="Networking", diff=2, hint="Show the route packets take to a host",
         ans=["traceroute", "tracepath"], why="Both print each network hop between you and the destination."),
    dict(cat="Networking", diff=3, hint="Capture packets live on an interface with tcpdump",
         ans=["tcpdump -i"], why="-i specifies which interface to listen on, e.g. tcpdump -i eth0."),

    dict(cat="Files", diff=1, hint="Create a new empty file",
         ans=["touch"], why="touch creates an empty file if it doesn't exist, or updates its timestamp if it does."),
    dict(cat="Files", diff=1, hint="Make a new directory",
         ans=["mkdir"], why="mkdir creates a new, empty directory at the given path."),
    dict(cat="Files", diff=1, hint="Copy a file",
         ans=["cp"], why="cp copies a file (or with -r, a whole directory) to a new location."),
    dict(cat="Files", diff=1, hint="Move or rename a file",
         ans=["mv"], why="mv moves files between locations — renaming is just moving within the same folder."),
    dict(cat="Files", diff=2, hint="Give a script execute permission for the owner",
         ans=["chmod +x", "chmod u+x"], why="+x adds execute permission so the file can be run as a program/script."),
    dict(cat="Files", diff=2, hint="Change file ownership to a user",
         ans=["chown"], why="chown changes which user (and optionally group) owns a file."),
    dict(cat="Files", diff=2, hint="Find all .txt files under current directory",
         ans=["find . -name \"*.txt\"", "find . -name '*.txt'"], why="find searches recursively; -name matches filenames by pattern."),
    dict(cat="Files", diff=3, hint="Search recursively for a word inside files",
         ans=["grep -r"], why="-r tells grep to search every file inside the directory tree, not just one file."),
    dict(cat="Files", diff=3, hint="Set permissions to rwxr-xr-x numerically",
         ans=["chmod 755"], why="755 in octal = owner rwx(7), group r-x(5), others r-x(5)."),

    dict(cat="System", diff=1, hint="Show running processes (full list)",
         ans=["ps aux"], why="aux shows processes from all users, in a user-friendly extended format."),
    dict(cat="System", diff=1, hint="Show a live view of system resource usage",
         ans=["top", "htop"], why="Both show live CPU/RAM/process stats; htop is the prettier, interactive version."),
    dict(cat="System", diff=2, hint="Kill a process by its PID",
         ans=["kill"], why="kill sends a termination signal to the process ID you specify."),
    dict(cat="System", diff=2, hint="Show disk usage of filesystems",
         ans=["df -h"], why="-h means 'human-readable' sizes (GB/MB) instead of raw byte counts."),
    dict(cat="System", diff=2, hint="Show memory usage",
         ans=["free -h"], why="free -h shows total/used/free RAM and swap in human-readable units."),
    dict(cat="System", diff=3, hint="Forcefully kill a process by name",
         ans=["pkill -9", "killall -9"], why="-9 sends SIGKILL, an immediate, un-ignorable termination signal."),

    dict(cat="Pentest", diff=2, hint="Launch the Metasploit console",
         ans=["msfconsole"], why="msfconsole opens the Metasploit Framework's interactive command interface."),
    dict(cat="Pentest", diff=2, hint="Search exploit-db from terminal for a keyword",
         ans=["searchsploit"], why="searchsploit queries a local copy of Exploit-DB by keyword, offline."),
    dict(cat="Pentest", diff=3, hint="Crack a password hash file with john",
         ans=["john"], why="John the Ripper takes a hash file and attempts to recover plaintext passwords."),
    dict(cat="Pentest", diff=3, hint="Put a wireless interface into monitor mode",
         ans=["airmon-ng start"], why="Monitor mode lets the wireless card capture all nearby traffic, not just traffic addressed to it."),
    dict(cat="Pentest", diff=3, hint="Brute force an SSH login with hydra",
         ans=["hydra -l"], why="-l sets a single username to try against a password list for the target service."),
    dict(cat="Pentest", diff=2, hint="Show the current wireless interfaces",
         ans=["iwconfig"], why="iwconfig is the wireless-specific counterpart to ifconfig, showing SSID, mode, signal, etc."),
    dict(cat="Pentest", diff=3, hint="Run an Nmap default-script scan",
         ans=["nmap -sC"], why="-sC runs Nmap's default safe script set for extra service enumeration."),

    dict(cat="Text", diff=1, hint="Print the contents of a file",
         ans=["cat"], why="cat ('concatenate') dumps a file's full contents straight to the terminal."),
    dict(cat="Text", diff=1, hint="Show the first 10 lines of a file",
         ans=["head"], why="By default head shows the first 10 lines; -n changes the count."),
    dict(cat="Text", diff=1, hint="Show the last 10 lines of a file, following new lines",
         ans=["tail -f"], why="-f keeps the file open and prints new lines as they're appended — great for live logs."),
    dict(cat="Text", diff=2, hint="Count the number of lines in a file",
         ans=["wc -l"], why="wc counts words/lines/bytes; -l restricts it to just line count."),
    dict(cat="Text", diff=2, hint="Replace all 'foo' with 'bar' in a file using sed",
         ans=["sed 's/foo/bar/g'", 'sed "s/foo/bar/g"'], why="s/old/new/g = substitute, globally (every match per line, not just the first)."),
    dict(cat="Text", diff=3, hint="Print only the 2nd column of a space-separated file with awk",
         ans=["awk '{print $2}'", 'awk "{print $2}"'], why="awk splits each line into fields; $2 refers to the second field."),

    dict(cat="Packages", diff=1, hint="Update package lists on Debian/Kali",
         ans=["apt update", "sudo apt update"], why="Refreshes the local index of available packages/versions — doesn't install anything yet."),
    dict(cat="Packages", diff=1, hint="Install a package named nmap",
         ans=["apt install nmap", "sudo apt install nmap"], why="apt install fetches and installs the named package and its dependencies."),
    dict(cat="Packages", diff=2, hint="Install a package in Termux",
         ans=["pkg install"], why="Termux wraps apt with its own 'pkg' command tailored for the Android environment."),
]

LIVES_START = 3
TIME_FAST = 6
TIME_OK = 12
BELL = "\a"

# --------------------------------------------------------------------------
# ACHIEVEMENTS
# --------------------------------------------------------------------------

ACHIEVEMENTS = [
    dict(id="first_blood", name="First Blood", desc="Score your first correct answer ever.",
         check=lambda s, p: p["total_correct"] >= 1),
    dict(id="hintless_hero", name="Hint-Free Hero", desc="Finish a Survival run scoring 100+ using zero hints.",
         check=lambda s, p: s["mode"] == "survival" and s["hints_used"] == 0 and s["score"] >= 100),
    dict(id="speed_demon", name="Speed Demon", desc="Land 5 lightning-fast answers in a row.",
         check=lambda s, p: s.get("max_lightning_streak", 0) >= 5),
    dict(id="perfect_ten", name="Perfect Ten", desc="Reach a 10-answer correct streak in one run.",
         check=lambda s, p: s.get("max_streak", 0) >= 10),
    dict(id="comeback_kid", name="Comeback Kid", desc="Survive on your last life and still add 150+ more points.",
         check=lambda s, p: s.get("comeback_pts", 0) >= 150),
    dict(id="root_runner", name="Root Runner", desc="Reach the 'Root Runner' rank (800+ score) in one run.",
         check=lambda s, p: s["score"] >= 800),
    dict(id="legend_rising", name="Legend Rising", desc="Reach the 'Kernel Whisperer' rank (1200+ score) in one run.",
         check=lambda s, p: s["score"] >= 1200),
    dict(id="daily_grinder", name="Daily Grinder", desc="Complete a Daily Challenge.",
         check=lambda s, p: s["mode"] == "daily"),
    dict(id="boss_slayer", name="Boss Slayer", desc="Clear a Boss Rush with a perfect 5/5.",
         check=lambda s, p: s["mode"] == "boss" and s.get("boss_perfect")),
    dict(id="scholar", name="Command Scholar", desc="Open the Study / Cheat Sheet mode at least once.",
         check=lambda s, p: p.get("opened_study", False)),
]

# --------------------------------------------------------------------------
# HELPERS
# --------------------------------------------------------------------------

def clear():
    os.system("clear" if os.name != "nt" else "cls")


def rank_for_score(score):
    current = RANKS[0][1]
    for threshold, name in RANKS:
        if score >= threshold:
            current = name
    return current


def load_json(path, default):
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            return default
    return default


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2))


def get_profile(name):
    profiles = load_json(PROFILE_FILE, {})
    if name not in profiles:
        profiles[name] = dict(games=0, total_correct=0, total_wrong=0,
                               best_score=0, best_streak=0, achievements=[],
                               opened_study=False)
    return profiles


def save_profile(profiles):
    save_json(PROFILE_FILE, profiles)


def save_score(name, score, mode):
    scores = load_json(SCORE_FILE, [])
    scores.append(dict(name=name, score=score, mode=mode,
                        ts=time.strftime("%Y-%m-%d %H:%M"),
                        date=date.today().isoformat()))
    scores.sort(key=lambda x: x["score"], reverse=True)
    save_json(SCORE_FILE, scores[:200])


def beep(enabled):
    if enabled:
        sys.stdout.write(BELL)
        sys.stdout.flush()


def check_achievements(state, profiles, player):
    profile = profiles[player]
    newly = []
    for a in ACHIEVEMENTS:
        if a["id"] in profile["achievements"]:
            continue
        try:
            if a["check"](state, profile):
                profile["achievements"].append(a["id"])
                newly.append(a)
        except Exception:
            pass
    return newly


# --------------------------------------------------------------------------
# LEADERBOARD / STUDY VIEWS
# --------------------------------------------------------------------------

def show_leaderboard():
    clear()
    print(C.CYAN + C.BOLD + "\n=== LEADERBOARDS ===" + C.RESET)
    print(f"  {C.CYAN}[1]{C.RESET} Survival   {C.CYAN}[2]{C.RESET} Daily Challenge   {C.CYAN}[3]{C.RESET} Boss Rush   {C.CYAN}[4]{C.RESET} Back")
    choice = input(C.YELLOW + "> " + C.RESET).strip()
    mode_map = {"1": "survival", "2": "daily", "3": "boss"}
    if choice not in mode_map:
        return
    mode = mode_map[choice]
    scores = load_json(SCORE_FILE, [])
    if mode == "daily":
        today = date.today().isoformat()
        scores = [s for s in scores if s.get("mode") == "daily" and s.get("date") == today]
        title = f"DAILY CHALLENGE — {today}"
    else:
        scores = [s for s in scores if s.get("mode") == mode]
        title = mode.upper()
    scores.sort(key=lambda x: x["score"], reverse=True)
    scores = scores[:10]

    clear()
    print(C.CYAN + C.BOLD + f"\n=== {title} — TOP 10 ===" + C.RESET + "\n")
    if not scores:
        print(C.DIM + "No scores yet. Be the first legend." + C.RESET)
    else:
        for i, s in enumerate(scores, 1):
            print(f"{C.YELLOW}{i:>2}.{C.RESET} {s['name']:<15} {C.GREEN}{s['score']:>6} pts{C.RESET}  {C.DIM}{s['ts']}{C.RESET}")
    input(C.DIM + "\nPress Enter to go back..." + C.RESET)


def show_study_mode(profiles, player):
    profiles[player]["opened_study"] = True
    save_profile(profiles)
    clear()
    print(C.CYAN + C.BOLD + "\n=== STUDY MODE: COMMAND CHEAT SHEET ===" + C.RESET)
    cats = sorted(set(c["cat"] for c in COMMANDS))
    for cat in cats:
        print(f"\n{C.MAGENTA}{C.BOLD}## {cat}{C.RESET}")
        for entry in [c for c in COMMANDS if c["cat"] == cat]:
            print(f"  {C.GREEN}{entry['ans'][0]:<22}{C.RESET} {C.DIM}- {entry['hint']}{C.RESET}")
            print(f"  {' ' * 22}  {C.WHITE}{textwrap.fill(entry['why'], width=65, subsequent_indent=' '*24)}{C.RESET}")
    input(C.DIM + "\nPress Enter to go back..." + C.RESET)


def show_profile(profiles, player):
    p = profiles[player]
    clear()
    print(C.CYAN + C.BOLD + f"\n=== PROFILE: {player} ===" + C.RESET + "\n")
    print(f"Games played:   {p['games']}")
    print(f"Correct / Wrong: {C.GREEN}{p['total_correct']}{C.RESET} / {C.RED}{p['total_wrong']}{C.RESET}")
    acc = 0 if (p['total_correct']+p['total_wrong']) == 0 else round(100*p['total_correct']/(p['total_correct']+p['total_wrong']))
    print(f"Accuracy:       {acc}%")
    print(f"Best score:     {C.YELLOW}{p['best_score']}{C.RESET}  ({rank_for_score(p['best_score'])})")
    print(f"Best streak:    {p['best_streak']}")
    print(f"\n{C.BOLD}Achievements ({len(p['achievements'])}/{len(ACHIEVEMENTS)}):{C.RESET}")
    unlocked_ids = set(p["achievements"])
    for a in ACHIEVEMENTS:
        tag = f"{C.GREEN}✔{C.RESET}" if a["id"] in unlocked_ids else f"{C.DIM}✘{C.RESET}"
        print(f"  {tag} {C.BOLD}{a['name']}{C.RESET} {C.DIM}- {a['desc']}{C.RESET}")
    input(C.DIM + "\nPress Enter to go back..." + C.RESET)


# --------------------------------------------------------------------------
# ROUND LOGIC (shared by all modes)
# --------------------------------------------------------------------------

def play_round(entry, tier, sound, allow_hint_skip=True):
    """Returns (points_or_None, elapsed_seconds, hint_used_bool)."""
    print(f"{C.MAGENTA}[{entry['cat']}]{C.RESET} " + C.BOLD + f"Tier {tier} Mission:" + C.RESET)
    print(textwrap.fill(f'"{entry["hint"]}"', width=70))
    if allow_hint_skip:
        print(C.DIM + "(type 'hint' for a clue, -5 pts | 'skip' to forfeit, -1 life)" + C.RESET)

    hint_used = False
    start = time.time()
    user_input = input(C.CYAN + "root@runner:~$ " + C.RESET).strip()
    elapsed = time.time() - start

    hint_penalty = 0
    while allow_hint_skip and user_input.lower() == "hint":
        reveal = entry["ans"][0][: max(2, len(entry["ans"][0]) // 2)]
        print(C.YELLOW + f"Hint: starts with '{reveal}...'" + C.RESET)
        hint_penalty = 5
        hint_used = True
        start = time.time()
        user_input = input(C.CYAN + "root@runner:~$ " + C.RESET).strip()
        elapsed = time.time() - start

    if allow_hint_skip and user_input.lower() == "skip":
        beep(sound)
        print(C.RED + f"Skipped. Correct command: {C.BOLD}{entry['ans'][0]}{C.RESET}")
        print(C.DIM + f"Why: {entry['why']}" + C.RESET)
        return None, elapsed, hint_used

    correct = any(user_input.lower() == a.lower() for a in entry["ans"])

    if correct:
        base = 10 * entry["diff"]
        if elapsed <= TIME_FAST:
            bonus, tag = 15, "LIGHTNING FAST"
        elif elapsed <= TIME_OK:
            bonus, tag = 5, "Solid pace"
        else:
            bonus, tag = 0, "Correct"
        points = max(0, base + bonus - hint_penalty)
        beep(sound)
        print(C.GREEN + C.BOLD + f"✔ {tag}! +{points} pts" + C.RESET)
        print(C.DIM + f"Why: {entry['why']}" + C.RESET)
        return points, elapsed, hint_used
    else:
        beep(sound)
        print(C.RED + C.BOLD + f"✘ WRONG." + C.RESET + f" You typed: {C.DIM}{user_input or '(nothing)'}{C.RESET}")
        print(C.RED + f"Correct command: {C.BOLD}{entry['ans'][0]}{C.RESET}")
        print(C.YELLOW + f"Explanation: {entry['why']}" + C.RESET)
        return None, elapsed, hint_used


def status_bar(player, score, lives, streak, mode_label):
    hearts = "❤ " * lives if lives is not None else ""
    fire = ("🔥" * min(streak, 10)) if streak > 0 else ""
    print(C.BOLD + C.WHITE + f"[{mode_label}] Player: {player}   " + C.RESET +
          C.GREEN + f"Score: {score}   " + C.RESET +
          (C.RED + f"Lives: {hearts}   " + C.RESET if lives is not None else "") +
          C.YELLOW + f"Streak: {streak} {fire}" + C.RESET)
    print(C.DIM + "-" * 60 + C.RESET)


# --------------------------------------------------------------------------
# MODE: SURVIVAL
# --------------------------------------------------------------------------

def mode_survival(player, profiles, sound):
    score = 0
    lives = LIVES_START
    streak = 0
    max_streak = 0
    lightning_streak = 0
    max_lightning_streak = 0
    hints_used = 0
    comeback_pts = 0
    on_last_life_flag = False

    pool = COMMANDS.copy()
    random.shuffle(pool)
    idx = 0

    while lives > 0:
        if idx >= len(pool):
            random.shuffle(pool)
            idx = 0

        tier = 1 if score < 100 else 2 if score < 400 else 3
        candidates = [e for e in pool if e["diff"] <= tier] or pool
        entry = random.choice(candidates)

        clear()
        status_bar(player, score, lives, streak, "SURVIVAL")

        if lives == 1:
            on_last_life_flag = True

        result, elapsed, hint_used = play_round(entry, tier, sound)
        idx += 1
        if hint_used:
            hints_used += 1

        if result is None:
            lives -= 1
            streak = 0
            lightning_streak = 0
            profiles[player]["total_wrong"] += 1
        else:
            streak += 1
            max_streak = max(max_streak, streak)
            if elapsed <= TIME_FAST:
                lightning_streak += 1
                max_lightning_streak = max(max_lightning_streak, lightning_streak)
            else:
                lightning_streak = 0
            streak_bonus = min(streak, 10) * 2
            gained = result + streak_bonus
            score += gained
            if on_last_life_flag:
                comeback_pts += gained
            if streak_bonus:
                print(C.MAGENTA + f"🔥 Streak bonus: +{streak_bonus}" + C.RESET)
            profiles[player]["total_correct"] += 1

        time.sleep(1.1)

    clear()
    print(C.RED + C.BOLD + "\n GAME OVER \n" + C.RESET)
    print(f"Final Score: {C.GREEN}{score}{C.RESET}")
    print(f"Rank Achieved: {C.YELLOW}{C.BOLD}{rank_for_score(score)}{C.RESET}\n")

    save_score(player, score, "survival")
    profiles[player]["games"] += 1
    profiles[player]["best_score"] = max(profiles[player]["best_score"], score)
    profiles[player]["best_streak"] = max(profiles[player]["best_streak"], max_streak)

    state = dict(mode="survival", score=score, max_streak=max_streak,
                 max_lightning_streak=max_lightning_streak, hints_used=hints_used,
                 comeback_pts=comeback_pts)
    newly = check_achievements(state, profiles, player)
    save_profile(profiles)
    announce_achievements(newly)
    input(C.DIM + "Press Enter to return to menu..." + C.RESET)


# --------------------------------------------------------------------------
# MODE: DAILY CHALLENGE  (same 10 questions for everyone, every day)
# --------------------------------------------------------------------------

def mode_daily(player, profiles, sound):
    seed = date.today().isoformat()
    rng = random.Random(seed)
    daily_set = rng.sample(COMMANDS, min(10, len(COMMANDS)))

    score = 0
    correct_count = 0
    for i, entry in enumerate(daily_set, 1):
        clear()
        print(C.BLUE + C.BOLD + f"=== DAILY CHALLENGE ({seed}) — Question {i}/{len(daily_set)} ===" + C.RESET)
        status_bar(player, score, None, correct_count, "DAILY")
        result, elapsed, _ = play_round(entry, entry["diff"], sound, allow_hint_skip=False)
        if result is not None:
            score += result
            correct_count += 1
            profiles[player]["total_correct"] += 1
        else:
            profiles[player]["total_wrong"] += 1
        time.sleep(1.1)

    clear()
    print(C.BLUE + C.BOLD + "\n DAILY CHALLENGE COMPLETE \n" + C.RESET)
    print(f"Score: {C.GREEN}{score}{C.RESET}   Correct: {correct_count}/{len(daily_set)}")
    save_score(player, score, "daily")
    profiles[player]["games"] += 1
    profiles[player]["best_score"] = max(profiles[player]["best_score"], score)
    state = dict(mode="daily", score=score)
    newly = check_achievements(state, profiles, player)
    save_profile(profiles)
    announce_achievements(newly)
    input(C.DIM + "\nPress Enter to return to menu..." + C.RESET)


# --------------------------------------------------------------------------
# MODE: BOSS RUSH  (5 rapid-fire, no hints, no skips, perfect-run bonus)
# --------------------------------------------------------------------------

def mode_boss(player, profiles, sound):
    clear()
    print(C.ORANGE + C.BOLD + textwrap.dedent("""
        ⚔  BOSS RUSH INCOMING  ⚔
        5 commands. No hints. No skips. No mercy.
        Clear all 5 for a massive perfect-run bonus.
    """) + C.RESET)
    input(C.DIM + "Press Enter when ready..." + C.RESET)

    pool = [e for e in COMMANDS if e["diff"] >= 2]
    boss_set = random.sample(pool, min(5, len(pool)))
    score = 0
    correct_count = 0
    total_time = 0.0

    for i, entry in enumerate(boss_set, 1):
        clear()
        print(C.ORANGE + C.BOLD + f"=== BOSS RUSH — {i}/{len(boss_set)} ===" + C.RESET)
        status_bar(player, score, None, correct_count, "BOSS")
        result, elapsed, _ = play_round(entry, entry["diff"], sound, allow_hint_skip=False)
        total_time += elapsed
        if result is not None:
            score += result
            correct_count += 1
            profiles[player]["total_correct"] += 1
        else:
            profiles[player]["total_wrong"] += 1
        time.sleep(1.0)

    perfect = correct_count == len(boss_set)
    if perfect:
        bonus = 100
        score += bonus
        print(C.GREEN + C.BOLD + f"\n🏆 PERFECT CLEAR! +{bonus} bonus pts" + C.RESET)

    clear()
    print(C.ORANGE + C.BOLD + "\n BOSS RUSH COMPLETE \n" + C.RESET)
    print(f"Score: {C.GREEN}{score}{C.RESET}   Hits: {correct_count}/{len(boss_set)}   Time: {total_time:.1f}s")
    save_score(player, score, "boss")
    profiles[player]["games"] += 1
    profiles[player]["best_score"] = max(profiles[player]["best_score"], score)
    state = dict(mode="boss", score=score, boss_perfect=perfect)
    newly = check_achievements(state, profiles, player)
    save_profile(profiles)
    announce_achievements(newly)
    input(C.DIM + "\nPress Enter to return to menu..." + C.RESET)


def announce_achievements(newly):
    if not newly:
        return
    print(C.MAGENTA + C.BOLD + "\n★ ACHIEVEMENT(S) UNLOCKED ★" + C.RESET)
    for a in newly:
        print(f"  {C.YELLOW}🏅 {a['name']}{C.RESET} - {C.DIM}{a['desc']}{C.RESET}")


# --------------------------------------------------------------------------
# MENU
# --------------------------------------------------------------------------

def settings_menu(sound):
    clear()
    print(C.CYAN + C.BOLD + "\n=== SETTINGS ===" + C.RESET)
    print(f"Sound (terminal bell on answer): {'ON' if sound else 'OFF'}")
    print(f"  {C.CYAN}[1]{C.RESET} Toggle sound   {C.CYAN}[2]{C.RESET} Back")
    choice = input(C.YELLOW + "> " + C.RESET).strip()
    if choice == "1":
        return not sound
    return sound


def main_menu():
    sound = True
    while True:
        clear()
        print(C.GREEN + C.BOLD + BANNER + C.RESET)
        print(C.DIM + "  The one-and-only command-mastery roguelike for your terminal" + C.RESET)
        print()
        print(f"  {C.CYAN}[1]{C.RESET} Survival Mode")
        print(f"  {C.CYAN}[2]{C.RESET} Daily Challenge")
        print(f"  {C.CYAN}[3]{C.RESET} Boss Rush")
        print(f"  {C.CYAN}[4]{C.RESET} Study / Cheat Sheet")
        print(f"  {C.CYAN}[5]{C.RESET} Leaderboards")
        print(f"  {C.CYAN}[6]{C.RESET} Profile & Achievements")
        print(f"  {C.CYAN}[7]{C.RESET} Settings")
        print(f"  {C.CYAN}[8]{C.RESET} Quit")
        choice = input(C.YELLOW + "\n> " + C.RESET).strip()

        if choice in ("1", "2", "3", "4", "6"):
            name = input(C.CYAN + "Enter your codename: " + C.RESET).strip() or "Anon"
            profiles = get_profile(name)
            save_profile(profiles)
            if choice == "1":
                mode_survival(name, profiles, sound)
            elif choice == "2":
                mode_daily(name, profiles, sound)
            elif choice == "3":
                mode_boss(name, profiles, sound)
            elif choice == "4":
                show_study_mode(profiles, name)
            elif choice == "6":
                show_profile(profiles, name)
        elif choice == "5":
            show_leaderboard()
        elif choice == "7":
            sound = settings_menu(sound)
        elif choice == "8":
            clear()
            print(C.GREEN + "Stay rooted. o/" + C.RESET)
            sys.exit(0)
        else:
            continue


if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(C.RED + "\n\nInterrupted. Exiting RootRunner." + C.RESET)
        sys.exit(0)
