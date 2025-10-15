import tkinter as tk
from tkinter import messagebox, simpledialog
import math
import statistics
import re

class RizsioFX333S:
    def __init__(self, root):
        self.root = root
        self.root.title("rizsio fx-333s")
        self.root.geometry("400x600")
        self.root.configure(bg="#FFFBE6")
        self.root.minsize(350, 500)
        self.root.resizable(True, True)

        self.equation = tk.StringVar()
        self.display = tk.Entry(root, textvariable=self.equation, font=("arial", 24, "bold"), bd=10, insertwidth=2, width=15,
                                borderwidth=4, relief="ridge", justify="right", bg="white", fg="#444")
        self.display.grid(row=0, column=0, columnspan=5, ipadx=8, ipady=15, pady=10)

        self.deg_mode = True
        self.sci_notation = False

        self._build_ui()

    def _build_ui(self):
        button_style = {"font": ("arial", 14, "bold"), "bg": "#FFF5B8", "fg": "#444", "bd": 2, "relief": "ridge", "width": 5, "height": 2}

        buttons = [
            ("sin", 1, 0), ("cos", 1, 1), ("tan", 1, 2), ("ln", 1, 3), ("log", 1, 4),
            ("asin", 2, 0), ("acos", 2, 1), ("atan", 2, 2), ("sqrt", 2, 3), ("^", 2, 4),
            ("7", 3, 0), ("8", 3, 1), ("9", 3, 2), ("/", 3, 3), ("(", 3, 4),
            ("4", 4, 0), ("5", 4, 1), ("6", 4, 2), ("*", 4, 3), (")", 4, 4),
            ("1", 5, 0), ("2", 5, 1), ("3", 5, 2), ("-", 5, 3), ("π", 5, 4),
            ("0", 6, 0), (".", 6, 1), ("+", 6, 2), ("!", 6, 3), ("e", 6, 4),
            ("C", 7, 0), ("⌫", 7, 1), ("=", 7, 2), ("DEG", 7, 3), ("STAT", 7, 4)
        ]

        for (text, row, col) in buttons:
            action = lambda x=text: self._on_click(x)
            tk.Button(self.root, text=text, command=action, **button_style).grid(row=row, column=col, padx=2, pady=2, sticky="nsew")

        for i in range(8):
            self.root.rowconfigure(i, weight=1)
        for i in range(5):
            self.root.columnconfigure(i, weight=1)

    def _on_click(self, key):
        if key == "C":
            self.equation.set("")
        elif key == "⌫":
            self.equation.set(self.equation.get()[:-1])
        elif key == "=":
            self._calculate()
        elif key == "DEG":
            self.deg_mode = not self.deg_mode
            messagebox.showinfo("Angle Mode", f"Mode: {'Degrees' if self.deg_mode else 'Radians'}")
        elif key == "π":
            self.equation.set(self.equation.get() + str(math.pi))
        elif key == "e":
            self.equation.set(self.equation.get() + str(math.e))
        elif key == "STAT":
            self._statistics_dialog()
        else:
            self.equation.set(self.equation.get() + key)

    def _calculate(self):
        try:
            expr = self.equation.get()
            expr = expr.replace("^", "**")
            expr = self._implicit_multiplication(expr)
            expr = self._replace_trig(expr)
            expr = self._replace_factorial(expr)

            allowed_names = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
            allowed_names["math"] = math

            result = eval(expr, {"__builtins__": {}}, allowed_names)
            if self.sci_notation:
                result = f"{result:.6e}"
            else:
                result = round(result, 10)
            self.equation.set(result)
        except Exception:
            messagebox.showerror("Error", "Invalid Input")

    def _replace_trig(self, expr):
        expr = re.sub(r"sin\((.*?)\)", lambda m: f"math.sin(math.radians({m.group(1)}))" if self.deg_mode else f"math.sin({m.group(1)})", expr)
        expr = re.sub(r"cos\((.*?)\)", lambda m: f"math.cos(math.radians({m.group(1)}))" if self.deg_mode else f"math.cos({m.group(1)})", expr)
        expr = re.sub(r"tan\((.*?)\)", lambda m: f"math.tan(math.radians({m.group(1)}))" if self.deg_mode else f"math.tan({m.group(1)})", expr)
        expr = re.sub(r"asin\((.*?)\)", lambda m: f"math.degrees(math.asin({m.group(1)}))" if self.deg_mode else f"math.asin({m.group(1)})", expr)
        expr = re.sub(r"acos\((.*?)\)", lambda m: f"math.degrees(math.acos({m.group(1)}))" if self.deg_mode else f"math.acos({m.group(1)})", expr)
        expr = re.sub(r"atan\((.*?)\)", lambda m: f"math.degrees(math.atan({m.group(1)}))" if self.deg_mode else f"math.atan({m.group(1)})", expr)
        expr = re.sub(r"ln\((.*?)\)", r"math.log(\1)", expr)
        expr = re.sub(r"log\((.*?)\)", r"math.log10(\1)", expr)
        expr = re.sub(r"sqrt\((.*?)\)", r"math.sqrt(\1)", expr)
        return expr

    def _replace_factorial(self, expr):
        return re.sub(r"(\d+|\))!", r"math.factorial(\1)", expr)

    def _implicit_multiplication(self, expr):
        expr = re.sub(r"(\d|\))\s*(\()", r"\1*\2", expr)
        expr = re.sub(r"(\))\s*(\d|\()", r"\1*\2", expr)
        expr = re.sub(r"(\d)([a-zA-Z])", r"\1*\2", expr)
        return expr

    def _statistics_dialog(self):
        try:
            data = simpledialog.askstring("Statistics", "Enter numbers separated by commas:")
            if not data:
                return
            numbers = [float(x.strip()) for x in data.split(",")]
            msg = (
                f"Count: {len(numbers)}\n"
                f"Sum: {sum(numbers)}\n"
                f"Mean: {statistics.mean(numbers)}\n"
                f"Median: {statistics.median(numbers)}\n"
                f"Stdev: {statistics.stdev(numbers) if len(numbers) > 1 else 'N/A'}"
            )
            messagebox.showinfo("Statistics", msg)
        except Exception:
            messagebox.showerror("Error", "Invalid input for statistics")

if __name__ == "__main__":
    root = tk.Tk()
    app = RizsioFX333S(root)
    root.mainloop()