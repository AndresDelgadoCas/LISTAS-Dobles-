import tkinter as tk
from tkinter import ttk, messagebox

from horse import Horse
from doubly_linked_list import DoublyLinkedList


class HorseStableManager:
    BG = "#0b1220"
    SIDEBAR = "#111c2e"
    PANEL = "#162337"
    CARD = "#1c2d45"
    CARD_HOVER = "#243b59"
    TEXT = "#f8fafc"
    MUTED = "#91a4bd"
    GOLD = "#d7aa61"
    GOLD_DARK = "#9b743c"
    GREEN = "#4ade80"
    RED = "#f87171"
    BLUE = "#60a5fa"
    BORDER = "#263a55"

    def __init__(self, root):
        self.root = root
        self.root.title("Horse Stable Manager")
        self.root.geometry("1280x780")
        self.root.minsize(1100, 700)
        self.root.configure(bg=self.BG)

        self.stable = DoublyLinkedList()

        self.configure_styles()
        self.build_interface()
        self.load_sample_data()
        self.refresh()

    def configure_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=self.PANEL,
            fieldbackground=self.PANEL,
            foreground=self.TEXT,
            rowheight=38,
            borderwidth=0,
            font=("Segoe UI", 9)
        )

        style.configure(
            "Treeview.Heading",
            background=self.CARD,
            foreground=self.GOLD,
            font=("Segoe UI Semibold", 9),
            relief="flat",
            padding=8
        )

        style.map(
            "Treeview",
            background=[("selected", self.GOLD_DARK)],
            foreground=[("selected", self.TEXT)]
        )

    def build_interface(self):
        self.build_header()

        body = tk.Frame(self.root, bg=self.BG)
        body.pack(fill="both", expand=True)

        self.build_sidebar(body)
        self.build_content(body)

    def build_header(self):
        header = tk.Frame(self.root, bg=self.SIDEBAR, height=78)
        header.pack(fill="x")
        header.pack_propagate(False)

        brand = tk.Frame(header, bg=self.SIDEBAR)
        brand.pack(side="left", padx=28)

        tk.Label(
            brand,
            text="🐎",
            bg=self.SIDEBAR,
            fg=self.GOLD,
            font=("Segoe UI Emoji", 23)
        ).pack(side="left", padx=(0, 10))

        titles = tk.Frame(brand, bg=self.SIDEBAR)
        titles.pack(side="left")

        tk.Label(
            titles,
            text="HORSE STABLE MANAGER",
            bg=self.SIDEBAR,
            fg=self.TEXT,
            font=("Segoe UI Semibold", 18)
        ).pack(anchor="w")

        tk.Label(
            titles,
            text="Stable records • Doubly Linked List",
            bg=self.SIDEBAR,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        ).pack(anchor="w")

        self.system_status = tk.Label(
            header,
            text="●  SYSTEM READY",
            bg=self.SIDEBAR,
            fg=self.GREEN,
            font=("Segoe UI Semibold", 9)
        )
        self.system_status.pack(side="right", padx=30)

    def build_sidebar(self, parent):
        sidebar = tk.Frame(parent, bg=self.SIDEBAR, width=235)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="NAVIGATION",
            bg=self.SIDEBAR,
            fg=self.MUTED,
            font=("Segoe UI Semibold", 8)
        ).pack(anchor="w", padx=25, pady=(30, 12))

        self.sidebar_button(sidebar, "▣   Dashboard", self.refresh, True)
        self.sidebar_button(sidebar, "🐎   Horse Records", self.show_all)
        self.sidebar_button(sidebar, "↔   Forward Traversal", self.show_forward)
        self.sidebar_button(sidebar, "↔   Backward Traversal", self.show_backward)

        tk.Frame(sidebar, bg=self.BORDER, height=1).pack(fill="x", padx=25, pady=25)

        tk.Label(
            sidebar,
            text="DATA STRUCTURE",
            bg=self.SIDEBAR,
            fg=self.MUTED,
            font=("Segoe UI Semibold", 8)
        ).pack(anchor="w", padx=25, pady=(0, 12))

        self.structure_label = tk.Label(
            sidebar,
            text="HEAD  →  ...  →  TAIL",
            bg=self.SIDEBAR,
            fg=self.GOLD,
            font=("Consolas", 9)
        )
        self.structure_label.pack(anchor="w", padx=25)

        tk.Label(
            sidebar,
            text="Each horse is stored as a node.\nEvery node points to the\nprevious and next horse.",
            bg=self.SIDEBAR,
            fg=self.MUTED,
            justify="left",
            font=("Segoe UI", 9),
            pady=12
        ).pack(anchor="w", padx=25)

        footer = tk.Frame(sidebar, bg=self.SIDEBAR)
        footer.pack(side="bottom", fill="x", padx=25, pady=25)

        tk.Label(
            footer,
            text="CASE STUDY",
            bg=self.SIDEBAR,
            fg=self.MUTED,
            font=("Segoe UI Semibold", 8)
        ).pack(anchor="w")

        tk.Label(
            footer,
            text="Horse Stable Management",
            bg=self.SIDEBAR,
            fg=self.TEXT,
            font=("Segoe UI", 9)
        ).pack(anchor="w", pady=(3, 0))

    def sidebar_button(self, parent, text, command, active=False):
        button = tk.Button(
            parent,
            text=text,
            command=command,
            anchor="w",
            bg=self.CARD if active else self.SIDEBAR,
            fg=self.TEXT if active else self.MUTED,
            activebackground=self.CARD_HOVER,
            activeforeground=self.TEXT,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            font=("Segoe UI Semibold", 9),
            padx=18,
            pady=11
        )
        button.pack(fill="x", padx=15, pady=2)

    def build_content(self, parent):
        content = tk.Frame(parent, bg=self.BG)
        content.pack(side="left", fill="both", expand=True, padx=25, pady=23)

        self.build_page_title(content)
        self.build_stats(content)
        self.build_current_card(content)
        self.build_toolbar(content)
        self.build_table(content)

    def build_page_title(self, parent):
        title = tk.Frame(parent, bg=self.BG)
        title.pack(fill="x", pady=(0, 18))

        tk.Label(
            title,
            text="Stable Overview",
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI Semibold", 23)
        ).pack(side="left")

        tk.Label(
            title,
            text="Manage and navigate horse records",
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 10)
        ).pack(side="left", padx=15, pady=(7, 0))

    def build_stats(self, parent):
        frame = tk.Frame(parent, bg=self.BG)
        frame.pack(fill="x", pady=(0, 16))

        self.total_card = self.stat_card(frame, "TOTAL HORSES", "0", self.GOLD)
        self.healthy_card = self.stat_card(frame, "HEALTHY", "0", self.GREEN)
        self.training_card = self.stat_card(frame, "IN TRAINING", "0", self.BLUE)
        self.current_card = self.stat_card(frame, "CURRENT HORSE", "—", self.GOLD)

    def stat_card(self, parent, title, value, accent):
        card = tk.Frame(parent, bg=self.CARD, height=88)
        card.pack(side="left", fill="x", expand=True, padx=4)
        card.pack_propagate(False)

        tk.Frame(card, bg=accent, width=4).pack(side="left", fill="y")

        info = tk.Frame(card, bg=self.CARD)
        info.pack(side="left", fill="both", expand=True, padx=14, pady=10)

        tk.Label(
            info,
            text=title,
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI Semibold", 8)
        ).pack(anchor="w")

        value_label = tk.Label(
            info,
            text=value,
            bg=self.CARD,
            fg=self.TEXT,
            font=("Segoe UI Semibold", 19)
        )
        value_label.pack(anchor="w")

        return value_label

    def build_current_card(self, parent):
        panel = tk.Frame(parent, bg=self.CARD)
        panel.pack(fill="x", pady=(0, 16))

        info = tk.Frame(panel, bg=self.CARD)
        info.pack(side="left", fill="both", expand=True, padx=24, pady=18)

        tk.Label(
            info,
            text="CURRENT HORSE",
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI Semibold", 8)
        ).pack(anchor="w")

        self.current_name = tk.Label(
            info,
            text="No horse selected",
            bg=self.CARD,
            fg=self.TEXT,
            font=("Segoe UI Semibold", 22)
        )
        self.current_name.pack(anchor="w", pady=(3, 0))

        self.current_info = tk.Label(
            info,
            text="Add a horse or select one from the table.",
            bg=self.CARD,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        )
        self.current_info.pack(anchor="w", pady=(3, 0))

        nav = tk.Frame(panel, bg=self.CARD)
        nav.pack(side="right", padx=22)

        self.action_button(nav, "←  PREVIOUS", self.previous_horse, self.CARD, self.TEXT).pack(side="left", padx=4)
        self.action_button(nav, "NEXT  →", self.next_horse, self.GOLD, self.BG).pack(side="left", padx=4)

    def build_toolbar(self, parent):
        toolbar = tk.Frame(parent, bg=self.BG)
        toolbar.pack(fill="x", pady=(0, 10))

        self.search = tk.Entry(
            toolbar,
            bg=self.CARD,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief="flat",
            font=("Segoe UI", 10)
        )
        self.search.pack(side="left", fill="x", expand=True, ipady=10, padx=(0, 8))

        self.action_button(toolbar, "SEARCH", self.search_horse, self.CARD, self.TEXT).pack(side="left", padx=4)
        self.action_button(toolbar, "＋ ADD HORSE", self.open_add_window, self.GOLD, self.BG).pack(side="left", padx=4)
        self.action_button(toolbar, "FORWARD", self.show_forward, self.CARD, self.TEXT).pack(side="left", padx=4)
        self.action_button(toolbar, "BACKWARD", self.show_backward, self.CARD, self.TEXT).pack(side="left", padx=4)

    def build_table(self, parent):
        table_panel = tk.Frame(parent, bg=self.CARD)
        table_panel.pack(fill="both", expand=True)

        columns = ("id", "name", "breed", "age", "owner", "health", "training")

        self.tree = ttk.Treeview(
            table_panel,
            columns=columns,
            show="headings",
            selectmode="browse"
        )

        headers = {
            "id": "ID",
            "name": "HORSE",
            "breed": "BREED",
            "age": "AGE",
            "owner": "OWNER",
            "health": "HEALTH",
            "training": "TRAINING"
        }

        widths = {
            "id": 75, "name": 125, "breed": 120,
            "age": 55, "owner": 125, "health": 135, "training": 120
        }

        for column in columns:
            self.tree.heading(column, text=headers[column])
            self.tree.column(column, width=widths[column], anchor="center")

        scrollbar = ttk.Scrollbar(table_panel, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=10)
        scrollbar.pack(side="right", fill="y", padx=(0, 8), pady=10)

        self.tree.bind("<<TreeviewSelect>>", self.on_table_select)
        self.tree.bind("<Double-1>", lambda _event: self.open_edit_window())

        hint = tk.Label(
            parent,
            text="Double-click a horse to edit it  •  Use Previous / Next to navigate the linked list",
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 8)
        )
        hint.pack(anchor="w", pady=(7, 0))

    def action_button(self, parent, text, command, bg, fg):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=bg,
            fg=fg,
            activebackground=bg,
            activeforeground=fg,
            relief="flat",
            borderwidth=0,
            cursor="hand2",
            font=("Segoe UI Semibold", 8),
            padx=12,
            pady=9
        )

    def load_sample_data(self):
        records = [
            ("H001", "Thunder", "Arabian", 7, "John Smith", "Healthy", "In Training"),
            ("H002", "Spirit", "Mustang", 6, "Emma Wilson", "Healthy", "Competition"),
            ("H003", "Apollo", "Andalusian", 8, "James Brown", "Under Observation", "In Training"),
            ("H004", "Rocky", "Friesian", 5, "Daniel Carter", "Healthy", "Resting"),
            ("H005", "Shadow", "Quarter Horse", 9, "Olivia Martin", "Healthy", "Competition"),
        ]

        for record in records:
            self.stable.add(Horse(*record))

        self.stable.current = self.stable.head

    def refresh(self):
        self.populate_table(self.stable.forward())

        horses = self.stable.forward()
        healthy = sum(h.health == "Healthy" for h in horses)
        training = sum(h.training == "In Training" for h in horses)

        self.total_card.config(text=str(self.stable.size))
        self.healthy_card.config(text=str(healthy))
        self.training_card.config(text=str(training))

        if self.stable.current:
            self.current_card.config(text=self.stable.current.horse.name)
            self.current_name.config(text=self.stable.current.horse.name)
            horse = self.stable.current.horse
            self.current_info.config(
                text=f"{horse.breed}  •  Age {horse.age}  •  {horse.health}  •  {horse.training}"
            )
        else:
            self.current_card.config(text="—")
            self.current_name.config(text="No horse selected")
            self.current_info.config(text="Add a horse or select one from the table.")

        self.update_structure_label()

    def populate_table(self, horses):
        for item in self.tree.get_children():
            self.tree.delete(item)

        for horse in horses:
            self.tree.insert(
                "",
                "end",
                values=(
                    horse.horse_id,
                    horse.name,
                    horse.breed,
                    horse.age,
                    horse.owner,
                    horse.health,
                    horse.training
                )
            )

    def update_structure_label(self):
        if not self.stable.head:
            self.structure_label.config(text="HEAD  →  NULL  ←  TAIL")
            return

        horses = self.stable.forward()

        if len(horses) <= 3:
            names = "  ⇄  ".join(h.name for h in horses)
        else:
            names = f"{horses[0].name}  ⇄  ...  ⇄  {horses[-1].name}"

        self.structure_label.config(text=f"HEAD → {names} ← TAIL")

    def on_table_select(self, _event=None):
        selected = self.tree.selection()

        if not selected:
            return

        values = self.tree.item(selected[0], "values")
        node = self.stable.find(values[0])

        if node:
            self.stable.current = node
            self.refresh()

    def show_all(self):
        self.populate_table(self.stable.forward())
        self.set_status("SHOWING ALL HORSES", self.GREEN)

    def show_forward(self):
        self.populate_table(self.stable.forward())
        self.set_status("FORWARD: HEAD → TAIL", self.GREEN)

    def show_backward(self):
        self.populate_table(self.stable.backward())
        self.set_status("BACKWARD: TAIL → HEAD", self.GOLD)

    def next_horse(self):
        if self.stable.next():
            self.refresh()
            self.set_status("MOVED TO NEXT HORSE", self.BLUE)
        else:
            self.set_status("ALREADY AT TAIL", self.MUTED)

    def previous_horse(self):
        if self.stable.previous():
            self.refresh()
            self.set_status("MOVED TO PREVIOUS HORSE", self.BLUE)
        else:
            self.set_status("ALREADY AT HEAD", self.MUTED)

    def search_horse(self):
        horse_id = self.search.get().strip()

        if not horse_id:
            messagebox.showwarning("Search", "Enter a Horse ID.")
            return

        node = self.stable.find(horse_id)

        if node:
            self.stable.current = node
            self.refresh()
            self.set_status("HORSE FOUND", self.GREEN)
        else:
            messagebox.showinfo("Search Result", "Horse not found.")

    def open_add_window(self):
        self.open_form_window("Add Horse", None)

    def open_edit_window(self):
        if not self.stable.current:
            messagebox.showinfo("Edit Horse", "Select a horse first.")
            return

        self.open_form_window("Edit Horse", self.stable.current.horse)

    def open_form_window(self, title, horse):
        window = tk.Toplevel(self.root)
        window.title(title)
        window.geometry("430x570")
        window.resizable(False, False)
        window.configure(bg=self.SIDEBAR)
        window.transient(self.root)
        window.grab_set()

        tk.Label(
            window,
            text="🐎",
            bg=self.SIDEBAR,
            fg=self.GOLD,
            font=("Segoe UI Emoji", 28)
        ).pack(pady=(22, 0))

        tk.Label(
            window,
            text=title.upper(),
            bg=self.SIDEBAR,
            fg=self.TEXT,
            font=("Segoe UI Semibold", 16)
        ).pack(pady=(3, 18))

        fields = {}
        definitions = [
            ("Horse ID", "horse_id"),
            ("Horse Name", "name"),
            ("Breed", "breed"),
            ("Age", "age"),
            ("Owner", "owner")
        ]

        for label, key in definitions:
            self.form_field(window, label, key, fields)

        self.form_combo(window, "Health Status", "health",
                        ["Healthy", "Under Observation", "Veterinary Care"], fields)

        self.form_combo(window, "Training Status", "training",
                        ["Resting", "In Training", "Competition"], fields)

        if horse:
            values = {
                "horse_id": horse.horse_id,
                "name": horse.name,
                "breed": horse.breed,
                "age": str(horse.age),
                "owner": horse.owner
            }

            for key, value in values.items():
                fields[key].insert(0, value)

            fields["health"].set(horse.health)
            fields["training"].set(horse.training)

        def save():
            data = {key: widget.get().strip() for key, widget in fields.items()}

            if any(not data[k] for k in ("horse_id", "name", "breed", "age", "owner")):
                messagebox.showwarning("Missing Information", "Complete all required fields.", parent=window)
                return

            try:
                age = int(data["age"])
                if age <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showwarning("Invalid Age", "Age must be a positive number.", parent=window)
                return

            if horse:
                if data["horse_id"].lower() != horse.horse_id.lower():
                    messagebox.showwarning("ID Locked", "Horse ID cannot be changed when editing.", parent=window)
                    return

                self.stable.update(
                    horse.horse_id, data["name"], data["breed"], age,
                    data["owner"], data["health"], data["training"]
                )
                self.set_status("HORSE UPDATED", self.BLUE)
            else:
                if self.stable.find(data["horse_id"]):
                    messagebox.showwarning("Duplicate ID", "That Horse ID already exists.", parent=window)
                    return

                self.stable.add(
                    Horse(
                        data["horse_id"], data["name"], data["breed"], age,
                        data["owner"], data["health"], data["training"]
                    )
                )
                self.set_status("HORSE ADDED", self.GREEN)

            self.refresh()
            window.destroy()

        self.action_button(
            window, "SAVE HORSE", save, self.GOLD, self.BG
        ).pack(fill="x", padx=35, pady=22)

    def form_field(self, parent, label, key, fields):
        tk.Label(
            parent,
            text=label.upper(),
            bg=self.SIDEBAR,
            fg=self.MUTED,
            font=("Segoe UI Semibold", 8)
        ).pack(anchor="w", padx=35, pady=(3, 4))

        entry = tk.Entry(
            parent,
            bg=self.CARD,
            fg=self.TEXT,
            insertbackground=self.TEXT,
            relief="flat",
            font=("Segoe UI", 10)
        )
        entry.pack(fill="x", padx=35, ipady=8, pady=(0, 7))
        fields[key] = entry

    def form_combo(self, parent, label, key, values, fields):
        tk.Label(
            parent,
            text=label.upper(),
            bg=self.SIDEBAR,
            fg=self.MUTED,
            font=("Segoe UI Semibold", 8)
        ).pack(anchor="w", padx=35, pady=(3, 4))

        combo = ttk.Combobox(
            parent,
            values=values,
            state="readonly",
            font=("Segoe UI", 10)
        )
        combo.pack(fill="x", padx=35, pady=(0, 7), ipady=3)
        combo.current(0)
        fields[key] = combo

    def delete_current(self):
        if not self.stable.current:
            return

        horse = self.stable.current.horse

        if not messagebox.askyesno(
            "Delete Horse",
            f"Delete {horse.name} from the stable?"
        ):
            return

        self.stable.delete(horse.horse_id)
        self.refresh()
        self.set_status("HORSE DELETED", self.RED)

    def set_status(self, text, color):
        self.system_status.config(text=f"●  {text}", fg=color)


def run_app():
    root = tk.Tk()
    app = HorseStableManager(root)
    root.mainloop()
