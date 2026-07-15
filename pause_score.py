import datetime
import os

# Pause Score Tracker
# Companion to the Founder's Sovereignty Equation
# Tracks hooks caught and pauses taken

LOG_FILE = "pause_score_log.txt"

def log_pause_score(hooks, pauses):
    """
    Log a daily pause score entry.
    hooks: total hooks/tugs noticed today
    pauses: total hooks where you paused before acting
    """
    score = (pauses / hooks * 100) if hooks > 0 else 0
    date = datetime.datetime.now().strftime("%Y-%m-%d")
    entry = f"{date} | Hooks: {hooks} | Pauses: {pauses} | Pause%: {score:.1f}\n"

    with open(LOG_FILE, "a") as f:
        f.write(entry)

    print(f"Logged: {entry.strip()}")
    return score

def daily_checkin():
    """
    Interactive daily check-in prompt.
    """
    print("\n--- Pause Score Check-In ---")
    hooks = input("How many hooks/tugs did you notice today? (enter number): ")
    pauses = input("How many did you pause on before acting? (enter number): ")

    try:
        hooks = int(hooks.strip())
        pauses = int(pauses.strip())
    except ValueError:
        print("Please enter valid numbers.")
        return

    score = log_pause_score(hooks, pauses)
    print(f"Pause Score today: {score:.1f}%")

def weekly_review():
    """
    Display a summary of the last 7 days of pause scores.
    """
    if not os.path.exists(LOG_FILE):
        print("No pause score log found.")
        return

    with open(LOG_FILE, "r") as f:
        lines = f.readlines()[-7:]  # last 7 entries

    print("\n--- Weekly Pause Score Review ---")
    for line in lines:
        print(line.strip())

if __name__ == "__main__":
    print("Pause Score Tracker")
    print("1. Daily Check-In")
    print("2. Weekly Review")
    choice = input("Choose an option (1 or 2): ")

    if choice == "1":
        daily_checkin()
    elif choice == "2":
        weekly_review()
    else:
        print("Invalid choice.")
