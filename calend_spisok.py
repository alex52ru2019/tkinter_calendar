import tkinter as tk
from tkinter import simpledialog, messagebox
import calendar
from datetime import datetime


class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Календарь со списком дел")
        self.root.geometry("350x600")

        self.current_year = datetime.now().year
        self.current_month = datetime.now().month

        self.tasks = {}  # Словарь для хранения задач {дата: [(задача, выполнено)]}

        self.create_widgets()
        self.update_calendar()

    def create_widgets(self):
        # Верхняя панель с месяцем и годом
        self.header_frame = tk.Frame(self.root)
        self.header_frame.pack()

        self.prev_button = tk.Button(self.header_frame, text="<", command=self.prev_month)
        self.prev_button.pack(side=tk.LEFT)

        self.month_year_label = tk.Label(self.header_frame, text="", font=("Arial", 14))
        self.month_year_label.pack(side=tk.LEFT)

        self.next_button = tk.Button(self.header_frame, text=">", command=self.next_month)
        self.next_button.pack(side=tk.LEFT)

        # Календарь
        self.calendar_frame = tk.Frame(self.root)
        self.calendar_frame.pack()

        self.day_buttons = []
        for i in range(6):
            row = []
            for j in range(7):
                btn = tk.Button(self.calendar_frame, width=4, height=2, command=lambda i=i, j=j: self.select_day(i, j))
                btn.grid(row=i+1, column=j)
                row.append(btn)
            self.day_buttons.append(row)

        # Список дел
        self.tasks_frame = tk.Frame(self.root)
        self.tasks_frame.pack()

        self.tasks_listbox = tk.Listbox(self.tasks_frame, bg="light yellow", width=25, height=5, font=("Arial", 14))
        self.tasks_listbox.pack(side=tk.LEFT)


        self.tasks_scrollbar = tk.Scrollbar(self.tasks_frame)
        self.tasks_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        self.tasks_listbox.config(yscrollcommand=self.tasks_scrollbar.set)
        self.tasks_scrollbar.config(command=self.tasks_listbox.yview)

        # Кнопки управления задачами
        self.add_task_button = tk.Button(self.root, text="Добавить дело", command=self.add_task, font=("Arial", 14))
        self.add_task_button.pack()

        self.mark_done_button = tk.Button(self.root, text="Выполнено", command=self.mark_task_done, font=("Arial", 14))
        self.mark_done_button.pack()

        self.delete_task_button = tk.Button(self.root, text="Удалить задачу", command=self.delete_task, font=("Arial", 14))
        self.delete_task_button.pack()

    def update_calendar(self):
        self.month_year_label.config(text=f"{calendar.month_name[self.current_month]} {self.current_year}")
        cal = calendar.monthcalendar(self.current_year, self.current_month)

        days_of_week = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        for day in days_of_week:
            tk.Label(self.calendar_frame, text=day, font=("Arial", 12, "bold"), bg="white").grid(row=0, column=days_of_week.index(day))

        # Обновить кнопки дней
        for i in range(6):
            for j in range(7):
                self.day_buttons[i][j].config(text="", bg="white", state=tk.DISABLED, font=("Arial", 12))

        for i, week in enumerate(cal):
            for j, day in enumerate(week):
                if day != 0:
                    self.day_buttons[i][j].config(text=str(day), state=tk.NORMAL, font=("Arial", 12))
                    date = datetime(self.current_year, self.current_month, day)
                    if date in self.tasks:
                        if any(not task[1] and date < datetime.now() for task in self.tasks[date]):
                            self.day_buttons[i][j].config(bg="red")
                        else:
                            self.day_buttons[i][j].config(bg="yellow")

    def select_day(self, row, col):
        for i in range(6):
            for j in range(7):
                self.day_buttons[i][j].config(
                    bg="white" if self.day_buttons[i][j].cget("bg") == "lightblue" else self.day_buttons[i][j].cget("bg"))
        self.day_buttons[row][col].config(bg="lightblue")
        self.selected_day = int(self.day_buttons[row][col].cget("text"))
        self.update_tasks_list()

    def update_tasks_list(self):
        self.tasks_listbox.delete(0, tk.END)
        date = datetime(self.current_year, self.current_month, self.selected_day)
        if date in self.tasks:
            for task, done in self.tasks[date]:
                self.tasks_listbox.insert(tk.END, task)
                if done:
                    self.tasks_listbox.itemconfig(tk.END, {'bg': 'light green'})

    def add_task(self):
        date = datetime(self.current_year, self.current_month, self.selected_day)
        task = simpledialog.askstring("Добавить дело", "Введите задачу:")
        if task:
            if date not in self.tasks:
                self.tasks[date] = []
            self.tasks[date].append((task, False))
            self.update_tasks_list()
            self.update_calendar()

    def mark_task_done(self):
        selected_task_index = self.tasks_listbox.curselection()
        if selected_task_index:
            date = datetime(self.current_year, self.current_month, self.selected_day)
            task, done = self.tasks[date][selected_task_index[0]]
            self.tasks[date][selected_task_index[0]] = (task, True)
            self.update_tasks_list()
            self.update_calendar()

    def delete_task(self):
        selected_task_index = self.tasks_listbox.curselection()
        if selected_task_index:
            date = datetime(self.current_year, self.current_month, self.selected_day)
            del self.tasks[date][selected_task_index[0]]
            if not self.tasks[date]:
                del self.tasks[date]
            self.update_tasks_list()
            self.update_calendar()

    def prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.update_calendar()

    def next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.update_calendar()

if __name__ == "__main__":
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()