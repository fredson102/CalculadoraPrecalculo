import tkinter as tk
from tkinter import ttk, messagebox

from calculadora_completa import compute_statistics


def _float(value: str, field: str):
    try:
        return float(value)
    except ValueError:
        raise ValueError(f"{field} debe ser un número válido")


def _show_error(err: Exception):
    messagebox.showerror("Error", str(err))


class CalculadoraGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Calculadora PreCálculo")
        self.geometry("920x620")
        self.minsize(900, 580)

        self.configure(bg="#0f172a")
        style = ttk.Style(self)
        style.theme_use("clam")

        style.configure("TFrame", background="#0f172a")
        style.configure("TLabel", background="#0f172a", foreground="#e2e8f0", font=("Segoe UI", 10))
        style.configure("Header.TLabel", font=("Segoe UI", 18, "bold"), foreground="#38bdf8")
        style.configure("TButton", font=("Segoe UI", 10, "bold"))
        style.configure("TNotebook", background="#0f172a", borderwidth=0)
        style.configure("TNotebook.Tab", background="#1e293b", foreground="#e2e8f0", padding=(12, 6))
        style.map("TNotebook.Tab", background=[("selected", "#0ea5e9")])

        header = ttk.Frame(self)
        header.pack(fill="x", padx=16, pady=(12, 6))
        ttk.Label(header, text="Calculadora PreCálculo", style="Header.TLabel").pack(side="left")
        ttk.Label(header, text="Interfaz gráfica moderna", foreground="#94a3b8").pack(side="left", padx=12)

        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=16, pady=12)

        self._tab_algebra(notebook)
        self._tab_funciones(notebook)
        self._tab_trigonometria(notebook)
        self._tab_aplicaciones(notebook)
        self._tab_estadistica(notebook)

    def _result_box(self, parent):
        frame = ttk.Frame(parent)
        frame.grid(column=0, row=99, columnspan=6, sticky="nsew", pady=(14, 0))
        text = tk.Text(frame, height=8, bg="#0b1220", fg="#e2e8f0", insertbackground="#e2e8f0", wrap="word")
        text.pack(fill="both", expand=True)
        text.insert("end", "Resultados aparecerán aquí...\n")
        return text

    def _tab_algebra(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Álgebra")
        tab.columnconfigure(5, weight=1)

        ttk.Label(tab, text="Ecuación lineal: ax + b = c").grid(column=0, row=0, columnspan=6, sticky="w")
        a = ttk.Entry(tab, width=10)
        b = ttk.Entry(tab, width=10)
        c = ttk.Entry(tab, width=10)
        a.grid(column=0, row=1, padx=4, pady=4)
        b.grid(column=1, row=1, padx=4, pady=4)
        c.grid(column=2, row=1, padx=4, pady=4)
        result = self._result_box(tab)

        def solve_lineal():
            try:
                av = _float(a.get(), "a")
                bv = _float(b.get(), "b")
                cv = _float(c.get(), "c")
                if av == 0:
                    raise ValueError("a no puede ser 0")
                x = (cv - bv) / av
                result.delete("1.0", "end")
                result.insert("end", f"x = {x:.6f}\n")
            except Exception as e:
                _show_error(e)

        ttk.Button(tab, text="Resolver", command=solve_lineal).grid(column=3, row=1, padx=4, pady=4)

        ttk.Separator(tab, orient="horizontal").grid(column=0, row=2, columnspan=6, sticky="ew", pady=8)

        ttk.Label(tab, text="Ecuación cuadrática: ax² + bx + c = 0").grid(column=0, row=3, columnspan=6, sticky="w")
        a2 = ttk.Entry(tab, width=10)
        b2 = ttk.Entry(tab, width=10)
        c2 = ttk.Entry(tab, width=10)
        a2.grid(column=0, row=4, padx=4, pady=4)
        b2.grid(column=1, row=4, padx=4, pady=4)
        c2.grid(column=2, row=4, padx=4, pady=4)

        def solve_cuadratica():
            try:
                av = _float(a2.get(), "a")
                bv = _float(b2.get(), "b")
                cv = _float(c2.get(), "c")
                if av == 0:
                    raise ValueError("a no puede ser 0")
                disc = bv ** 2 - 4 * av * cv
                result.delete("1.0", "end")
                if disc > 0:
                    x1 = (-bv + disc ** 0.5) / (2 * av)
                    x2 = (-bv - disc ** 0.5) / (2 * av)
                    result.insert("end", f"x1 = {x1:.6f}\n")
                    result.insert("end", f"x2 = {x2:.6f}\n")
                elif disc == 0:
                    x = -bv / (2 * av)
                    result.insert("end", f"x = {x:.6f}\n")
                else:
                    real = -bv / (2 * av)
                    imag = (abs(disc) ** 0.5) / (2 * av)
                    result.insert("end", f"x1 = {real:.6f} + {imag:.6f}i\n")
                    result.insert("end", f"x2 = {real:.6f} - {imag:.6f}i\n")
            except Exception as e:
                _show_error(e)

        ttk.Button(tab, text="Resolver", command=solve_cuadratica).grid(column=3, row=4, padx=4, pady=4)

    def _tab_funciones(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Funciones")

        ttk.Label(tab, text="f(x) = a * b^(x-h) + k").grid(column=0, row=0, columnspan=6, sticky="w")
        a = ttk.Entry(tab, width=10)
        b = ttk.Entry(tab, width=10)
        h = ttk.Entry(tab, width=10)
        k = ttk.Entry(tab, width=10)
        x = ttk.Entry(tab, width=10)
        for i, w in enumerate([a, b, h, k, x]):
            w.grid(column=i, row=1, padx=4, pady=4)
        result = self._result_box(tab)

        def calc_exp():
            try:
                av = _float(a.get(), "a")
                bv = _float(b.get(), "b")
                hv = _float(h.get(), "h")
                kv = _float(k.get(), "k")
                xv = _float(x.get(), "x")
                if bv <= 0 or bv == 1:
                    raise ValueError("b debe ser > 0 y distinto de 1")
                y = av * (bv ** (xv - hv)) + kv
                result.delete("1.0", "end")
                result.insert("end", f"f({xv}) = {y:.6f}\n")
            except Exception as e:
                _show_error(e)

        ttk.Button(tab, text="Calcular", command=calc_exp).grid(column=5, row=1, padx=4, pady=4)

        ttk.Separator(tab, orient="horizontal").grid(column=0, row=2, columnspan=6, sticky="ew", pady=8)

        ttk.Label(tab, text="f(x) = a * log_b(x-h) + k").grid(column=0, row=3, columnspan=6, sticky="w")
        a2 = ttk.Entry(tab, width=10)
        b2 = ttk.Entry(tab, width=10)
        h2 = ttk.Entry(tab, width=10)
        k2 = ttk.Entry(tab, width=10)
        x2 = ttk.Entry(tab, width=10)
        for i, w in enumerate([a2, b2, h2, k2, x2]):
            w.grid(column=i, row=4, padx=4, pady=4)

        def calc_log():
            try:
                import math
                av = _float(a2.get(), "a")
                bv = _float(b2.get(), "b")
                hv = _float(h2.get(), "h")
                kv = _float(k2.get(), "k")
                xv = _float(x2.get(), "x")
                if bv <= 0 or bv == 1:
                    raise ValueError("b debe ser > 0 y distinto de 1")
                if xv - hv <= 0:
                    raise ValueError("x-h debe ser > 0")
                y = av * math.log(xv - hv, bv) + kv
                result.delete("1.0", "end")
                result.insert("end", f"f({xv}) = {y:.6f}\n")
            except Exception as e:
                _show_error(e)

        ttk.Button(tab, text="Calcular", command=calc_log).grid(column=5, row=4, padx=4, pady=4)

    def _tab_trigonometria(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Trigonometría")

        ttk.Label(tab, text="Ángulo (grados)").grid(column=0, row=0, sticky="w")
        angle = ttk.Entry(tab, width=12)
        angle.grid(column=1, row=0, padx=4, pady=4)
        result = self._result_box(tab)

        def calc_trig():
            try:
                import math
                ang = _float(angle.get(), "ángulo")
                r = math.radians(ang)
                result.delete("1.0", "end")
                result.insert("end", f"sin = {math.sin(r):.6f}\n")
                result.insert("end", f"cos = {math.cos(r):.6f}\n")
                result.insert("end", f"tan = {math.tan(r):.6f}\n")
            except Exception as e:
                _show_error(e)

        ttk.Button(tab, text="Calcular", command=calc_trig).grid(column=2, row=0, padx=4, pady=4)

    def _tab_aplicaciones(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Aplicaciones")

        ttk.Label(tab, text="Interés compuesto").grid(column=0, row=0, columnspan=5, sticky="w")
        p = ttk.Entry(tab, width=10)
        i = ttk.Entry(tab, width=10)
        t = ttk.Entry(tab, width=10)
        n = ttk.Entry(tab, width=10)
        for idx, w in enumerate([p, i, t, n]):
            w.grid(column=idx, row=1, padx=4, pady=4)
        result = self._result_box(tab)

        def calc_interes():
            try:
                pv = _float(p.get(), "P")
                iv = _float(i.get(), "i")
                tv = _float(t.get(), "t")
                nv = _float(n.get(), "n")
                if nv <= 0:
                    raise ValueError("n debe ser > 0")
                a = pv * (1 + iv / nv) ** (nv * tv)
                result.delete("1.0", "end")
                result.insert("end", f"Monto final A = {a:.2f}\n")
                result.insert("end", f"Interés = {a - pv:.2f}\n")
            except Exception as e:
                _show_error(e)

        ttk.Button(tab, text="Calcular", command=calc_interes).grid(column=4, row=1, padx=4, pady=4)

    def _tab_estadistica(self, notebook):
        tab = ttk.Frame(notebook)
        notebook.add(tab, text="Estadística")

        ttk.Label(tab, text="Datos (separados por comas)").grid(column=0, row=0, sticky="w")
        data = ttk.Entry(tab, width=60)
        data.grid(column=0, row=1, columnspan=4, padx=4, pady=4, sticky="ew")
        result = self._result_box(tab)

        def calc_stats():
            try:
                values = [float(x.strip()) for x in data.get().split(',') if x.strip()]
                stats = compute_statistics(values)
                if not stats:
                    raise ValueError("No hay datos válidos")
                result.delete("1.0", "end")
                result.insert("end", f"n = {stats['n']}\n")
                result.insert("end", f"Media = {stats['mean']:.6f}\n")
                result.insert("end", f"Varianza (p) = {stats['var_p']:.6f}\n")
                result.insert("end", f"Desv. (p) = {stats['sd_p']:.6f}\n")
                result.insert("end", f"Q1 = {stats['q1']:.6f}, Q2 = {stats['q2']:.6f}, Q3 = {stats['q3']:.6f}\n")
            except Exception as e:
                _show_error(e)

        ttk.Button(tab, text="Calcular", command=calc_stats).grid(column=0, row=2, padx=4, pady=4, sticky="w")


def main():
    app = CalculadoraGUI()
    app.mainloop()


if __name__ == "__main__":
    main()
