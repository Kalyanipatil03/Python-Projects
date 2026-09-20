import tkinter as tk
from tkinter import messagebox

from calculator import SafeCalculator


class ScientificCalculatorUI:
    BG = "#101114"
    DISPLAY_BG = "#17191E"
    PANEL = "#1C1F26"
    BUTTON = "#252932"
    BUTTON_HOVER = "#30343E"
    TEXT = "#F5F7FA"
    MUTED = "#8E96A3"
    ACCENT = "#6C63FF"
    ACCENT_HOVER = "#7D75FF"
    OPERATOR = "#343944"
    DANGER = "#B83B5E"
    BORDER = "#2C3038"

    def __init__(self, root):
        self.root = root
        self.root.title("Scientific Calculator")
        self.root.geometry("520x760")
        self.root.minsize(430, 650)
        self.root.configure(bg=self.BG)

        self.calculator = SafeCalculator()
        self.expression = tk.StringVar()
        self.result = tk.StringVar(value="0")

        self.history = []

        self.build_ui()
        self.bind_keyboard()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------

    def build_ui(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(1, weight=1)

        self.build_header()
        self.build_calculator()

    def build_header(self):
        header = tk.Frame(
            self.root,
            bg=self.BG,
            height=70
        )
        header.grid(row=0, column=0, sticky="ew", padx=22, pady=(18, 5))

        header.columnconfigure(0, weight=1)

        title = tk.Label(
            header,
            text="SCIENTIFIC CALCULATOR",
            bg=self.BG,
            fg=self.TEXT,
            font=("Segoe UI", 16, "bold")
        )
        title.grid(row=0, column=0, sticky="w")

        subtitle = tk.Label(
            header,
            text="Precise • Fast • Scientific",
            bg=self.BG,
            fg=self.MUTED,
            font=("Segoe UI", 9)
        )
        subtitle.grid(row=1, column=0, sticky="w", pady=(2, 0))

        self.mode_button = tk.Button(
            header,
            text="DEG",
            command=self.toggle_angle_mode,
            bg=self.ACCENT,
            fg="white",
            activebackground=self.ACCENT_HOVER,
            activeforeground="white",
            relief="flat",
            bd=0,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            padx=16,
            pady=8
        )
        self.mode_button.grid(row=0, column=1, rowspan=2, padx=(10, 0))

    def build_calculator(self):
        container = tk.Frame(
            self.root,
            bg=self.PANEL,
            highlightbackground=self.BORDER,
            highlightthickness=1
        )
        container.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=18,
            pady=(5, 18)
        )

        container.columnconfigure(0, weight=1)
        container.rowconfigure(2, weight=1)

        self.build_display(container)
        self.build_history(container)
        self.build_buttons(container)

    def build_display(self, parent):
        display = tk.Frame(
            parent,
            bg=self.DISPLAY_BG,
            height=150
        )
        display.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=12,
            pady=12
        )

        display.columnconfigure(0, weight=1)

        expression_label = tk.Label(
            display,
            textvariable=self.expression,
            bg=self.DISPLAY_BG,
            fg=self.MUTED,
            anchor="e",
            font=("Segoe UI", 13)
        )
        expression_label.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=18,
            pady=(15, 5)
        )

        result_label = tk.Label(
            display,
            textvariable=self.result,
            bg=self.DISPLAY_BG,
            fg=self.TEXT,
            anchor="e",
            font=("Segoe UI", 30, "bold")
        )
        result_label.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=18,
            pady=(5, 15)
        )

    def build_history(self, parent):
        history_frame = tk.Frame(
            parent,
            bg=self.PANEL
        )
        history_frame.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=12,
            pady=(0, 8)
        )

        history_frame.columnconfigure(0, weight=1)

        self.history_label = tk.Label(
            history_frame,
            text="No calculations yet",
            bg=self.PANEL,
            fg=self.MUTED,
            anchor="w",
            font=("Segoe UI", 9)
        )
        self.history_label.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=5
        )

        clear_history = tk.Button(
            history_frame,
            text="Clear history",
            command=self.clear_history,
            bg=self.PANEL,
            fg=self.MUTED,
            activebackground=self.PANEL,
            activeforeground=self.TEXT,
            relief="flat",
            bd=0,
            font=("Segoe UI", 8),
            cursor="hand2"
        )
        clear_history.grid(row=0, column=1, padx=5)

    def build_buttons(self, parent):
        buttons_frame = tk.Frame(
            parent,
            bg=self.PANEL
        )
        buttons_frame.grid(
            row=2,
            column=0,
            sticky="nsew",
            padx=12,
            pady=8
        )

        for column in range(5):
            buttons_frame.columnconfigure(column, weight=1)

        for row in range(7):
            buttons_frame.rowconfigure(row, weight=1)

        buttons = [
            [
                ("sin", "sin("),
                ("cos", "cos("),
                ("tan", "tan("),
                ("log", "log("),
                ("ln", "ln("),
            ],
            [
                ("√", "sqrt("),
                ("x²", "^2"),
                ("xʸ", "^"),
                ("π", "pi"),
                ("e", "e"),
            ],
            [
                ("(", "("),
                (")", ")"),
                ("n!", "factorial("),
                ("AC", "AC"),
                ("⌫", "BACK"),
            ],
            [
                ("7", "7"),
                ("8", "8"),
                ("9", "9"),
                ("÷", "÷"),
                ("×", "×"),
            ],
            [
                ("4", "4"),
                ("5", "5"),
                ("6", "6"),
                ("−", "−"),
                ("+", "+"),
            ],
            [
                ("1", "1"),
                ("2", "2"),
                ("3", "3"),
                (".", "."),
                ("=", "="),
            ],
            [
                ("0", "0"),
                ("00", "00"),
                ("%", "%"),
                ("±", "NEG"),
                ("History", "HISTORY"),
            ],
        ]

        for row_index, row in enumerate(buttons):
            for col_index, (label, action) in enumerate(row):
                button = self.create_button(
                    buttons_frame,
                    label,
                    action
                )

                button.grid(
                    row=row_index,
                    column=col_index,
                    sticky="nsew",
                    padx=4,
                    pady=4
                )

    def create_button(self, parent, text, action):
        if action == "=":
            bg = self.ACCENT
            hover = self.ACCENT_HOVER
        elif action in {"AC", "BACK"}:
            bg = self.DANGER
            hover = "#D34A6B"
        elif action in {"÷", "×", "−", "+", "%", "NEG"}:
            bg = self.OPERATOR
            hover = self.BUTTON_HOVER
        else:
            bg = self.BUTTON
            hover = self.BUTTON_HOVER

        button = tk.Button(
            parent,
            text=text,
            command=lambda: self.handle_action(action),
            bg=bg,
            fg=self.TEXT,
            activebackground=hover,
            activeforeground="white",
            relief="flat",
            bd=0,
            font=(
                "Segoe UI",
                12 if len(text) < 5 else 10,
                "bold"
            ),
            cursor="hand2"
        )

        button.bind(
            "<Enter>",
            lambda event: button.configure(bg=hover)
        )

        button.bind(
            "<Leave>",
            lambda event: button.configure(bg=bg)
        )

        return button

    # ---------------------------------------------------------
    # Actions
    # ---------------------------------------------------------

    def handle_action(self, action):
        if action == "AC":
            self.clear()
            return

        if action == "BACK":
            self.backspace()
            return

        if action == "=":
            self.calculate()
            return

        if action == "NEG":
            self.toggle_negative()
            return

        if action == "HISTORY":
            self.show_history()
            return

        self.expression.set(
            self.expression.get() + action
        )

    def clear(self):
        self.expression.set("")
        self.result.set("0")

    def backspace(self):
        current = self.expression.get()
        self.expression.set(current[:-1])

    def toggle_negative(self):
        current = self.expression.get()

        if not current:
            self.expression.set("-")
        elif current.startswith("-(") and current.endswith(")"):
            self.expression.set(current[2:-1])
        else:
            self.expression.set(f"-({current})")

    def calculate(self):
        expression = self.expression.get()

        if not expression:
            return

        try:
            value = self.calculator.evaluate(expression)
            formatted = self.format_result(value)

            self.result.set(formatted)

            self.history.insert(
                0,
                f"{expression} = {formatted}"
            )

            self.history = self.history[:5]
            self.update_history_label()

        except Exception as error:
            self.result.set("Error")
            self.history_label.configure(
                text=str(error),
                fg="#FF6B81"
            )

    def format_result(self, value):
        if isinstance(value, int):
            return str(value)

        if abs(value) < 1e-12:
            value = 0

        if float(value).is_integer():
            return str(int(value))

        return f"{value:.12g}"

    # ---------------------------------------------------------
    # Mode / history
    # ---------------------------------------------------------

    def toggle_angle_mode(self):
        if self.calculator.angle_mode == "DEG":
            self.calculator.angle_mode = "RAD"
        else:
            self.calculator.angle_mode = "DEG"

        self.mode_button.configure(
            text=self.calculator.angle_mode
        )

    def update_history_label(self):
        if not self.history:
            self.history_label.configure(
                text="No calculations yet",
                fg=self.MUTED
            )
            return

        self.history_label.configure(
            text="  •  ".join(self.history[:3]),
            fg=self.MUTED
        )

    def clear_history(self):
        self.history.clear()
        self.update_history_label()

    def show_history(self):
        if not self.history:
            messagebox.showinfo(
                "History",
                "No calculations yet."
            )
            return

        messagebox.showinfo(
            "Calculation History",
            "\n\n".join(self.history)
        )

    # ---------------------------------------------------------
    # Keyboard
    # ---------------------------------------------------------

    def bind_keyboard(self):
        self.root.bind("<Return>", lambda event: self.calculate())
        self.root.bind("<KP_Enter>", lambda event: self.calculate())
        self.root.bind("<Escape>", lambda event: self.clear())
        self.root.bind("<BackSpace>", lambda event: self.backspace())

        self.root.bind(
            "<Key>",
            self.keyboard_input
        )

    def keyboard_input(self, event):
        key = event.char

        allowed = "0123456789.+-*/()%"

        if key in allowed:
            self.expression.set(
                self.expression.get() + key
            )
