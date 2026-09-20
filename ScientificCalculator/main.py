import tkinter as tk

from ui import ScientificCalculatorUI


def main():
    root = tk.Tk()

    app = ScientificCalculatorUI(root)

    root.mainloop()


if __name__ == "__main__":
    main()
