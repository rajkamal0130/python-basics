"""
Grade Manager
Stores students in a list of dicts: [{"name": str, "mark": float}, ...]
Validates marks to 0-100 and handles all bad input gracefully.
"""

students = []


def get_grade(mark):
    if mark >= 90:
        return "A"
    elif mark >= 80:
        return "B"
    elif mark >= 70:
        return "C"
    elif mark >= 60:
        return "D"
    else:
        return "E"


def add_student():
    name = input("  Enter student name: ").strip()
    if not name:
        print("  ⚠  Name cannot be empty.")
        return

    # Check for duplicate
    if any(s["name"].lower() == name.lower() for s in students):
        print(f"  ⚠  '{name}' already exists.")
        return

    while True:
        raw = input(f"  Enter mark for {name} (0–100): ").strip()
        try:
            mark = float(raw)
            if mark < 0 or mark > 100:
                print("  ⚠  Mark must be between 0 and 100.")
            else:
                students.append({"name": name, "mark": mark})
                grade = get_grade(mark)
                print(f"  ✓  Added {name} — Mark: {mark:.1f}, Grade: {grade}")
                break
        except ValueError:
            print(f"  ⚠  '{raw}' is not a valid number. Please try again.")


def show_students():
    if not students:
        print("\n  No students added yet.\n")
        return

    # Column widths
    name_w  = max(len(s["name"]) for s in students)
    name_w  = max(name_w, 4)          # min width = len("Name")
    mark_w  = 6                        # "Mark  "
    grade_w = 5                        # "Grade"

    header = f"  {'Name':<{name_w}}  {'Mark':>{mark_w}}  {'Grade':<{grade_w}}"
    sep    = f"  {'-'*name_w}  {'-'*mark_w}  {'-'*grade_w}"

    print()
    print(header)
    print(sep)
    for s in students:
        grade = get_grade(s["mark"])
        print(f"  {s['name']:<{name_w}}  {s['mark']:>{mark_w}.1f}  {grade:<{grade_w}}")
    print(sep)

    marks   = [s["mark"] for s in students]
    average = sum(marks) / len(marks)
    highest = max(marks)
    lowest  = min(marks)

    print(f"  Average: {average:.1f}    Highest: {highest:.0f}    Lowest: {lowest:.0f}\n")


def menu():
    print("\n========== Grade Manager ==========")
    while True:
        print("\n  1. Add student")
        print("  2. Show results")
        print("  3. Quit")
        choice = input("\n  Your choice: ").strip()

        if choice == "1":
            add_student()
        elif choice == "2":
            show_students()
        elif choice == "3":
            print("\n  Goodbye!\n")
            break
        else:
            print(f"  ⚠  '{choice}' is not a valid option. Please enter 1, 2 or 3.")


if __name__ == "__main__":
    menu()