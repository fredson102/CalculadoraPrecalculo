import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext

import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
)
from sympy import (
    Symbol, symbols, solve, diff, integrate, limit, summation,
    expand, factor, simplify, apart, together, cancel,
    sin, cos, tan, asin, acos, atan, sinh, cosh, tanh,
    exp, log, sqrt, Abs, Rational, oo, I, pi, E,
    Matrix
)

TRANSFORMS = standard_transformations + (implicit_multiplication_application,)


def _show_error(err: Exception):
    messagebox.showerror("Error", str(err))


def _parse_expression(text: str):
    """Parsea una expresión matemática"""
    try:
        return parse_expr(text, transformations=TRANSFORMS, evaluate=False)
    except Exception as e:
        raise ValueError(f"Expresión inválida: {e}")


def _format_result(expr):
    """Formatea el resultado para visualización"""
    try:
        return sp.pretty(expr, use_unicode=True)
    except Exception:
        return str(expr)


def solve_with_steps(text: str):
    """Resuelve un problema y devuelve pasos detallados"""
    text = text.strip()
    if not text:
        raise ValueError("Escribe un problema matemático")

    lowered = text.lower().strip()
    steps = []

    # Derivada
    if lowered.startswith("deriv:") or lowered.startswith("d:"):
        expr_text = text.split(":", 1)[1].strip()
        expr = _parse_expression(expr_text)
        x = Symbol("x")
        steps.append(f"📊 Función original: f(x) = {_format_result(expr)}")
        derivative = diff(expr, x)
        steps.append(f"➜ Derivada: f'(x) = {_format_result(derivative)}")
        steps.append(f"✓ Usando la regla de potencia y suma")
        return "\n".join(steps), derivative

    # Integral
    if lowered.startswith("integral:") or lowered.startswith("∫:"):
        expr_text = text.split(":", 1)[1].strip()
        expr = _parse_expression(expr_text)
        x = Symbol("x")
        steps.append(f"📊 Integrando: {_format_result(expr)}")
        integral = integrate(expr, x)
        steps.append(f"➜ Integral indefinida:")
        steps.append(f"   ∫ {_format_result(expr)} dx = {_format_result(integral)} + C")
        steps.append(f"✓ Donde C es la constante de integración")
        return "\n".join(steps), integral

    # Límite
    if lowered.startswith("lim:") or lowered.startswith("limit:"):
        parts = text.split(":", 1)[1].strip()
        try:
            expr_text, point = parts.rsplit(",", 1)
            expr = _parse_expression(expr_text.strip())
            x = Symbol("x")
            point_val = float(point.strip()) if point.strip() != "oo" else oo
            steps.append(f"📊 Función: {_format_result(expr)}")
            steps.append(f"➜ Evaluando lím (x → {point.strip()})")
            lim = limit(expr, x, point_val)
            steps.append(f"✓ Límite = {_format_result(lim)}")
            return "\n".join(steps), lim
        except ValueError:
            raise ValueError("Formato: lim: expr, punto (ej: lim: (x^2-1)/(x-1), 1)")

    # Sumatoria
    if lowered.startswith("sum:") or lowered.startswith("σ:"):
        expr_text = text.split(":", 1)[1].strip()
        expr = _parse_expression(expr_text)
        n = Symbol("n")
        steps.append(f"📊 Sumando: {_format_result(expr)}")
        steps.append(f"➜ Para n desde 1 hasta n")
        suma = summation(expr, (n, 1, n))
        steps.append(f"✓ Resultado: {_format_result(suma)}")
        return "\n".join(steps), suma

    # Expandir
    if lowered.startswith("expand:"):
        expr_text = text.split(":", 1)[1].strip()
        expr = _parse_expression(expr_text)
        steps.append(f"📊 Expresión original: {_format_result(expr)}")
        expanded = expand(expr)
        steps.append(f"➜ Paso: Distribuir términos")
        steps.append(f"✓ Expandida: {_format_result(expanded)}")
        return "\n".join(steps), expanded

    # Factorizar
    if lowered.startswith("factor:"):
        expr_text = text.split(":", 1)[1].strip()
        expr = _parse_expression(expr_text)
        steps.append(f"📊 Expresión original: {_format_result(expr)}")
        factored = factor(expr)
        steps.append(f"➜ Buscando factores comunes")
        steps.append(f"✓ Factorizada: {_format_result(factored)}")
        return "\n".join(steps), factored

    # Fracciones parciales
    if lowered.startswith("apart:"):
        expr_text = text.split(":", 1)[1].strip()
        expr = _parse_expression(expr_text)
        x = Symbol("x")
        steps.append(f"📊 Expresión racional: {_format_result(expr)}")
        partial = apart(expr, x)
        steps.append(f"➜ Descomposición en fracciones parciales:")
        steps.append(f"{_format_result(partial)}")
        return "\n".join(steps), partial

    # Estadística: media
    if lowered.startswith("mean:"):
        data_str = text.split(":", 1)[1].strip()
        try:
            data = [float(x.strip()) for x in data_str.split(",")]
            steps.append(f"📊 Datos: {data}")
            mean_val = sum(data) / len(data)
            steps.append(f"➜ Media = (Σx) / n = {sum(data)} / {len(data)}")
            steps.append(f"✓ μ = {mean_val:.6f}")
            return "\n".join(steps), mean_val
        except ValueError:
            raise ValueError("Formato: mean: 1,2,3,4,5")

    # Estadística: varianza
    if lowered.startswith("var:"):
        data_str = text.split(":", 1)[1].strip()
        try:
            data = [float(x.strip()) for x in data_str.split(",")]
            steps.append(f"📊 Datos: {data}")
            mean_val = sum(data) / len(data)
            variance = sum((x - mean_val)**2 for x in data) / len(data)
            steps.append(f"➜ Paso 1 - Media: {mean_val:.6f}")
            steps.append(f"➜ Paso 2 - Σ(x - μ)² = {sum((x - mean_val)**2 for x in data):.6f}")
            steps.append(f"➜ Paso 3 - Varianza = Σ(x - μ)² / n")
            steps.append(f"✓ σ² = {variance:.6f}")
            return "\n".join(steps), variance
        except ValueError:
            raise ValueError("Formato: var: 1,2,3,4,5")

    # Estadística: desviación estándar
    if lowered.startswith("std:"):
        data_str = text.split(":", 1)[1].strip()
        try:
            data = [float(x.strip()) for x in data_str.split(",")]
            steps.append(f"📊 Datos: {data}")
            mean_val = sum(data) / len(data)
            variance = sum((x - mean_val)**2 for x in data) / len(data)
            std = variance ** 0.5
            steps.append(f"➜ Paso 1 - Media: {mean_val:.6f}")
            steps.append(f"➜ Paso 2 - Varianza: σ² = {variance:.6f}")
            steps.append(f"➜ Paso 3 - Desv. Est. = √(σ²)")
            steps.append(f"✓ σ = {std:.6f}")
            return "\n".join(steps), std
        except ValueError:
            raise ValueError("Formato: std: 1,2,3,4,5")

    # Combinatorias: Combinaciones
    if lowered.startswith("comb:") or lowered.startswith("c("):
        try:
            text_clean = text.split(":", 1)[1].strip() if ":" in text else text
            n_str, r_str = text_clean.replace("C(", "").replace(")", "").split(",")
            n, r = int(n_str.strip()), int(r_str.strip())
            from math import factorial
            comb = factorial(n) // (factorial(r) * factorial(n - r))
            steps.append(f"📊 Combinación: C({n},{r})")
            steps.append(f"➜ Fórmula: C(n,r) = n! / (r!(n-r)!)")
            steps.append(f"➜ C({n},{r}) = {n}! / ({r}!×{n-r}!)")
            steps.append(f"✓ Resultado: {comb}")
            return "\n".join(steps), comb
        except ValueError:
            raise ValueError("Formato: comb: n,r (ej: comb: 5,2)")

    # Combinatorias: Permutaciones
    if lowered.startswith("perm:") or lowered.startswith("p("):
        try:
            text_clean = text.split(":", 1)[1].strip() if ":" in text else text
            n_str, r_str = text_clean.replace("P(", "").replace(")", "").split(",")
            n, r = int(n_str.strip()), int(r_str.strip())
            from math import factorial
            perm = factorial(n) // factorial(n - r)
            steps.append(f"📊 Permutación: P({n},{r})")
            steps.append(f"➜ Fórmula: P(n,r) = n! / (n-r)!")
            steps.append(f"➜ P({n},{r}) = {n}! / {n-r}!")
            steps.append(f"✓ Resultado: {perm}")
            return "\n".join(steps), perm
        except ValueError:
            raise ValueError("Formato: perm: n,r (ej: perm: 5,2)")

    # Ecuación
    if "=" in text:
        left, right = text.split("=", 1)
        lhs = _parse_expression(left.strip())
        rhs = _parse_expression(right.strip())
        steps.append(f"📊 Ecuación: {_format_result(lhs)} = {_format_result(rhs)}")
        eq = sp.Eq(lhs, rhs)
        symbols_found = list(eq.free_symbols)
        if not symbols_found:
            result = simplify(lhs - rhs)
            steps.append(f"➜ Simplificando: {_format_result(result)}")
            return "\n".join(steps), result
        target = Symbol("x") if Symbol("x") in symbols_found else symbols_found[0]
        steps.append(f"➜ Resolviendo para: {target}")
        solutions = solve(eq, target)
        if not solutions:
            steps.append(f"✗ Sin soluciones reales")
            return "\n".join(steps), "Sin soluciones"
        for i, sol in enumerate(solutions, 1):
            steps.append(f"✓ Solución {i}: {target} = {_format_result(sol)}")
        return "\n".join(steps), solutions if len(solutions) > 1 else solutions[0]

    # Simplificar/Evaluar
    expr = _parse_expression(text)
    steps.append(f"📊 Expresión: {_format_result(expr)}")
    simplified = simplify(expr)
    if simplified != expr:
        steps.append(f"➜ Simplificada: {_format_result(simplified)}")
    if not simplified.free_symbols:
        numerical = float(sp.N(simplified))
        steps.append(f"✓ Valor: {numerical:.10g}")
        return "\n".join(steps), numerical
    steps.append(f"✓ Resultado: {_format_result(simplified)}")
    return "\n".join(steps), simplified



class CalculadoraGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora PreCálculo Pro")
        self.geometry("1100x750")
        self.minsize(1000, 700)

        self.configure(bg="#0b1120")
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TFrame", background="#0b1120")
        style.configure("TLabel", background="#0b1120", foreground="#e2e8f0", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 22, "bold"), foreground="#38bdf8")
        style.configure("SubHeader.TLabel", font=("Segoe UI", 10), foreground="#94a3b8")
        style.configure("TButton", font=("Segoe UI", 10, "bold"))
        style.configure("Card.TFrame", background="#0f172a", relief="flat")

        # Header
        header = ttk.Frame(self)
        header.pack(fill="x", padx=20, pady=(16, 12))
        ttk.Label(header, text="✓ Calculadora PreCálculo Pro", style="Header.TLabel").pack(side="left")
        ttk.Label(
            header, text="Resuelve problemas con pasos detallados", style="SubHeader.TLabel"
        ).pack(side="left", padx=16)

        # Main container
        main_container = ttk.Frame(self)
        main_container.pack(fill="both", expand=True, padx=20, pady=12)

        # Left panel - Input
        left_panel = ttk.Frame(main_container, style="Card.TFrame")
        left_panel.pack(side="left", fill="both", expand=True, padx=(0, 10))

        ttk.Label(left_panel, text="Escribe tu problema", style="Header.TLabel").pack(
            padx=16, pady=(12, 8), anchor="w"
        )

        self.input_text = tk.Text(
            left_panel,
            height=6,
            bg="#0b1220",
            fg="#e2e8f0",
            font=("Fira Code", 11),
            insertbackground="#38bdf8",
            wrap="word",
            padx=12,
            pady=10,
        )
        self.input_text.pack(fill="both", expand=True, padx=12, pady=12)
        self.input_text.bind("<Control-Return>", lambda e: self.on_solve())

        # Buttons
        btn_frame = ttk.Frame(left_panel)
        btn_frame.pack(fill="x", padx=12, pady=(0, 12))

        btn_solve = tk.Button(
            btn_frame,
            text="🔍 Resolver",
            command=self.on_solve,
            bg="#38bdf8",
            fg="#0b1120",
            font=("Segoe UI", 11, "bold"),
            activebackground="#60a5fa",
            padx=20,
            pady=8,
            border=0,
        )
        btn_solve.pack(side="left", padx=4)

        btn_clear = tk.Button(
            btn_frame,
            text="🗑️ Limpiar",
            command=self.on_clear,
            bg="#475569",
            fg="#e2e8f0",
            font=("Segoe UI", 11, "bold"),
            activebackground="#64748b",
            padx=20,
            pady=8,
            border=0,
        )
        btn_clear.pack(side="left", padx=4)

        btn_examples = tk.Button(
            btn_frame,
            text="📚 Ejemplos",
            command=self.on_examples,
            bg="#8b5cf6",
            fg="#fff",
            font=("Segoe UI", 11, "bold"),
            activebackground="#a78bfa",
            padx=20,
            pady=8,
            border=0,
        )
        btn_examples.pack(side="left", padx=4)

        # Right panel - Output
        right_panel = ttk.Frame(main_container, style="Card.TFrame")
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0))

        ttk.Label(right_panel, text="Solución paso a paso", style="Header.TLabel").pack(
            padx=16, pady=(12, 8), anchor="w"
        )

        self.output_text = scrolledtext.ScrolledText(
            right_panel,
            bg="#0b1220",
            fg="#e2e8f0",
            font=("Fira Code", 10),
            wrap="word",
            padx=12,
            pady=10,
        )
        self.output_text.pack(fill="both", expand=True, padx=12, pady=12)

        # Configure text tags for styling
        self.output_text.tag_configure("header", foreground="#38bdf8", font=("Fira Code", 11, "bold"))
        self.output_text.tag_configure("step", foreground="#94a3b8")
        self.output_text.tag_configure("result", foreground="#34d399", font=("Fira Code", 11, "bold"))
        self.output_text.tag_configure("error", foreground="#f87171")

    def on_solve(self):
        text = self.input_text.get("1.0", "end").strip()
        if not text:
            messagebox.showwarning("Aviso", "Escribe un problema para resolver")
            return

        self.output_text.delete("1.0", "end")
        try:
            steps, result = solve_with_steps(text)
            self.output_text.insert("end", steps, "step")
        except Exception as e:
            self.output_text.insert("end", f"❌ Error: {str(e)}", "error")

    def on_clear(self):
        self.input_text.delete("1.0", "end")
        self.output_text.delete("1.0", "end")
        self.input_text.focus()

    def on_examples(self):
        examples = [
            ("Ecuación lineal", "2x + 5 = 17"),
            ("Ecuación cuadrática", "x^2 - 5x + 6 = 0"),
            ("Derivada", "deriv: x^3 + 2x^2 - x + 5"),
            ("Integral", "integral: x^2 + 2x"),
            ("Factorizar", "factor: x^2 - 9"),
            ("Expandir", "expand: (x + 3)(x - 2)"),
            ("Límite", "lim: (x^2 - 1)/(x - 1), 1"),
            ("Fracciones parciales", "apart: (2x + 3)/(x^2 - 1)"),
            ("Media", "mean: 5,10,15,20,25"),
            ("Varianza", "var: 2,4,6,8,10"),
            ("Desv. Est.", "std: 3,6,9,12,15"),
            ("Combinaciones", "comb: 5,2"),
            ("Permutaciones", "perm: 5,2"),
            ("Trigonometría", "sin(pi/6) + cos(pi/3)"),
            ("Logaritmos", "log(100, 10) + log(e)"),
        ]

        dialog = tk.Toplevel(self)
        dialog.title("Ejemplos de Problemas")
        dialog.geometry("500x450")
        dialog.configure(bg="#0b1120")

        ttk.Label(dialog, text="Haz clic en un ejemplo para copiarlo:", style="SubHeader.TLabel").pack(
            padx=12, pady=12
        )

        frame = ttk.Frame(dialog)
        frame.pack(fill="both", expand=True, padx=12, pady=12)

        for category, example in examples:
            btn = tk.Button(
                frame,
                text=f"► {category}: {example}",
                command=lambda e=example: self._copy_example(e, dialog),
                bg="#0f172a",
                fg="#38bdf8",
                font=("Segoe UI", 9),
                activebackground="#1e293b",
                activeforeground="#60a5fa",
                anchor="w",
                padx=12,
                pady=8,
                border=0,
            )
            btn.pack(fill="x", pady=2)

    def _copy_example(self, example: str, dialog):
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", example)
        dialog.destroy()
        self.input_text.focus()


if __name__ == "__main__":
    app = CalculadoraGUI()
    app.mainloop()
