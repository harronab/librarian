from pathlib import Path
from datetime import datetime
from ui.layout import render_home

def clock_12h():
    # %I is 12-hour with leading zero on Windows; strip it for cleaner look
    t = datetime.now().strftime("%I:%M %p")
    if t.startswith("0"):
        t = t[1:]
    return t

def main():
    labels = ("Check-Out", "Check-In", "View Patron", "Print Due List")
    status = "Ready — tap a function"
    clock = clock_12h()

    img, rects = render_home(labels, status_text=status, clock_text=clock)

    out_dir = Path("build")
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "home.png"
    img.save(out_path)

    print(f"✅ Wrote {out_path.resolve()}")
    for i, r in enumerate(rects, 1):
        print(f"btn{i}: {r}")

if __name__ == "__main__":
    main()
