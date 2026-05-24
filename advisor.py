import matplotlib.pyplot as plt

# -----------------------------
# Get User Input
# -----------------------------
def get_user_input():
    n = int(input("Enter number of processes: "))
    processes = []
    for i in range(n):
        pid = f"P{i+1}"
        arrival = int(input(f"Arrival time for {pid}: "))
        burst = int(input(f"Burst time for {pid}: "))
        priority = int(input(f"Priority for {pid}: "))
        processes.append({"pid": pid, "arrival": arrival, "burst": burst, "priority": priority})
    return processes

# -----------------------------
# FCFS Scheduling
# -----------------------------
def fcfs(processes):
    processes = sorted(processes, key=lambda x: x['arrival'])
    current_time = 0
    waiting, turnaround = [], []

    for p in processes:
        if current_time < p['arrival']:
            current_time = p['arrival']
        wait = current_time - p['arrival']
        current_time += p['burst']
        tat = current_time - p['arrival']
        waiting.append(wait)
        turnaround.append(tat)

    return sum(waiting)/len(waiting), sum(turnaround)/len(turnaround)

# -----------------------------
# SJF Scheduling
# -----------------------------
def sjf(processes):
    processes = sorted(processes, key=lambda x: (x['arrival'], x['burst']))
    current_time = 0
    waiting, turnaround = [], []
    ready = []

    while processes or ready:
        while processes and processes[0]['arrival'] <= current_time:
            ready.append(processes.pop(0))
        if ready:
            ready.sort(key=lambda x: x['burst'])
            p = ready.pop(0)
            wait = current_time - p['arrival']
            current_time += p['burst']
            tat = current_time - p['arrival']
            waiting.append(wait)
            turnaround.append(tat)
        else:
            current_time = processes[0]['arrival']

    return sum(waiting)/len(waiting), sum(turnaround)/len(turnaround)

# -----------------------------
# Priority Scheduling
# -----------------------------
def priority(processes):
    processes = sorted(processes, key=lambda x: (x['arrival'], x['priority']))
    current_time = 0
    waiting, turnaround = [], []
    ready = []

    while processes or ready:
        while processes and processes[0]['arrival'] <= current_time:
            ready.append(processes.pop(0))
        if ready:
            ready.sort(key=lambda x: x['priority'])
            p = ready.pop(0)
            wait = current_time - p['arrival']
            current_time += p['burst']
            tat = current_time - p['arrival']
            waiting.append(wait)
            turnaround.append(tat)
        else:
            current_time = processes[0]['arrival']

    return sum(waiting)/len(waiting), sum(turnaround)/len(turnaround)

# -----------------------------
# Round Robin Scheduling
# -----------------------------
def round_robin(processes, quantum=4):
    queue = sorted(processes, key=lambda x: x['arrival'])
    current_time = 0
    waiting, turnaround = {}, {}
    ready = []

    while queue or ready:
        while queue and queue[0]['arrival'] <= current_time:
            ready.append(queue.pop(0))
        if ready:
            p = ready.pop(0)
            if 'remaining' not in p:
                p['remaining'] = p['burst']
            run_time = min(quantum, p['remaining'])
            p['remaining'] -= run_time
            current_time += run_time
            if p['remaining'] > 0:
                ready.append(p)
            else:
                tat = current_time - p['arrival']
                turnaround[p['pid']] = tat
                waiting[p['pid']] = tat - p['burst']
        else:
            current_time = queue[0]['arrival']

    return sum(waiting.values())/len(waiting), sum(turnaround.values())/len(turnaround)

# -----------------------------
# Smart Advisor
# -----------------------------
def smart_advisor(processes):
    results = {
        "FCFS": fcfs(processes.copy()),
        "SJF": sjf(processes.copy()),
        "Priority": priority(processes.copy()),
        "Round Robin": round_robin(processes.copy(), quantum=4)
    }

    # Improved recommendation logic: lowest combined waiting + turnaround time
    best_algo = min(results, key=lambda k: (results[k][0] + results[k][1]))

    print("\n--- Algorithm Performance ---")
    for algo, (awt, att) in results.items():
        print(f"{algo}: Avg Waiting = {awt:.2f}, Avg Turnaround = {att:.2f}")
    print(f"\n✅ Recommended Algorithm: {best_algo}\n")

    return best_algo, results

# -----------------------------
# Visualization
# -----------------------------
def visualize(results):
    algos = list(results.keys())
    awt = [results[a][0] for a in algos]
    att = [results[a][1] for a in algos]

    plt.bar(algos, awt, color='blue', label='Avg Waiting Time')
    plt.bar(algos, att, color='orange', alpha=0.6, label='Avg Turnaround Time')
    plt.legend()
    plt.title("CPU Scheduling Algorithm Comparison")
    plt.show()

# -----------------------------
# Run Everything
# -----------------------------
if __name__ == "__main__":
    processes = get_user_input()
    best, results = smart_advisor(processes)
    visualize(results)
