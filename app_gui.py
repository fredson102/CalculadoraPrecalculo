import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import re
from math import factorial, comb as math_comb, perm as math_perm

import sympy as sp
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor,
)
from sympy import (
    Symbol, symbols, solve, diff, integrate, limit, summation,
    expand, factor, simplify, apart, together, cancel, gcd,
    sin, cos, tan, asin, acos, atan, sinh, cosh, tanh,
    exp, log, sqrt, Abs, Rational, oo, I, pi, E,
    Matrix, solveset, roots, degree, Poly, fraction,
    dsolve, Function, Derivative, series, summation, Product,
    factorint, divisors, isprime, factorial as sp_factorial,
    binomial, rf, ff, zeta, polygamma, floor, ceiling
)

TRANSFORMS = (standard_transformations + (implicit_multiplication_application, convert_xor))


def _show_error(err: Exception):
    messagebox.showerror("Error", str(err))



def _parse_expression(text: str):
    """Parsea una expresión matemática con símbolos mejorados"""
    try:
        # Reemplazar símbolos matemáticos comunes
        text = text.replace('π', 'pi').replace('∞', 'oo')
        text = text.replace('Σ', 'summation').replace('∑', 'summation')
        text = text.replace('√', 'sqrt').replace('Π', 'Product')
        text = text.replace('°', '*pi/180')  # Grados a radianes
        
        # Permitir notación de potencia sin ^
        text = re.sub(r'(\w+)\*\*', r'\1**', text)
        
        return parse_expr(text, transformations=TRANSFORMS, evaluate=False, local_dict={
            'sin': sin, 'cos': cos, 'tan': tan,
            'asin': asin, 'acos': acos, 'atan': atan,
            'sinh': sinh, 'cosh': cosh, 'tanh': tanh,
            'exp': exp, 'log': log, 'sqrt': sqrt, 'abs': Abs,
            'pi': pi, 'e': E, 'E': E, 'I': I,
            'oo': oo, 'factorial': sp_factorial, 'binomial': binomial,
            'floor': floor, 'ceiling': ceiling,
            'summation': summation, 'Product': Product
        })
    except Exception as e:
        raise ValueError(f"Expresión inválida: {str(e)[:100]}")


def _format_result(expr):
    """Formatea el resultado para visualización"""
    try:
        if isinstance(expr, (int, float)):
            return str(expr)
        return sp.pretty(expr, use_unicode=True)
    except Exception:
        return str(expr)


def _try_numeric(expr):
    """Intenta evaluar numéricamente si es posible"""
    try:
        if not expr.free_symbols:
            result = float(sp.N(expr))
            if result == int(result):
                return int(result)
            return round(result, 10)
    except:
        pass
    return None


def solve_with_steps(text: str):
    """Resuelve un problema y devuelve pasos detallados"""
    text = text.strip()
    if not text:
        raise ValueError("Escribe un problema matemático")

    lowered = text.lower().strip()
    steps = []

    # ============ COMANDOS EXPLÍCITOS ============
    
    # Derivada
    if lowered.startswith(("deriv:", "d:", "derivative:")):
        expr_text = text.split(":", 1)[1].strip()
        expr = _parse_expression(expr_text)
        x = Symbol("x")
        steps.append(f"📊 Función: f(x) = {_format_result(expr)}")
        derivative = diff(expr, x)
        steps.append(f"➜ f'(x) = {_format_result(derivative)}")
        num = _try_numeric(derivative)
        if num is not None:
            steps.append(f"✓ Valor numérico: {num}")
        return "\n".join(steps), derivative

    # Integral
    if lowered.startswith(("integral:", "∫:", "int:")):
        expr_text = text.split(":", 1)[1].strip()
        expr = _parse_expression(expr_text)
        x = Symbol("x")
        steps.append(f"📊 Integrando: {_format_result(expr)}")
        try:
            integral = integrate(expr, x)
            steps.append(f"➜ ∫ {_format_result(expr)} dx = {_format_result(integral)} + C")
        except Exception:
            integral = None
            steps.append(f"✗ No se puede integrar analíticamente")
        return "\n".join(steps), integral

    # Límite
    if lowered.startswith(("lim:", "limit:")):
        parts = text.split(":", 1)[1].strip()
        try:
            expr_text, point = parts.rsplit(",", 1)
            expr = _parse_expression(expr_text.strip())
            x = Symbol("x")
            point_val = float(point.strip()) if point.strip() != "oo" else oo
            steps.append(f"📊 lím (x→{point.strip()}) [{_format_result(expr)}]")
            lim = limit(expr, x, point_val)
            steps.append(f"✓ = {_format_result(lim)}")
            return "\n".join(steps), lim
        except Exception as e:
            raise ValueError("Formato: lim: expr, punto")

    # Expandir
    if lowered.startswith("expand:"):
        expr_text = text.split(":", 1)[1].strip()
        expr = _parse_expression(expr_text)
        steps.append(f"📊 Expandir: {_format_result(expr)}")
        expanded = expand(expr)
        steps.append(f"✓ = {_format_result(expanded)}")
        return "\n".join(steps), expanded

    # Factorizar
    if lowered.startswith("factor:"):
        expr_text = text.split(":", 1)[1].strip()
        expr = _parse_expression(expr_text)
        steps.append(f"📊 Factorizar: {_format_result(expr)}")
        try:
            factored = factor(expr)
            steps.append(f"✓ = {_format_result(factored)}")
        except Exception:
            steps.append(f"✗ No se puede factorizar")
            factored = expr
        return "\n".join(steps), factored

    # Simplificar
    if lowered.startswith(("simplify:", "simpl:")):
        expr_text = text.split(":", 1)[1].strip()
        expr = _parse_expression(expr_text)
        steps.append(f"📊 Simplificar: {_format_result(expr)}")
        simplified = simplify(expr)
        steps.append(f"✓ = {_format_result(simplified)}")
        return "\n".join(steps), simplified

    # Fracciones parciales
    if lowered.startswith("apart:"):
        expr_text = text.split(":", 1)[1].strip()
        expr = _parse_expression(expr_text)
        x = Symbol("x")
        steps.append(f"📊 Descomponer en fracciones parciales:")
        steps.append(f"   {_format_result(expr)}")
        try:
            partial = apart(expr, x)
            steps.append(f"✓ = {_format_result(partial)}")
        except Exception:
            steps.append(f"✗ No se puede descomponer")
            partial = expr
        return "\n".join(steps), partial

    # Estadística
    if lowered.startswith(("mean:", "μ:", "media:")):
        data_str = text.split(":", 1)[1].strip()
        try:
            data = [float(x.strip()) for x in data_str.split(",")]
            mean_val = sum(data) / len(data)
            steps.append(f"📊 Datos: {data}")
            steps.append(f"➜ μ = (Σx) / n = {sum(data)} / {len(data)}")
            steps.append(f"✓ μ = {mean_val:.6g}")
            return "\n".join(steps), mean_val
        except ValueError:
            raise ValueError("Formato: mean: 1,2,3,4,5")

    if lowered.startswith(("var:", "variance:", "σ²:")):
        data_str = text.split(":", 1)[1].strip()
        try:
            data = [float(x.strip()) for x in data_str.split(",")]
            mean_val = sum(data) / len(data)
            variance = sum((x - mean_val)**2 for x in data) / len(data)
            steps.append(f"📊 Datos: {data}")
            steps.append(f"➜ Media: {mean_val:.6g}")
            steps.append(f"➜ σ² = Σ(x - μ)² / n = {variance:.6g}")
            return "\n".join(steps), variance
        except ValueError:
            raise ValueError("Formato: var: 1,2,3,4,5")

    if lowered.startswith(("std:", "stdev:", "σ:")):
        data_str = text.split(":", 1)[1].strip()
        try:
            data = [float(x.strip()) for x in data_str.split(",")]
            mean_val = sum(data) / len(data)
            variance = sum((x - mean_val)**2 for x in data) / len(data)
            std = variance ** 0.5
            steps.append(f"📊 Datos: {data}")
            steps.append(f"➜ σ² = {variance:.6g}")
            steps.append(f"➜ σ = √(σ²) = {std:.6g}")
            return "\n".join(steps), std
        except ValueError:
            raise ValueError("Formato: std: 1,2,3,4,5")

    # Combinatorias
    if lowered.startswith(("comb:", "c(")):
        try:
            text_clean = text.split(":", 1)[1].strip() if ":" in text else text
            n_str, r_str = text_clean.replace("C(", "").replace(")", "").split(",")
            n, r = int(n_str.strip()), int(r_str.strip())
            comb_val = binomial(n, r)
            steps.append(f"📊 C({n},{r}) = {n}! / ({r}! × {n-r}!)")
            steps.append(f"✓ = {comb_val}")
            return "\n".join(steps), comb_val
        except Exception:
            raise ValueError("Formato: comb: n,r")

    if lowered.startswith(("perm:", "p(")):
        try:
            text_clean = text.split(":", 1)[1].strip() if ":" in text else text
            n_str, r_str = text_clean.replace("P(", "").replace(")", "").split(",")
            n, r = int(n_str.strip()), int(r_str.strip())
            perm_val = factorial(n) // factorial(n - r)
            steps.append(f"📊 P({n},{r}) = {n}! / {n-r}!")
            steps.append(f"✓ = {perm_val}")
            return "\n".join(steps), perm_val
        except Exception:
            raise ValueError("Formato: perm: n,r")

    # ============ DETECCIÓN AUTOMÁTICA ============

    # Ecuación (contiene =)
    if "=" in text:
        parts = text.split("=", 1)
        if len(parts) == 2:
            left_str, right_str = parts
            try:
                lhs = _parse_expression(left_str.strip())
                rhs = _parse_expression(right_str.strip())
                eq = sp.Eq(lhs, rhs)
                symbols_found = list(eq.free_symbols)
                
                if not symbols_found:
                    result = simplify(lhs - rhs)
                    steps.append(f"📊 {_format_result(lhs)} = {_format_result(rhs)}")
                    steps.append(f"✓ {_format_result(result)}")
                    return "\n".join(steps), result
                
                # Detectar tipo de ecuación
                target = Symbol("x") if Symbol("x") in symbols_found else symbols_found[0]
                
                # Intentar resolver
                try:
                    solutions = solve(eq, target)
                    if not solutions:
                        steps.append(f"📊 {_format_result(lhs)} = {_format_result(rhs)}")
                        steps.append(f"✗ Sin soluciones")
                        return "\n".join(steps), None
                    
                    # Mostrar soluciones
                    steps.append(f"📊 Resolver para {target}:")
                    steps.append(f"   {_format_result(lhs)} = {_format_result(rhs)}")
                    
                    if len(solutions) == 1:
                        steps.append(f"✓ {target} = {_format_result(solutions[0])}")
                        num = _try_numeric(solutions[0])
                        if num is not None:
                            steps.append(f"   ≈ {num}")
                        return "\n".join(steps), solutions[0]
                    else:
                        for i, sol in enumerate(solutions, 1):
                            steps.append(f"✓ Solución {i}: {target} = {_format_result(sol)}")
                            num = _try_numeric(sol)
                            if num is not None:
                                steps.append(f"   ≈ {num}")
                        return "\n".join(steps), solutions
                
                except Exception as e:
                    steps.append(f"✗ Error al resolver: {str(e)[:50]}")
                    return "\n".join(steps), None
                    
            except Exception as e:
                raise ValueError(f"Ecuación inválida: {str(e)[:50]}")

    # Expresión matemática simple
    try:
        expr = _parse_expression(text)
        steps.append(f"📊 {_format_result(expr)}")
        
        # Si no tiene símbolos, evaluar numéricamente
        if not expr.free_symbols:
            result = float(sp.N(expr))
            if result == int(result):
                result = int(result)
            steps.append(f"✓ = {result}")
            return "\n".join(steps), result
        
        # Si tiene símbolos, intentar simplificar
        simplified = simplify(expr)
        if simplified != expr:
            steps.append(f"✓ = {_format_result(simplified)}")
            return "\n".join(steps), simplified
        
        steps.append(f"✓ = {_format_result(expr)}")
        return "\n".join(steps), expr
        
    except Exception as e:
        raise ValueError(f"No se puede resolver: {str(e)[:60]}")



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
            ("Ecuación cúbica", "x^3 - 6x^2 + 11x - 6 = 0"),
            ("Sistema (múltiples vars)", "2x + y = 5"),
            ("Derivada simple", "deriv: x^3"),
            ("Derivada compleja", "deriv: sin(x)*cos(x) + e^x"),
            ("Integral", "integral: x^2 + 2x"),
            ("Integral trigonométrica", "integral: sin(x)*cos(x)"),
            ("Límite simple", "lim: (x^2 - 1)/(x - 1), 1"),
            ("Límite infinito", "lim: 1/x, 0"),
            ("Factorizar", "factor: x^2 - 9"),
            ("Factorizar complejo", "factor: x^3 - 8"),
            ("Expandir", "expand: (x + 3)(x - 2)(x + 1)"),
            ("Simplificar", "simplify: (x^2 - 1)/(x - 1)"),
            ("Fracciones parciales", "apart: (2x + 3)/(x^2 - 1)"),
            ("Media", "mean: 5,10,15,20,25"),
            ("Varianza", "var: 2,4,6,8,10"),
            ("Desv. Estándar", "std: 3,6,9,12,15"),
            ("Combinaciones", "comb: 10,3"),
            ("Permutaciones", "perm: 10,3"),
            ("Trigonometría", "sin(pi/6) + cos(pi/3)"),
            ("Logaritmos", "log(100, 10)"),
            ("Exponenciales", "e^2 + 2^8"),
            ("Raíces", "sqrt(16) + sqrt(25)"),
            ("Valor absoluto", "abs(-5) + abs(3)"),
        ]

        dialog = tk.Toplevel(self)
        dialog.title("Ejemplos de Problemas")
        dialog.geometry("600x550")
        dialog.configure(bg="#0b1120")

        ttk.Label(
            dialog,
            text="Selecciona un ejemplo o escribe tu propio problema",
            style="SubHeader.TLabel"
        ).pack(padx=12, pady=12)

        # Create scrollable frame
        canvas = tk.Canvas(dialog, bg="#0b1120", highlightthickness=0)
        canvas.pack(side="left", fill="both", expand=True, padx=12, pady=12)
        
        scrollbar = ttk.Scrollbar(dialog, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y", pady=12, padx=(0, 12))
        
        canvas.configure(yscrollcommand=scrollbar.set)
        
        frame = tk.Frame(canvas, bg="#0b1120")
        canvas.create_window((0, 0), window=frame, anchor="nw")

        for category, example in examples:
            btn = tk.Button(
                frame,
                text=f"► {category}\n   {example}",
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
                justify="left"
            )
            btn.pack(fill="x", pady=3)

        frame.update_idletasks()
        canvas.configure(scrollregion=canvas.bbox("all"))

    def _copy_example(self, example: str, dialog):
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", example)
        dialog.destroy()
        self.input_text.focus()


if __name__ == "__main__":
    app = CalculadoraGUI()
    app.mainloop()
