# Student Grade Manager with Streamlit
#
# Streamlit turns a normal Python script into a web page.
# Every st.something(...) call draws one thing on the page:
# a title, a text box, a button, a table, a chart...
#
# IMPORTANT idea: every time you click a button or type something,
# Streamlit runs this whole file again from top to bottom.
# Normal variables would be reset each time, so we keep our student list
# inside st.session_state, which remembers values between those runs.
#
# Run it with:   streamlit run app.py

import streamlit as st

# Page settings - shown in the browser tab.
st.set_page_config(page_title="Student Grade Manager", page_icon="🎓")


# ---------------------------------------------------------------------------
# Helper functions (plain Python, nothing Streamlit-specific)
# ---------------------------------------------------------------------------

def get_grade(mark):
    """Turn a mark (0-100) into a grade letter."""
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


def name_exists(name):
    """Return True if a student with this name is already in the list."""
    for student in st.session_state.students:
        if student["name"].lower() == name.lower():
            return True
    return False


# ---------------------------------------------------------------------------
# Remember the students between reruns
# ---------------------------------------------------------------------------
# The first time the page loads, "students" is not in session_state yet,
# so we create an empty list. On later runs we leave it alone.

if "students" not in st.session_state:
    st.session_state.students = []  # each item: {"name": "Asha", "mark": 85.0}


# ---------------------------------------------------------------------------
# Page heading
# ---------------------------------------------------------------------------

st.title("🎓 Student Grade Manager")
st.write("Add students and their marks. Grades and class results update automatically.")


# ---------------------------------------------------------------------------
# 1. Add a student
# ---------------------------------------------------------------------------
# A form groups inputs together, so the page only reruns when
# the submit button is pressed (not on every key you type).
# clear_on_submit=True empties the boxes after adding.

st.header("Add a student")

with st.form("add_student_form", clear_on_submit=True):
    name = st.text_input("Student name")
    # number_input only allows numbers, and min/max keep the mark in 0-100.
    mark = st.number_input("Mark (0-100)", min_value=0.0, max_value=100.0, step=1.0)
    submitted = st.form_submit_button("Add student")

# This part runs only on the rerun where the button was clicked.
if submitted:
    name = name.strip()  # remove spaces at the start and end

    if name == "":
        st.error("Name cannot be empty.")
    elif name_exists(name):
        st.warning(f"'{name}' is already in the list.")
    else:
        st.session_state.students.append({"name": name, "mark": mark})
        st.success(f"Added {name} - Mark: {mark:.1f}, Grade: {get_grade(mark)}")


# ---------------------------------------------------------------------------
# 2. Results table and class summary
# ---------------------------------------------------------------------------

st.header("Results")

students = st.session_state.students

if len(students) == 0:
    st.info("No students added yet. Use the form above to add one.")
else:
    # Build the rows for the table: one dictionary per student.
    rows = []
    for student in students:
        rows.append({
            "Name": student["name"],
            "Mark": student["mark"],
            "Grade": get_grade(student["mark"]),
        })

    st.dataframe(rows, hide_index=True, width="stretch")

    # Class summary - same maths as the terminal version.
    marks = [student["mark"] for student in students]
    average = sum(marks) / len(marks)
    highest = max(marks)
    lowest = min(marks)

    # st.columns puts things side by side; st.metric shows a big number.
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Students", len(students))
    col2.metric("Average", f"{average:.1f}")
    col3.metric("Highest", f"{highest:.0f}")
    col4.metric("Lowest", f"{lowest:.0f}")

    # -----------------------------------------------------------------------
    # 3. How many students got each grade
    # -----------------------------------------------------------------------
    st.subheader("Grade count")

    grade_letters = ["A", "B", "C", "D", "E"]
    counts = []
    for letter in grade_letters:
        count = 0
        for student in students:
            if get_grade(student["mark"]) == letter:
                count = count + 1
        counts.append(count)

    st.bar_chart({"Grade": grade_letters, "Students": counts}, x="Grade", y="Students")

    # -----------------------------------------------------------------------
    # 4. Remove a student, or clear everyone
    # -----------------------------------------------------------------------
    st.header("Remove students")

    all_names = [student["name"] for student in students]
    to_remove = st.selectbox("Choose a student", all_names)

    left, right = st.columns(2)

    if left.button("Remove selected student"):
        # Keep every student except the chosen one.
        st.session_state.students = [s for s in students if s["name"] != to_remove]
        st.rerun()  # run the script again so the table updates straight away

    if right.button("Clear all students"):
        st.session_state.students = []
        st.rerun()
