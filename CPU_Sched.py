import tkinter as tk
from tkinter import ttk, messagebox
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import random


BG_DARK   = "#1a1a2e"
BG_CARD   = "#16213e"
BG_INPUT  = "#0f3460"
ACCENT    = "#533483"
ACCENT2   = "#e94560"
TEXT_W    = "#eaeaea"
TEXT_MUTED= "#8892a4"
SUCCESS   = "#0d7377"
WARNING   = "#f5a623"

PROC_COLORS = [
    "#7b5ea7","#2d6a4f","#c0392b","#1a6985",
    "#c0782a","#2e4053","#6d4c41","#1b5e20",
    "#4a148c","#015355"
]


def fcfs(data):
    d = sorted(data, key=lambda x: x["at"])
    time, chart = 0, []
    for p in d:
        if time < p["at"]:
            time = p["at"]
        chart.append((p["name"], time, time + p["bt"]))
        time += p["bt"]
    return chart


def sjf(data):
    d = sorted(data, key=lambda x: x["at"])
    time, chart, ready = 0, [], []
    while d or ready:
        while d and d[0]["at"] <= time:
            ready.append(d.pop(0))
        if not ready:
            time = d[0]["at"]
            continue
        ready.sort(key=lambda x: x["bt"])
        p = ready.pop(0)
        chart.append((p["name"], time, time + p["bt"]))
        time += p["bt"]
    return chart


def priority_algo(data):
    d = sorted(data, key=lambda x: x["at"])
    time, chart, ready = 0, [], []
    while d or ready:
        while d and d[0]["at"] <= time:
            ready.append(d.pop(0))
        if not ready:
            time = d[0]["at"]
            continue
        ready.sort(key=lambda x: x["pr"])
        p = ready.pop(0)
        chart.append((p["name"], time, time + p["bt"]))
        time += p["bt"]
    return chart


def round_robin(data, quantum):
    queue = sorted(data, key=lambda x: x["at"])
    rem = {p["name"]: p["bt"] for p in data}
    time, chart, ready = 0, [], []
    arrived = 0
    while True:
        while arrived < len(queue) and queue[arrived]["at"] <= time:
            ready.append(dict(queue[arrived]))
            arrived += 1
        if not ready:
            if arrived < len(queue):
                time = queue[arrived]["at"]
                continue
            break
        cur = ready.pop(0)
        exec_t = min(quantum, rem[cur["name"]])
        chart.append((cur["name"], time, time + exec_t))
        time += exec_t
        rem[cur["name"]] -= exec_t
        while arrived < len(queue) and queue[arrived]["at"] <= time:
            ready.append(dict(queue[arrived]))
            arrived += 1
        if rem[cur["name"]] > 0:
            ready.append(cur)
    return chart


def compute_stats(data, chart):
    stats = []
    for p in data:
        segs = [(s, e) for (n, s, e) in chart if n == p["name"]]
        completion = max(e for _, e in segs)
        tat = completion - p["at"]
        wt  = tat - p["bt"]
        stats.append({
            "name": p["name"], "at": p["at"], "bt": p["bt"],
            "completion": completion, "tat": tat, "wt": wt
        })
    return stats


def smart_advisor(data):
    bursts    = [p["bt"] for p in data]
    priorities= [p["pr"] for p in data]
    avg_burst = sum(bursts) / len(bursts)
    burst_var = max(bursts) - min(bursts)
    prior_var = max(priorities) - min(priorities)

    if prior_var > 3:
        return "Priority", "Processes have significantly different priority levels."
    elif burst_var <= 3 and avg_burst <= 6:
        return "SJF", "Burst times are similar and short — SJF minimises average waiting time."
    elif len(data) >= 5:
        return "Round Robin", "Many processes benefit from fair, time-shared scheduling."
    else:
        return "FCFS", "Simple workload with similar burst times — FCFS is efficient here."



class CPUSchedulerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("CPU Scheduling Simulator")
        self.root.geometry("1100x820")
        self.root.configure(bg=BG_DARK)
        self.root.resizable(True, True)

        self.entries     = []   # list of dicts: {name, at, bt, pr}
        self.proc_count  = 0
        self.canvas_widget = None

        self._build_ui()

   

    def _build_ui(self):
        # ── Title bar ──
        title_bar = tk.Frame(self.root, bg=ACCENT, pady=10)
        title_bar.pack(fill="x")
        tk.Label(title_bar, text="⚙  CPU Scheduling Simulator",
                 font=("Segoe UI", 16, "bold"),
                 bg=ACCENT, fg=TEXT_W).pack()

        # ── Main body scrollable canvas ──
        outer = tk.Frame(self.root, bg=BG_DARK)
        outer.pack(fill="both", expand=True, padx=16, pady=12)

        # Left column (config) + Right column (results)
        self.left  = tk.Frame(outer, bg=BG_DARK)
        self.right = tk.Frame(outer, bg=BG_DARK)
        self.left.pack(side="left", fill="y", padx=(0,12))
        self.right.pack(side="left", fill="both", expand=True)

        self._build_left()
        self._build_right()

    def _card(self, parent, title):
        frame = tk.Frame(parent, bg=BG_CARD, padx=14, pady=12,
                         relief="flat", bd=0)
        frame.pack(fill="x", pady=(0, 10))
        if title:
            tk.Label(frame, text=title,
                     font=("Segoe UI", 11, "bold"),
                     bg=BG_CARD, fg=TEXT_W).pack(anchor="w", pady=(0, 8))
        return frame

    def _build_left(self):
        # ── Number of processes ──
        c1 = self._card(self.left, "Setup")
        row = tk.Frame(c1, bg=BG_CARD)
        row.pack(fill="x")
        tk.Label(row, text="Processes (1–10):", bg=BG_CARD,
                 fg=TEXT_MUTED, font=("Segoe UI", 10)).pack(side="left")
        self.n_var = tk.StringVar(value="4")
        e = tk.Entry(row, textvariable=self.n_var, width=5,
                     bg=BG_INPUT, fg=TEXT_W, insertbackground=TEXT_W,
                     relief="flat", font=("Segoe UI", 10))
        e.pack(side="left", padx=8)
        tk.Button(row, text="Generate", command=self._generate,
                  bg=ACCENT, fg=TEXT_W, relief="flat", cursor="hand2",
                  font=("Segoe UI", 9, "bold"), padx=10
                  ).pack(side="left")

       
        self.table_card = self._card(self.left, "Process parameters")
        self._build_table_header()

        self.table_body = tk.Frame(self.table_card, bg=BG_CARD)
        self.table_body.pack(fill="x")

        
        c2 = self._card(self.left, "Round Robin")
        qrow = tk.Frame(c2, bg=BG_CARD)
        qrow.pack(fill="x")
        tk.Label(qrow, text="Time quantum:", bg=BG_CARD,
                 fg=TEXT_MUTED, font=("Segoe UI", 10)).pack(side="left")
        self.q_var = tk.StringVar(value="2")
        tk.Entry(qrow, textvariable=self.q_var, width=5,
                 bg=BG_INPUT, fg=TEXT_W, insertbackground=TEXT_W,
                 relief="flat", font=("Segoe UI", 10)).pack(side="left", padx=8)

        
        c3 = self._card(self.left, "Run algorithm")
        algos = [("FCFS", "#2d6a4f"), ("SJF", "#1a6985"),
                 ("Priority", "#6d4c41"), ("Round Robin", "#7b5ea7")]
        for name, color in algos:
            tk.Button(c3, text=name,
                      command=lambda a=name: self._run(a),
                      bg=color, fg=TEXT_W, relief="flat", cursor="hand2",
                      font=("Segoe UI", 10, "bold"),
                      padx=12, pady=5, width=18
                      ).pack(fill="x", pady=2)

        # Smart advisor
        tk.Button(c3, text="🧠  Smart Advisor",
                  command=self._run_advisor,
                  bg=ACCENT2, fg=TEXT_W, relief="flat", cursor="hand2",
                  font=("Segoe UI", 10, "bold"),
                  padx=12, pady=6, width=18
                  ).pack(fill="x", pady=(8, 2))

        # Advisor output
        self.advisor_var = tk.StringVar(value="")
        self.advisor_lbl = tk.Label(c3, textvariable=self.advisor_var,
                                    bg=BG_CARD, fg=WARNING,
                                    font=("Segoe UI", 9, "italic"),
                                    wraplength=240, justify="left")
        self.advisor_lbl.pack(anchor="w", pady=(4, 0))

    def _build_table_header(self):
        hdr = tk.Frame(self.table_card, bg=BG_INPUT)
        hdr.pack(fill="x", pady=(0, 4))
        for col, w in [("Process", 7), ("Arrival", 7), ("Burst", 7), ("Priority", 7)]:
            tk.Label(hdr, text=col, bg=BG_INPUT, fg=TEXT_W,
                     font=("Segoe UI", 9, "bold"), width=w,
                     pady=3).pack(side="left")

    def _build_right(self):
       
        self.metrics_frame = tk.Frame(self.right, bg=BG_DARK)
        self.metrics_frame.pack(fill="x", pady=(0, 8))

       
        self.gantt_frame = tk.Frame(self.right, bg=BG_CARD,
                                    relief="flat", bd=0)
        self.gantt_frame.pack(fill="both", expand=True, pady=(0, 8))

        tk.Label(self.gantt_frame,
                 text="Run an algorithm to see the Gantt chart",
                 bg=BG_CARD, fg=TEXT_MUTED,
                 font=("Segoe UI", 11, "italic")).pack(expand=True)

       
        self.stats_frame = tk.Frame(self.right, bg=BG_CARD)
        self.stats_frame.pack(fill="x")

   

    def _generate(self):
        try:
            n = int(self.n_var.get())
            if not 1 <= n <= 10:
                raise ValueError
        except ValueError:
            messagebox.showerror("Input error", "Enter a whole number from 1 to 10.")
            return

        for w in self.table_body.winfo_children():
            w.destroy()
        self.entries.clear()
        self.proc_count = n

        for i in range(n):
            row = tk.Frame(self.table_body, bg=BG_CARD)
            row.pack(fill="x", pady=1)

            color = PROC_COLORS[i % len(PROC_COLORS)]
            tk.Label(row, text=f"P{i+1}", bg=color, fg=TEXT_W,
                     font=("Segoe UI", 9, "bold"),
                     width=7, pady=3).pack(side="left")

            at_v = tk.StringVar(value=str(i))
            bt_v = tk.StringVar(value=str(random.randint(1, 8)))
            pr_v = tk.StringVar(value=str(random.randint(1, 5)))

            for var in (at_v, bt_v, pr_v):
                tk.Entry(row, textvariable=var, width=7,
                         bg=BG_INPUT, fg=TEXT_W,
                         insertbackground=TEXT_W,
                         relief="flat",
                         font=("Segoe UI", 9),
                         justify="center").pack(side="left", padx=1)

            self.entries.append({"name": f"P{i+1}",
                                  "at_v": at_v,
                                  "bt_v": bt_v,
                                  "pr_v": pr_v})

        self.advisor_var.set("")
        self._clear_results()

    

    def _collect_data(self):
        data = []
        for i, e in enumerate(self.entries):
            try:
                at = int(e["at_v"].get())
                bt = int(e["bt_v"].get())
                pr = int(e["pr_v"].get())
                if bt < 1:
                    raise ValueError
            except ValueError:
                messagebox.showerror(
                    "Input error",
                    f"P{i+1}: Arrival/Burst/Priority must be integers; Burst ≥ 1.")
                return None
            data.append({"name": e["name"], "at": at, "bt": bt, "pr": pr})
        return data

    

    def _run(self, algo):
        if not self.entries:
            messagebox.showwarning("No processes", "Click 'Generate' first.")
            return
        data = self._collect_data()
        if data is None:
            return

        try:
            q = int(self.q_var.get())
            if q < 1:
                raise ValueError
        except ValueError:
            q = 2

        if algo == "FCFS":
            chart = fcfs(data)
            label = "FCFS"
        elif algo == "SJF":
            chart = sjf(data)
            label = "SJF (Non-preemptive)"
        elif algo == "Priority":
            chart = priority_algo(data)
            label = "Priority (Non-preemptive)"
        else:  # Round Robin
            chart = round_robin(data, q)
            label = f"Round Robin  (q = {q})"

        stats = compute_stats(data, chart)
        self._show_metrics(stats, label)
        self._draw_gantt(chart, data, label)
        self._show_stats_table(stats)

    def _run_advisor(self):
        if not self.entries:
            messagebox.showwarning("No processes", "Click 'Generate' first.")
            return
        data = self._collect_data()
        if data is None:
            return
        rec, reason = smart_advisor(data)
        self.advisor_var.set(f"→ {rec}\n{reason}")
        self._run(rec)

   

    def _clear_results(self):
        for w in self.metrics_frame.winfo_children():
            w.destroy()
        for w in self.gantt_frame.winfo_children():
            w.destroy()
        for w in self.stats_frame.winfo_children():
            w.destroy()
        tk.Label(self.gantt_frame,
                 text="Run an algorithm to see the Gantt chart",
                 bg=BG_CARD, fg=TEXT_MUTED,
                 font=("Segoe UI", 11, "italic")).pack(expand=True)
        if self.canvas_widget:
            plt.close("all")
            self.canvas_widget = None

   

    def _metric_card(self, parent, label, value, color):
        c = tk.Frame(parent, bg=color, padx=14, pady=8)
        c.pack(side="left", padx=5)
        tk.Label(c, text=label, bg=color, fg=TEXT_MUTED,
                 font=("Segoe UI", 9)).pack(anchor="w")
        tk.Label(c, text=value, bg=color, fg=TEXT_W,
                 font=("Segoe UI", 14, "bold")).pack(anchor="w")

    def _show_metrics(self, stats, algo_label):
        for w in self.metrics_frame.winfo_children():
            w.destroy()
        avg_wt  = sum(s["wt"]  for s in stats) / len(stats)
        avg_tat = sum(s["tat"] for s in stats) / len(stats)
        self._metric_card(self.metrics_frame, "Algorithm", algo_label, ACCENT)
        self._metric_card(self.metrics_frame, "Avg waiting time",     f"{avg_wt:.2f}",  SUCCESS)
        self._metric_card(self.metrics_frame, "Avg turnaround time",  f"{avg_tat:.2f}", BG_INPUT)
        self._metric_card(self.metrics_frame, "Processes", str(len(stats)), "#4a148c")

       

    def _draw_gantt(self, chart, data, title):
        for w in self.gantt_frame.winfo_children():
            w.destroy()
        if self.canvas_widget:
            plt.close("all")

        proc_names = [p["name"] for p in data]
        color_map  = {p["name"]: PROC_COLORS[i % len(PROC_COLORS)]
                      for i, p in enumerate(data)}

        height = max(2.2, len(proc_names) * 0.55 + 1.2)
        fig, ax = plt.subplots(figsize=(8, height))
        fig.patch.set_facecolor(BG_CARD)
        ax.set_facecolor(BG_CARD)

        bar_h   = 0.55
        y_pos   = {name: i for i, name in enumerate(proc_names)}

        for (pname, start, end) in chart:
            y = y_pos[pname]
            ax.barh(y, end - start, left=start, height=bar_h,
                    color=color_map[pname], edgecolor="#ffffff20", linewidth=0.5)
            mid = (start + end) / 2
            if end - start > 0.8:
                ax.text(mid, y, f"{end - start}", ha="center", va="center",
                        fontsize=8, color="white", fontweight="bold")

        # Mark time ticks
        all_times = sorted({t for (_, s, e) in chart for t in (s, e)})
        ax.set_xticks(all_times)
        ax.set_xticklabels([str(t) for t in all_times],
                           fontsize=8, color=TEXT_MUTED)
        ax.set_yticks(range(len(proc_names)))
        ax.set_yticklabels(proc_names, fontsize=9, color=TEXT_W)
        ax.set_xlabel("Time", color=TEXT_MUTED, fontsize=9)
        ax.set_title(f"Gantt Chart — {title}",
                     color=TEXT_W, fontsize=10, pad=8)

        for spine in ax.spines.values():
            spine.set_edgecolor("#333355")
        ax.tick_params(colors=TEXT_MUTED)
        ax.grid(axis="x", color="#333355", linestyle="--", linewidth=0.5)
        ax.set_xlim(left=0)

        # Legend
        patches = [mpatches.Patch(color=color_map[p], label=p)
                   for p in proc_names]
        ax.legend(handles=patches, loc="upper right",
                  facecolor=BG_DARK, edgecolor="#333355",
                  labelcolor=TEXT_W, fontsize=8,
                  ncol=min(5, len(proc_names)))

        plt.tight_layout(pad=0.8)

        canvas = FigureCanvasTkAgg(fig, master=self.gantt_frame)
        canvas.draw()
        self.canvas_widget = canvas.get_tk_widget()
        self.canvas_widget.pack(fill="both", expand=True)

    

    def _show_stats_table(self, stats):
        for w in self.stats_frame.winfo_children():
            w.destroy()

        cols = ("Process", "Arrival", "Burst", "Completion",
                "Turnaround", "Waiting")
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("Dark.Treeview",
                        background=BG_CARD, fieldbackground=BG_CARD,
                        foreground=TEXT_W, rowheight=24,
                        font=("Segoe UI", 9))
        style.configure("Dark.Treeview.Heading",
                        background=BG_INPUT, foreground=TEXT_W,
                        font=("Segoe UI", 9, "bold"), relief="flat")
        style.map("Dark.Treeview",
                  background=[("selected", ACCENT)],
                  foreground=[("selected", TEXT_W)])

        tree = ttk.Treeview(self.stats_frame, columns=cols,
                            show="headings", height=len(stats),
                            style="Dark.Treeview")
        for col in cols:
            tree.heading(col, text=col)
            tree.column(col, width=110, anchor="center")

        avg_wt  = sum(s["wt"]  for s in stats) / len(stats)
        avg_tat = sum(s["tat"] for s in stats) / len(stats)

        for i, s in enumerate(stats):
            tag = "even" if i % 2 == 0 else "odd"
            tree.insert("", "end",
                        values=(s["name"], s["at"], s["bt"],
                                s["completion"], s["tat"], s["wt"]),
                        tags=(tag,))
        tree.tag_configure("even", background=BG_CARD)
        tree.tag_configure("odd",  background="#1c2a45")

        # Averages row
        tree.insert("", "end",
                    values=("Average", "—", "—", "—",
                            f"{avg_tat:.2f}", f"{avg_wt:.2f}"),
                    tags=("avg",))
        tree.tag_configure("avg", background=ACCENT, foreground=TEXT_W)

        tree.pack(fill="x", padx=4, pady=4)




if __name__ == "__main__":
    root = tk.Tk()
    app  = CPUSchedulerApp(root)
    root.mainloop()
