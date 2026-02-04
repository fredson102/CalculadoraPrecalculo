import tkinter as tk
from tkinter import ttk, messagebox

import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)

TRANSFORMS = standard_transformations + (implicit_multiplication_application,)


def _show_error(err: Exception):
    messagebox.showerror("Error", str(err))


def _parse_expression(text: str):
    return parse_expr(text, transformations=TRANSFORMS, evaluate=True)


def _format_result(expr):
    try:
        return sp.pretty(expr)
    except Exception:
        return str(expr)


def solve_problem(text: str):
    text = text.strip()
    if not text:
        raise ValueError("Escribe un problema matemático")

    lowered = text.lower().strip()

    if lowered.startswith("deriv:"):
        expr_text = text.split(":", 1)[1].strip()
        expr = _parse_expression(expr_text)
        x = sp.Symbol("x")
        return sp.diff(expr, x)

    if lowered.startswith("integral:"):
        expr_text = text.split(":", 1)[1].strip()
        expr = _parse_expression(expr_text)
        x = sp.Symbol("x")
        return sp.integrate(expr, x)

    if "=" in text:
        left, right = text.split("=", 1)
        lhs = _parse_expression(left)
        rhs = _parse_expression(right)
        eq = sp.Eq(lhs, rhs)
        symbols = list(eq.free_symbols)
        if not symbols:
            return sp.simplify(lhs - rhs)
        target = sp.Symbol("x") if sp.Symbol("x") in symbols else symbols[0]
        return sp.solve(eq, target)

    expr = _parse_expression(text)
    simplified = sp.simplify(expr)

    if not simplified.free_symbols:
        return sp.N(simplified)

    return simplified


class CalculadoraGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora PreCálculo")
        self.geometry("980x640")
        self.minsize(920, 600)

        self.configure(bg="#0b1120")
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TFrame", background="#0b1120")
        style.configure("TLabel", background="#0b1120", foreground="#e2e8f0", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 20, "bold"), foreground="#38bdf8")
        style.configure("SubHeader.TLabel", font=("Segoe UI", 11), foreground="#94a3b8")
        style.configure("TButton", font=("Segoe UI", 10, "bold"))
        style.configure("Card.TFrame", background="#0f172a")

        header = ttk.Frame(self)
        header.pack(fill="x", padx=20, pady=(16, 8))
        ttk.Label(header, text="Calculadora PreCálculo", style="Header.TLabel").pack(side="left")
        ttk.Label(header, text="Escribe tu problema y obtén la solución", style="SubHeader.TLabel").pack(
            side="left", padx=12
        )

        card = ttk.Frame(self, style="Card.TFrame")
        card.pack(fill="both", expand=True, padx=20, pady=12)

        self.input_text = tk.Text(
            card,
            height=3,
            bg="#0b1220",
            fg="#e2e8f0",
            insertbackground="#e2e8f0",
            font=("Consolas", 14),
            wrap="word",
        )
        self.input_text.pack(fill="x", padx=16, pady=(16, 8))
        self.input_text.insert(
            "end",
            "Ejemplos: 2x + 5 = 17   |   deriv: x^2 + 3x   |   integral: sin(x)\n",
        )

        actions = ttk.Frame(card)
        actions.pack(fill="x", padx=16, pady=(0, 10))
        ttk.Button(actions, text="Resolver", command=self.on_solve).pack(side="left")
        ttk.Button(actions, text="Limpiar", command=self.on_clear).pack(side="left", padx=8)
        ttk.Button(actions, text="Ejemplos", command=self.on_examples).pack(side="left")

        self.output = tk.Text(
            card,
            height=18,
            bg="#0b1220",
            fg="#e2e8f0",
            insertbackground="#e2e8f0",
            font=("Consolas", 12),
            wrap="word",
        )
        self.output.pack(fill="both", expand=True, padx=16, pady=(0, 16))
        self.output.insert("end", "Resultados aparecerán aquí...\n")

    def on_clear(self):
        self.input_text.delete("1.0", "end")
        self.output.delete("1.0", "end")

    def on_examples(self):
        examples = (
            "2x + 5 = 17\n"
            "x^2 - 5x + 6 = 0\n"
            "(x+2)(x-3)\n"
            "deriv: x^3 + 2x\n"
            "integral: sin(x)\n"
        )
        self.input_text.delete("1.0", "end")
        self.input_text.insert("end", examples)

    def on_solve(self):
        try:
            text = self.input_text.get("1.0", "end").strip()
            if not text:
                raise ValueError("Escribe un problema matemático")

            results = []
            for line in text.splitlines():
                line = line.strip()
                if not line:
                    continue
                res = solve_problem(line)
                results.append(f"> {line}\n{_format_result(res)}\n")

            self.output.delete("1.0", "end")
            self.output.insert("end", "\n".join(results))
        except Exception as e:
            _show_error(e)


def main():
    app = CalculadoraGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
