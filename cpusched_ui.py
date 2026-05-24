from tkinter import *

window = Tk()
window.title("CPU Scheduling Simulator")
window.geometry("900x700")
window.config(bg="#1e1e2f")

# MAIN PAGE
page1 = Frame(window, bg="#1e1e2f")
page1.pack(fill="both", expand=True)

# TITLE
title = Label(
    page1,
    text="CPU Scheduling Simulator",
    font=("Verdana", 18, "bold"),
    bg="#1e1e2f",
    fg="white"
)

title.pack(pady=10)

# TOP INPUT
top_frame = Frame(page1, bg="#2d2d44")
top_frame.pack(pady=10)

Label(
    top_frame,
    text="Number of Processes:",
    font=("Arial", 12),
    bg="#2d2d44",
    fg="white"
).grid(row=0, column=0, padx=5, pady=5)

Entry(top_frame).grid(row=0, column=1, padx=10, pady=10)

# PROCESS TABLE FRAME
process_frame = Frame(page1, bg="#2d2d44")

# RESULT + GANTT SECTION
bottom_frame = Frame(page1, bg="#1e1e2f")

# RESULT FRAME
result_frame = Frame(
    bottom_frame,
    bg="#2d2d44",
    width=250,
    height=200
)

result_frame.pack(side=LEFT, padx=20)
result_frame.pack_propagate(False)

# GANTT FRAME
gantt_frame = Frame(
    bottom_frame,
    bg="#2d2d44",
    width=400,
    height=200
)

gantt_frame.pack(side=RIGHT, padx=20)
gantt_frame.pack_propagate(False)

# RESULT CONTENT
Label(
    result_frame,
    text="Simulation Results",
    font=("Arial", 12, "bold"),
    bg="#2d2d44",
    fg="white"
).pack(pady=10)

Label(
    result_frame,
    text="Average Waiting Time:",
    bg="#2d2d44",
    fg="white"
).pack(pady=5)

Label(
    result_frame,
    text="Average Turnaround Time:",
    bg="#2d2d44",
    fg="white"
).pack(pady=5)

# GANTT CONTENT
Label(
    gantt_frame,
    text="Gantt Chart Area",
    font=("Arial", 12, "bold"),
    bg="#2d2d44",
    fg="white"
).pack(pady=10)

Label(
    gantt_frame,
    text="[ Chart will appear here ]",
    bg="#2d2d44",
    fg="white",
    width=35,
    height=8
).pack(pady=20)

# SHOW RESULTS FUNCTION
def show_results():
    bottom_frame.pack(pady=20)

# CREATE FIELDS FUNCTION
def create_fields():

    create_button.config(state=DISABLED)

    process_frame.pack(pady=10)

    # HEADERS
    Label(
        process_frame,
        text="Process",
        bg="#2d2d44",
        fg="white"
    ).grid(row=0, column=0, padx=10, pady=10)

    Label(
        process_frame,
        text="Arrival Time",
        bg="#2d2d44",
        fg="white"
    ).grid(row=0, column=1, padx=10, pady=10)

    Label(
        process_frame,
        text="Burst Time",
        bg="#2d2d44",
        fg="white"
    ).grid(row=0, column=2, padx=10, pady=10)

    Label(
        process_frame,
        text="Priority",
        bg="#2d2d44",
        fg="white"
    ).grid(row=0, column=3, padx=10, pady=10)

    # P1
    Label(
        process_frame,
        text="P1",
        bg="#2d2d44",
        fg="white"
    ).grid(row=1, column=0, padx=10, pady=10)

    Entry(process_frame).grid(row=1, column=1, padx=10, pady=10)
    Entry(process_frame).grid(row=1, column=2, padx=10, pady=10)
    Entry(process_frame).grid(row=1, column=3, padx=10, pady=10)

    # P2
    Label(
        process_frame,
        text="P2",
        bg="#2d2d44",
        fg="white"
    ).grid(row=2, column=0, padx=10, pady=10)

    Entry(process_frame).grid(row=2, column=1, padx=10, pady=10)
    Entry(process_frame).grid(row=2, column=2, padx=10, pady=10)
    Entry(process_frame).grid(row=2, column=3, padx=10, pady=10)

    # P3
    Label(
        process_frame,
        text="P3",
        bg="#2d2d44",
        fg="white"
    ).grid(row=3, column=0, padx=10, pady=10)

    Entry(process_frame).grid(row=3, column=1, padx=10, pady=10)
    Entry(process_frame).grid(row=3, column=2, padx=10, pady=10)
    Entry(process_frame).grid(row=3, column=3, padx=10, pady=10)

    # P4
    Label(
        process_frame,
        text="P4",
        bg="#2d2d44",
        fg="white"
    ).grid(row=4, column=0, padx=10, pady=10)

    Entry(process_frame).grid(row=4, column=1, padx=10, pady=10)
    Entry(process_frame).grid(row=4, column=2, padx=10, pady=10)
    Entry(process_frame).grid(row=4, column=3, padx=10, pady=10)

    # CONTROL FRAME
    control_frame = Frame(page1, bg="#1e1e2f")
    control_frame.pack(pady=20)

    # SMART ADVISOR BUTTON
    Button(
        control_frame,
        text="Recommend Best Algorithm:",
        font=("Arial", 10, "bold"),
        bg="#00b894",
        fg="white"
    ).grid(row=0, column=0, columnspan=4, pady=10)

    # ALGORITHM BUTTONS
    Button(
        control_frame,
        text="FCFS",
        bg="#5b6ee1",
        width=10
    ).grid(row=1, column=0, padx=5)

    Button(
        control_frame,
        text="SJF",
        bg="#5b6ee1",
        width=10
    ).grid(row=1, column=1, padx=5)

    Button(
        control_frame,
        text="Priority",
        bg="#5b6ee1",
        width=10
    ).grid(row=1, column=2, padx=5)

    Button(
        control_frame,
        text="Round Robin",
        bg="#5b6ee1",
        width=12
    ).grid(row=1, column=3, padx=5)

    # RUN BUTTON
    Button(
        control_frame,
        text="Run Simulation",
        width=15,
        bg="#5c2eb3",
        fg="white",
        command=show_results
    ).grid(row=2, column=0, columnspan=4, pady=20)

# CREATE PROCESS BUTTON
create_button = Button(
    page1,
    text="Create Process Fields",
    bg="#5c2eb3",
    fg="white",
    width=20,
    command=create_fields
)

create_button.pack(pady=10)

window.mainloop()