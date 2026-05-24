# CPU-SCHEDULING-SIMULATOR
## Project Overview
This repository contains a simulator for different CPU scheduling algorithms.  
The goal is to show how each algorithm handles process scheduling and to compare their performance in terms of waiting time and turnaround time.

## Implemented Algorithms
- First Come First Serve (FCFS)
- Shortest Job First (SJF)
- Priority Scheduling
- Round Robin

Each algorithm is coded separately, and the **Smart Advisor** module runs all of them, compares the results, and recommends the most suitable one for the given set of processes.

## Features
- Interactive input: users can enter arrival time, burst time, and priority for each process.
- Automatic calculation of:
  - Average Waiting Time (AWT)
  - Average Turnaround Time (ATT)
- Advisor logic that suggests the best algorithm based on results.
- Graphical comparison using Matplotlib.

## How to Run
1. Make sure Python 3.14 is installed on your system.
2. Install the required library:
   ```bash
   python -m pip install matplotlib
