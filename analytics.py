import tkinter as tk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import pandas as pd

# Function to load and process grades and ECA data
def load_data():
    try:
        grades_df = pd.read_csv("grades.txt", sep=":", header=None, names=["username", "grades"])
        eca_df = pd.read_csv("eca.txt", sep=":", header=None, names=["username", "activities"])
    except FileNotFoundError:
        messagebox.showerror("Data Error", "Required data files not found.")
        return None, None

    # Process grades
    grades_df["grades"] = grades_df["grades"].apply(lambda g: list(map(int, g.split(","))))
    grades_df[["sub1", "sub2", "sub3", "sub4", "sub5"]] = pd.DataFrame(grades_df["grades"].tolist(), index=grades_df.index)
    grades_df["average"] = grades_df[["sub1", "sub2", "sub3", "sub4", "sub5"]].mean(axis=1)

    # Process ECA
    eca_df["activities"] = eca_df["activities"].astype(str)
    eca_df["activity_count"] = eca_df["activities"].apply(lambda x: len(x.split(",")) if x.strip() else 0)

    return grades_df, eca_df

# Function to show grade trends in the GUI
def show_grade_trends(grades_df, window):
    subject_cols = ["sub1", "sub2", "sub3", "sub4", "sub5"]
    subject_means = grades_df[subject_cols].mean()
    
    fig1 = plt.Figure(figsize=(4, 3), dpi=100)
    ax1 = fig1.add_subplot(111)
    ax1.bar(subject_cols, subject_means, color="skyblue")
    ax1.set_title("Average Grades Per Subject")
    ax1.set_ylabel("Average")
    ax1.set_ylim(0, 100)
    
    canvas1 = FigureCanvasTkAgg(fig1, master=window)
    canvas1.draw()
    canvas1.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Function to show ECA vs performance correlation in the GUI
def show_eca_correlation(grades_df, eca_df, window):
    merged_df = pd.merge(grades_df[["username", "average"]], eca_df[["username", "activity_count"]], on="username")
    
    fig2 = plt.Figure(figsize=(4, 3), dpi=100)
    ax2 = fig2.add_subplot(111)
    ax2.scatter(merged_df["activity_count"], merged_df["average"], c="green", edgecolors="black")
    ax2.set_title("ECA Activity Count vs Average Grade")
    ax2.set_xlabel("Activity Count")
    ax2.set_ylabel("Average Grade")
    ax2.grid(True)
    
    canvas2 = FigureCanvasTkAgg(fig2, master=window)
    canvas2.draw()
    canvas2.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

# Function to show performance alerts
def show_performance_alerts(grades_df, window, threshold=50):
    low_performers = grades_df[grades_df["average"] < threshold]
    if low_performers.empty:
        messagebox.showinfo("Performance Alerts", "No students below the performance threshold.")
    else:
        messagebox.showinfo("Performance Alerts", f"Students Below Threshold:\n{low_performers[['username', 'average']].to_string(index=False)}")

# Main function to run the GUI and analytics dashboard
def run_analytics_dashboard():
    window = tk.Tk()
    window.title("📊 Reports Dashboard")
    window.geometry("900x600")

    # Load data
    grades_df, eca_df = load_data()
    if grades_df is None or eca_df is None:
        window.quit()
        return

    # Create the menu frame
    menu_frame = tk.Frame(window)
    menu_frame.pack(side=tk.TOP, fill=tk.X, pady=10)

    # Create the buttons for analytics
    def show_grades():
        show_grade_trends(grades_df, window)

    def show_eca():
        show_eca_correlation(grades_df, eca_df, window)

    def show_alerts():
        threshold = tk.simpledialog.askinteger("Threshold", "Enter grade threshold (default 50):", parent=window, minvalue=0, maxvalue=100)
        threshold = threshold if threshold is not None else 50
        show_performance_alerts(grades_df, window, threshold)

    def close_dashboard():
        window.destroy()

    grade_button = tk.Button(menu_frame, text="Show Grade Trends", command=show_grades)
    grade_button.pack(side=tk.LEFT, padx=10)

    eca_button = tk.Button(menu_frame, text="ECA vs Performance", command=show_eca)
    eca_button.pack(side=tk.LEFT, padx=10)

    alert_button = tk.Button(menu_frame, text="Performance Alerts", command=show_alerts)
    alert_button.pack(side=tk.LEFT, padx=10)

    close_button = tk.Button(menu_frame, text="Close Dashboard", command=close_dashboard, bg="tomato", fg="white")
    close_button.pack(side=tk.RIGHT, padx=10)

    # Start the GUI
    window.mainloop()


