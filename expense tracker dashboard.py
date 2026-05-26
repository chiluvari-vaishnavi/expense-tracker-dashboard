import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

class ExpenseTrackerDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker Dashboard")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")

        # Data store (list of dicts)
        self.expenses = []

        self.setup_ui()

    def setup_ui(self):
        # Title label
        title = tk.Label(
            self.root,
            text="Expense Tracker Dashboard",
            bg="#f0f0f0",
            font=("Arial", 16, "bold"),
            pady=10
        )
        title.pack()

        # Amount and category entry row
        input_frame = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        input_frame.pack()

        tk.Label(input_frame, text="Amount:", bg="#f0f0f0").grid(row=0, column=0, padx=5)
        self.amount_entry = tk.Entry(input_frame, width=10)
        self.amount_entry.grid(row=0, column=1, padx=5)

        tk.Label(input_frame, text="Category:", bg="#f0f0f0").grid(row=0, column=2, padx=5)
        self.category_entry = tk.Entry(input_frame, width=15)
        self.category_entry.grid(row=0, column=3, padx=5)

        tk.Label(input_frame, text="Description:", bg="#f0f0f0").grid(row=0, column=4, padx=5)
        self.desc_entry = tk.Entry(input_frame, width=20)
        self.desc_entry.grid(row=0, column=5, padx=5)

        add_btn = tk.Button(
            input_frame,
            text="Add Expense",
            bg="#4CAF50", fg="white",
            command=self.add_expense
        )
        add_btn.grid(row=0, column=6, padx=10)

        # Stats panels (Expenses, Total)
        stats_frame = tk.Frame(self.root, bg="#f0f0f0", pady=10)
        stats_frame.pack()

        self.total_label = tk.Label(
            stats_frame,
            text="Total Expenses: ₹0.00",
            bg="#d0f0c0",
            font=("Arial", 12),
            width=20,
            relief="groove"
        )
        self.total_label.grid(row=0, column=0, padx=10)

        self.exp_count_label = tk.Label(
            stats_frame,
            text="Total Items: 0",
            bg="#bedade",
            font=("Arial", 12),
            width=20,
            relief="groove"
        )
        self.exp_count_label.grid(row=0, column=1, padx=10)

        # Table for expenses
        table_frame = tk.Frame(self.root, bg="#f0f0f0")
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columns = ("id", "date", "amount", "category", "description")
        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=15
        )

        self.tree.heading("id", text="ID")
        self.tree.heading("date", text="Date")
        self.tree.heading("amount", text="Amount (₹)")
        self.tree.heading("category", text="Category")
        self.tree.heading("description", text="Description")

        self.tree.column("id", width=40, anchor="center")
        self.tree.column("date", width=100, anchor="center")
        self.tree.column("amount", width=80, anchor="e")
        self.tree.column("category", width=100, anchor="w")
        self.tree.column("description", width=200, anchor="w")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)

        # Delete button
        del_btn = tk.Button(
            self.root,
            text="Delete Selected",
            bg="#f44336",
            fg="white",
            command=self.delete_expense
        )
        del_btn.pack(pady=5)

    def add_expense(self):
        try:
            amt = float(self.amount_entry.get().strip())
            cat = self.category_entry.get().strip()
            desc = self.desc_entry.get().strip()

            if not cat:
                messagebox.showwarning("Input Error", "Category is required.")
                return

            date_str = datetime.now().strftime("%Y-%m-%d %H:%M")
            idx = len(self.expenses) + 1

            self.expenses.append({
                "id": idx,
                "date": date_str,
                "amount": amt,
                "category": cat,
                "description": desc
            })

            self.tree.insert(
                "", "end",
                values=(idx, date_str, f"{amt:.2f}", cat, desc)
            )

            self.update_stats()
            self.clear_entries()

        except ValueError:
            messagebox.showwarning("Input Error", "Amount must be a valid number.")

    def delete_expense(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showinfo("No Selection", "Select an expense to delete.")
            return

        item = self.tree.focus()
        values = self.tree.item(item, "values")
        exp_id = int(values[0])

        # Remove from memory
        self.expenses = [e for e in self.expenses if e["id"] != exp_id]

        # Repack IDs and refresh
        for i, e in enumerate(self.expenses):
            e["id"] = i + 1

        # Clear and reinsert
        self.tree.delete(*self.tree.get_children())
        for e in self.expenses:
            self.tree.insert(
                "", "end",
                values=(
                    e["id"],
                    e["date"],
                    f"{e['amount']:.2f}",
                    e["category"],
                    e["description"]
                )
            )

        self.update_stats()

    def update_stats(self):
        total = sum(e["amount"] for e in self.expenses)
        count = len(self.expenses)
        self.total_label.config(text=f"Total Expenses: ₹{total:.2f}")
        self.exp_count_label.config(text=f"Total Items: {count}")

    def clear_entries(self):
        self.amount_entry.delete(0, tk.END)
        self.category_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerDashboard(root)
    root.mainloop()