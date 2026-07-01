# tracker.py
import datetime

def daily_checkin():
    date = datetime.date.today().isoformat()
    print(f"Founder's Log — {date}")
    thread = input("What loose thread tugged at you today? ")
    knot = input("What minimal authentic knot did you tie (or will you tie)? ")
    degraded = input("Did you degrade your signal today? (y/n) ").lower() == 'y'
    with open("sovereignty_log.txt", "a") as f:
        f.write(f"{date} | Thread: {thread} | Knot: {knot} | Degraded: {degraded}\n")
    print("Logged. Coram te necto.")

if __name__ == "__main__":
    daily_checkin()
