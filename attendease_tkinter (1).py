import tkinter as tk
from tkinter import ttk, messagebox
from datetime import date, datetime


class AttendanceApp:
    BG = "#0B1220"
    SIDEBAR = "#111C2F"
    PANEL = "#172338"
    PANEL_LIGHT = "#1D2C45"
    TEXT = "#F4F7FB"
    MUTED = "#91A2B8"
    BLUE = "#3987F5"
    GREEN = "#20B486"
    RED = "#E45B69"
    YELLOW = "#E7AE45"
    BORDER = "#263750"

    def __init__(self, root):
        self.root = root
        self.root.title("AttendEase | Student Attendance System")
        self.root.geometry("1200x760")
        self.root.minsize(980, 650)
        self.root.configure(bg=self.BG)

        # Frontend-only data: stored in memory until the app is closed.
        self.students = []
        self.history = []
        self.current_page = "Dashboard"

        self.setup_style()
        self.build_layout()
        self.show_page("Dashboard")

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=self.PANEL,
            foreground=self.TEXT,
            fieldbackground=self.PANEL,
            rowheight=37,
            borderwidth=0,
            font=("Segoe UI", 10)
        )
        style.configure(
            "Treeview.Heading",
            background=self.PANEL_LIGHT,
            foreground=self.MUTED,
            relief="flat",
            font=("Segoe UI", 9, "bold"),
            padding=(10, 12)
        )
        style.map(
            "Treeview",
            background=[("selected", "#244D80")],
            foreground=[("selected", "#FFFFFF")]
        )
        style.map(
            "Treeview.Heading",
            background=[("active", self.PANEL_LIGHT)]
        )
        style.configure(
            "TNotebook",
            background=self.BG,
            borderwidth=0
        )
        style.configure(
            "TNotebook.Tab",
            background=self.PANEL,
            foreground=self.MUTED,
            padding=(16, 9),
            font=("Segoe UI", 9, "bold")
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", self.BLUE)],
            foreground=[("selected", "#FFFFFF")]
        )

    def build_layout(self):
        self.sidebar = tk.Frame(self.root, bg=self.SIDEBAR, width=225)
        self.sidebar.pack(side="left", fill="y")
        self.sidebar.pack_propagate(False)

        brand = tk.Frame(self.sidebar, bg=self.SIDEBAR)
        brand.pack(fill="x", padx=22, pady=(27, 35))

        tk.Label(
            brand, text="●", fg=self.BLUE, bg=self.SIDEBAR,
            font=("Segoe UI", 23, "bold")
        ).pack(side="left")
        brand_text = tk.Frame(brand, bg=self.SIDEBAR)
        brand_text.pack(side="left", padx=9)
        tk.Label(
            brand_text, text="AttendEase", bg=self.SIDEBAR,
            fg=self.TEXT, font=("Segoe UI", 17, "bold")
        ).pack(anchor="w")
        tk.Label(
            brand_text, text="STUDENT MANAGEMENT", bg=self.SIDEBAR,
            fg=self.MUTED, font=("Segoe UI", 7, "bold")
        ).pack(anchor="w")

        tk.Label(
            self.sidebar, text="MAIN MENU", bg=self.SIDEBAR,
            fg="#657991", font=("Segoe UI", 8, "bold")
        ).pack(anchor="w", padx=23, pady=(0, 10))

        self.nav_buttons = {}
        for name, symbol in [
            ("Dashboard", "▦"),
            ("Attendance", "✓"),
            ("History", "◷"),
            ("Students", "♙"),
        ]:
            button = tk.Button(
                self.sidebar,
                text=f"   {symbol}     {name}",
                anchor="w",
                command=lambda page=name: self.show_page(page),
                bg=self.SIDEBAR,
                fg=self.MUTED,
                activebackground=self.PANEL_LIGHT,
                activeforeground=self.TEXT,
                relief="flat",
                bd=0,
                cursor="hand2",
                font=("Segoe UI", 11),
                padx=15,
                pady=12
            )
            button.pack(fill="x", padx=12, pady=3)
            self.nav_buttons[name] = button

        bottom = tk.Frame(self.sidebar, bg=self.SIDEBAR)
        bottom.pack(side="bottom", fill="x", padx=20, pady=22)
        tk.Frame(bottom, bg=self.BORDER, height=1).pack(fill="x", pady=(0, 14))
        tk.Label(
            bottom, text="AttendEase Desktop", bg=self.SIDEBAR,
            fg=self.MUTED, font=("Segoe UI", 9)
        ).pack(anchor="w")
        tk.Label(
            bottom, text="Frontend project • Tkinter", bg=self.SIDEBAR,
            fg="#657991", font=("Segoe UI", 8)
        ).pack(anchor="w", pady=(4, 0))

        self.main = tk.Frame(self.root, bg=self.BG)
        self.main.pack(side="left", fill="both", expand=True)

        self.header = tk.Frame(self.main, bg=self.BG)
        self.header.pack(fill="x", padx=30, pady=(23, 12))

        self.page_title = tk.Label(
            self.header, text="", bg=self.BG, fg=self.TEXT,
            font=("Segoe UI", 22, "bold")
        )
        self.page_title.pack(side="left")

        self.date_label = tk.Label(
            self.header, text=date.today().strftime("%A, %d %B %Y"),
            bg=self.BG, fg=self.MUTED, font=("Segoe UI", 10)
        )
        self.date_label.pack(side="right", pady=10)

        self.content = tk.Frame(self.main, bg=self.BG)
        self.content.pack(fill="both", expand=True, padx=30, pady=(5, 25))

    # ---------- Reusable UI helpers ----------

    def clear_content(self):
        for widget in self.content.winfo_children():
            widget.destroy()

    def card(self, parent, title, value, subtitle, accent):
        frame = tk.Frame(
            parent, bg=self.PANEL, highlightthickness=1,
            highlightbackground=self.BORDER
        )
        tk.Frame(frame, bg=accent, width=4).pack(side="left", fill="y")
        inner = tk.Frame(frame, bg=self.PANEL)
        inner.pack(side="left", fill="both", expand=True, padx=17, pady=15)

        tk.Label(
            inner, text=title.upper(), bg=self.PANEL, fg=self.MUTED,
            font=("Segoe UI", 8, "bold")
        ).pack(anchor="w")
        tk.Label(
            inner, text=str(value), bg=self.PANEL, fg=self.TEXT,
            font=("Segoe UI", 25, "bold")
        ).pack(anchor="w", pady=(5, 1))
        tk.Label(
            inner, text=subtitle, bg=self.PANEL, fg=self.MUTED,
            font=("Segoe UI", 8)
        ).pack(anchor="w")
        return frame

    def make_button(self, parent, text, command, color=None, width=None):
        return tk.Button(
            parent, text=text, command=command,
            bg=color or self.BLUE, fg="#FFFFFF",
            activebackground=color or self.BLUE,
            activeforeground="#FFFFFF",
            relief="flat", bd=0, cursor="hand2",
            font=("Segoe UI", 9, "bold"),
            padx=15, pady=9, width=width
        )

    def section_title(self, parent, title, subtitle=None):
        frame = tk.Frame(parent, bg=self.BG)
        frame.pack(fill="x", pady=(0, 12))
        tk.Label(
            frame, text=title, bg=self.BG, fg=self.TEXT,
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w")
        if subtitle:
            tk.Label(
                frame, text=subtitle, bg=self.BG, fg=self.MUTED,
                font=("Segoe UI", 9)
            ).pack(anchor="w", pady=(3, 0))
        return frame

    def make_table(self, parent, columns, headings, widths=None):
        wrapper = tk.Frame(parent, bg=self.PANEL)
        wrapper.pack(fill="both", expand=True)
        tree = ttk.Treeview(
            wrapper, columns=columns, show="headings",
            selectmode="browse"
        )
        for i, (column, heading) in enumerate(zip(columns, headings)):
            tree.heading(column, text=heading)
            width = widths[i] if widths else 130
            tree.column(column, width=width, minwidth=70, anchor="w")
        scrollbar = ttk.Scrollbar(
            wrapper, orient="vertical", command=tree.yview
        )
        tree.configure(yscrollcommand=scrollbar.set)
        tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        return tree

    def show_page(self, page):
        self.current_page = page
        for name, button in self.nav_buttons.items():
            button.configure(
                bg=self.PANEL_LIGHT if name == page else self.SIDEBAR,
                fg=self.TEXT if name == page else self.MUTED
            )

        self.clear_content()
        self.page_title.configure(text=page)

        if page == "Dashboard":
            self.build_dashboard()
        elif page == "Attendance":
            self.build_attendance()
        elif page == "History":
            self.build_history()
        elif page == "Students":
            self.build_students()

    # ---------- Dashboard ----------

    def build_dashboard(self):
        total = len(self.students)
        present = sum(s["present"] for s in self.students)
        absent_today = sum(
            1 for s in self.students if s["status"] == "Absent"
        )
        marked_today = sum(
            1 for s in self.students
            if s["status"] in ("Present", "Absent")
        )
        percentage = (present / sum(s["total"] for s in self.students) * 100
                      if sum(s["total"] for s in self.students) else 0)

        cards = tk.Frame(self.content, bg=self.BG)
        cards.pack(fill="x", pady=(3, 23))
        card_data = [
            ("Total students", total, "Registered students", self.BLUE),
            ("Present today", sum(1 for s in self.students if s["status"] == "Present"),
             "Marked present today", self.GREEN),
            ("Absent today", absent_today, "Marked absent today", self.RED),
            ("Overall attendance", f"{percentage:.1f}%",
             f"{marked_today} students marked today", self.YELLOW),
        ]
        for i, data in enumerate(card_data):
            widget = self.card(cards, *data)
            widget.grid(row=0, column=i, sticky="nsew",
                        padx=(0 if i == 0 else 8, 0))
            cards.grid_columnconfigure(i, weight=1, uniform="cards")

        self.section_title(
            self.content, "Today's attendance",
            "A quick overview of the current attendance status."
        )

        table = self.make_table(
            self.content,
            ("name", "status", "present", "total", "percentage"),
            ("STUDENT NAME", "TODAY'S STATUS", "PRESENT", "TOTAL CLASSES", "ATTENDANCE"),
            (220, 150, 100, 130, 130)
        )
        for student in self.students:
            pct = (student["present"] / student["total"] * 100
                   if student["total"] else 0)
            table.insert("", "end", values=(
                student["name"], student["status"],
                student["present"], student["total"], f"{pct:.1f}%"
            ))

        if not self.students:
            self.empty_hint(
                self.content,
                "No students added yet. Open Students to add your first student."
            )

    # ---------- Attendance page ----------

    def build_attendance(self):
        top = tk.Frame(self.content, bg=self.BG)
        top.pack(fill="x", pady=(0, 16))

        tk.Label(
            top, text="Mark attendance for each student.",
            bg=self.BG, fg=self.MUTED, font=("Segoe UI", 10)
        ).pack(side="left")

        self.make_button(
            top, "Mark all present", lambda: self.mark_all("Present"),
            self.GREEN
        ).pack(side="right", padx=(8, 0))
        self.make_button(
            top, "Mark all absent", lambda: self.mark_all("Absent"),
            self.RED
        ).pack(side="right")

        # Attendance date selector (defaults to today's date).
        date_bar = tk.Frame(self.content, bg=self.PANEL,
                            highlightthickness=1, highlightbackground=self.BORDER)
        date_bar.pack(fill="x", pady=(0, 16))
        tk.Label(
            date_bar, text="ATTENDANCE DATE", bg=self.PANEL,
            fg=self.MUTED, font=("Segoe UI", 8, "bold")
        ).pack(side="left", padx=(15, 10), pady=12)
        self.attendance_date_entry = tk.Entry(
            date_bar, bg=self.PANEL_LIGHT, fg=self.TEXT,
            insertbackground=self.TEXT, relief="flat",
            font=("Segoe UI", 10), width=14,
            highlightthickness=1, highlightbackground=self.BORDER
        )
        self.attendance_date_entry.pack(side="left", ipady=6, pady=7)
        self.attendance_date_entry.insert(0, date.today().strftime("%d-%m-%Y"))
        self.make_button(
            date_bar, "Today", self.set_today_date, self.PANEL_LIGHT
        ).pack(side="left", padx=8, pady=7)
        tk.Label(
            date_bar, text="Format: DD-MM-YYYY", bg=self.PANEL,
            fg=self.MUTED, font=("Segoe UI", 8)
        ).pack(side="left", padx=5)

        self.section_title(
            self.content, "Student attendance list",
            "Select a student in the table, then choose Present or Absent."
        )
        self.attendance_tree = self.make_table(
            self.content,
            ("name", "status", "present", "total", "percentage"),
            ("STUDENT NAME", "TODAY'S STATUS", "PRESENT", "TOTAL CLASSES", "ATTENDANCE"),
            (220, 150, 100, 130, 130)
        )
        self.refresh_attendance_table()

        controls = tk.Frame(self.content, bg=self.BG)
        controls.pack(fill="x", pady=15)
        self.make_button(
            controls, "✓  Mark Present",
            lambda: self.mark_selected("Present"), self.GREEN
        ).pack(side="left", padx=(0, 8))
        self.make_button(
            controls, "✕  Mark Absent",
            lambda: self.mark_selected("Absent"), self.RED
        ).pack(side="left", padx=8)
        self.make_button(
            controls, "Save Attendance",
            self.save_attendance, self.BLUE
        ).pack(side="right")

        tk.Label(
            self.content,
            text="Tip: Every student must be marked Present or Absent before saving.",
            bg=self.BG, fg=self.MUTED, font=("Segoe UI", 9)
        ).pack(anchor="w")

    def set_today_date(self):
        if hasattr(self, "attendance_date_entry"):
            self.attendance_date_entry.delete(0, "end")
            self.attendance_date_entry.insert(0, date.today().strftime("%d-%m-%Y"))

    def get_selected_attendance_date(self):
        raw_date = self.attendance_date_entry.get().strip()
        try:
            parsed = datetime.strptime(raw_date, "%d-%m-%Y").date()
            if parsed > date.today():
                messagebox.showwarning(
                    "Invalid date", "Attendance date cannot be in the future."
                )
                return None
            return parsed.strftime("%d-%m-%Y")
        except ValueError:
            messagebox.showwarning(
                "Invalid date", "Enter a valid date in DD-MM-YYYY format."
            )
            return None

    def refresh_attendance_table(self):
        if not hasattr(self, "attendance_tree"):
            return
        for item in self.attendance_tree.get_children():
            self.attendance_tree.delete(item)
        for student in self.students:
            pct = (student["present"] / student["total"] * 100
                   if student["total"] else 0)
            self.attendance_tree.insert("", "end", iid=student["name"],
                values=(student["name"], student["status"],
                        student["present"], student["total"], f"{pct:.1f}%"))

    def mark_selected(self, status):
        selected = self.attendance_tree.selection()
        if not selected:
            messagebox.showwarning("Select a student", "Please select a student first.")
            return
        name = selected[0]
        student = self.find_student(name)
        if student:
            student["status"] = status
            self.refresh_attendance_table()

    def mark_all(self, status):
        if not self.students:
            messagebox.showinfo("No students", "Add students before marking attendance.")
            return
        for student in self.students:
            student["status"] = status
        self.refresh_attendance_table()

    def save_attendance(self):
        if not self.students:
            messagebox.showwarning("No students", "Please add students first.")
            return

        pending = [s["name"] for s in self.students if s["status"] == "Pending"]
        if pending:
            messagebox.showwarning(
                "Attendance incomplete",
                "Mark attendance for every student before saving.\n\nPending: "
                + ", ".join(pending[:8])
            )
            return

        selected_date = self.get_selected_attendance_date()
        if selected_date is None:
            return

        if any(record["date"] == selected_date for record in self.history):
            if not messagebox.askyesno(
                "Attendance already saved",
                f"Attendance has already been saved for {selected_date}. Save another record?"
            ):
                return

        for student in self.students:
            status = student["status"]
            student["total"] += 1
            if status == "Present":
                student["present"] += 1
            self.history.append({
                "date": selected_date,
                "name": student["name"],
                "status": status
            })
            student["status"] = "Pending"

        messagebox.showinfo("Success", "Attendance saved successfully!")
        self.show_page("Attendance")

    # ---------- Students page ----------

    def build_students(self):
        add_panel = tk.Frame(
            self.content, bg=self.PANEL,
            highlightthickness=1, highlightbackground=self.BORDER
        )
        add_panel.pack(fill="x", pady=(0, 20))

        tk.Label(
            add_panel, text="Add a new student", bg=self.PANEL,
            fg=self.TEXT, font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", padx=18, pady=(15, 10))

        form = tk.Frame(add_panel, bg=self.PANEL)
        form.pack(fill="x", padx=18, pady=(0, 17))

        self.student_name_entry = self.styled_entry(form, "Enter student name")
        self.student_name_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.student_name_entry.bind("<Return>", lambda event: self.add_student())

        self.make_button(
            form, "+  Add Student", self.add_student, self.BLUE
        ).pack(side="left")

        self.section_title(
            self.content, "Registered students",
            "Manage the students in your attendance list."
        )
        self.students_tree = self.make_table(
            self.content,
            ("name", "present", "total", "percentage"),
            ("STUDENT NAME", "PRESENT CLASSES", "TOTAL CLASSES", "ATTENDANCE"),
            (260, 150, 150, 150)
        )
        self.refresh_students_table()

        actions = tk.Frame(self.content, bg=self.BG)
        actions.pack(fill="x", pady=14)
        self.make_button(
            actions, "Remove selected student", self.remove_student, self.RED
        ).pack(side="right")

    def styled_entry(self, parent, placeholder):
        entry = tk.Entry(
            parent, bg=self.PANEL_LIGHT, fg=self.TEXT,
            insertbackground=self.TEXT, relief="flat",
            font=("Segoe UI", 10), highlightthickness=1,
            highlightbackground=self.BORDER,
            highlightcolor=self.BLUE
        )
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda event: (
            entry.delete(0, "end") if entry.get() == placeholder else None
        ))
        return entry

    def add_student(self):
        name = self.student_name_entry.get().strip()
        if not name or name == "Enter student name":
            messagebox.showwarning("Missing name", "Please enter a student name.")
            return
        if self.find_student(name):
            messagebox.showwarning("Duplicate student", "This student already exists.")
            return

        self.students.append({
            "name": name,
            "present": 0,
            "total": 0,
            "status": "Pending"
        })
        self.student_name_entry.delete(0, "end")
        self.refresh_students_table()
        messagebox.showinfo("Student added", f"{name} was added successfully.")

    def refresh_students_table(self):
        if not hasattr(self, "students_tree"):
            return
        for item in self.students_tree.get_children():
            self.students_tree.delete(item)
        for student in self.students:
            pct = (student["present"] / student["total"] * 100
                   if student["total"] else 0)
            self.students_tree.insert("", "end", iid=student["name"],
                values=(student["name"], student["present"],
                        student["total"], f"{pct:.1f}%"))

    def remove_student(self):
        selected = self.students_tree.selection()
        if not selected:
            messagebox.showwarning("Select a student", "Please select a student to remove.")
            return
        name = selected[0]
        if messagebox.askyesno("Confirm removal", f"Remove {name} from the student list?"):
            self.students = [s for s in self.students if s["name"] != name]
            self.refresh_students_table()

    # ---------- History page ----------

    def build_history(self):
        top = tk.Frame(self.content, bg=self.BG)
        top.pack(fill="x", pady=(0, 15))

        tk.Label(
            top, text="Search records", bg=self.BG, fg=self.MUTED,
            font=("Segoe UI", 9, "bold")
        ).pack(side="left", padx=(0, 10))

        self.history_search = tk.Entry(
            top, bg=self.PANEL, fg=self.TEXT,
            insertbackground=self.TEXT, relief="flat",
            font=("Segoe UI", 10), width=30
        )
        self.history_search.pack(side="left", ipady=8)
        self.history_search.bind("<KeyRelease>", lambda event: self.refresh_history_table())

        self.section_title(
            self.content, "Attendance records",
            "Every saved attendance entry appears here."
        )
        self.history_tree = self.make_table(
            self.content,
            ("date", "name", "status"),
            ("DATE", "STUDENT NAME", "ATTENDANCE STATUS"),
            (180, 280, 200)
        )
        self.refresh_history_table()

        bottom = tk.Frame(self.content, bg=self.BG)
        bottom.pack(fill="x", pady=14)
        self.make_button(
            bottom, "Clear history", self.clear_history, self.RED
        ).pack(side="right")

    def refresh_history_table(self):
        if not hasattr(self, "history_tree"):
            return
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        query = self.history_search.get().strip().lower() if hasattr(self, "history_search") else ""
        for record in reversed(self.history):
            searchable = f'{record["date"]} {record["name"]} {record["status"]}'.lower()
            if query in searchable:
                self.history_tree.insert(
                    "", "end",
                    values=(record["date"], record["name"], record["status"])
                )

    def clear_history(self):
        if not self.history:
            messagebox.showinfo("History empty", "There are no records to clear.")
            return
        if messagebox.askyesno(
            "Clear attendance history",
            "Are you sure you want to delete all attendance history records?"
        ):
            self.history.clear()
            self.refresh_history_table()

    # ---------- General helpers ----------

    def find_student(self, name):
        for student in self.students:
            if student["name"].casefold() == name.casefold():
                return student
        return None

    def empty_hint(self, parent, message):
        tk.Label(
            parent, text=message, bg=self.PANEL, fg=self.MUTED,
            font=("Segoe UI", 10), padx=15, pady=18
        ).pack(fill="x", pady=10)


if __name__ == "__main__":
    root = tk.Tk()
    app = AttendanceApp(root)
    root.mainloop()
