"""
Calculadora Matemática Pro - GUI con pasos detallados tipo Mathway/PhotoMath
"""
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import sys
import os

# Importar el solver avanzado
from advanced_solver import DetailedSolver


class CalculadoraGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.solver = DetailedSolver()
        self.title("📐 Calculadora Matemática Pro - Soluciones Paso a Paso")
        self.geometry("1400x800")
        self.minsize(1200, 700)

        # Configurar colores
        self.bg_dark = "#0f172a"
        self.bg_darker = "#0b1120"
        self.text_light = "#e2e8f0"
        self.accent_blue = "#38bdf8"
        self.accent_green = "#34d399"
        self.accent_purple = "#a78bfa"
        
        self.configure(bg=self.bg_darker)
        
        # Crear estilos
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TFrame", background=self.bg_darker)
        style.configure("TLabel", background=self.bg_darker, foreground=self.text_light)
        
        self._create_ui()
    
    def _create_ui(self):
        """Crea la interfaz de usuario"""
        # Header profesional
        header = tk.Frame(self, bg="#1e293b")
        header.pack(fill="x", padx=0, pady=0, ipady=20)
        
        title_frame = tk.Frame(header, bg="#1e293b")
        title_frame.pack(fill="x", padx=30)
        
        tk.Label(title_frame, text="📐 CALCULADORA MATEMÁTICA PRO", 
                font=("Segoe UI", 26, "bold"), fg=self.accent_blue, bg="#1e293b").pack(anchor="w")
        tk.Label(title_frame, text="Soluciones paso a paso como Mathway & PhotoMath",
                font=("Segoe UI", 12), fg="#94a3b8", bg="#1e293b").pack(anchor="w", pady=(5,0))
        
        # Separador
        ttk.Separator(self, orient="horizontal").pack(fill="x")
        
        # Contenedor principal
        main = ttk.Frame(self)
        main.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Panel izquierdo - ENTRADA
        left_panel = tk.Frame(main, bg=self.bg_dark, relief="flat", bd=0)
        left_panel.pack(side="left", fill="both", padx=(0, 10), ipadx=20, ipady=20)
        
        tk.Label(left_panel, text="ESCRIBE TU PROBLEMA", font=("Segoe UI", 14, "bold"),
                fg=self.accent_blue, bg=self.bg_dark).pack(anchor="w", pady=(0, 10))
        
        tk.Label(left_panel, text="Ejemplos: 2x+5=17  |  deriv: x^2  |  x^2-5x+6=0",
                font=("Segoe UI", 9), fg="#94a3b8", bg=self.bg_dark).pack(anchor="w", pady=(0, 10))
        
        # Área de entrada
        self.input_text = tk.Text(
            left_panel, height=12, width=50,
            font=("Fira Code", 12), bg="#0b1220", fg=self.accent_green,
            insertbackground=self.accent_green, wrap="word", padx=12, pady=12
        )
        self.input_text.pack(fill="both", expand=True, pady=(0, 15))
        self.input_text.bind("<Control-Return>", lambda e: self.on_solve())
        
        # Botones
        btn_frame = tk.Frame(left_panel, bg=self.bg_dark)
        btn_frame.pack(fill="x", pady=(0, 10))
        
        self._make_button(btn_frame, "🔍 RESOLVER", self.on_solve, self.accent_blue).pack(side="left", padx=5)
        self._make_button(btn_frame, "🗑️ LIMPIAR", self.on_clear, "#64748b").pack(side="left", padx=5)
        self._make_button(btn_frame, "📚 EJEMPLOS", self.on_examples, self.accent_purple).pack(side="left", padx=5)
        
        # Panel derecho - SOLUCIÓN
        right_panel = tk.Frame(main, bg=self.bg_dark, relief="flat", bd=0)
        right_panel.pack(side="right", fill="both", expand=True, padx=(10, 0), ipadx=20, ipady=20)
        
        tk.Label(right_panel, text="SOLUCIÓN PASO A PASO", font=("Segoe UI", 14, "bold"),
                fg=self.accent_green, bg=self.bg_dark).pack(anchor="w", pady=(0, 10))
        
        # Área de salida con scroll
        self.output_text = scrolledtext.ScrolledText(
            right_panel, font=("Fira Code", 11), bg="#0b1220", fg=self.text_light,
            wrap="word", padx=15, pady=15, relief="flat", bd=0
        )
        self.output_text.pack(fill="both", expand=True)
        
        # Configurar tags para formateo
        self.output_text.tag_configure("title", foreground=self.accent_blue, font=("Fira Code", 12, "bold"))
        self.output_text.tag_configure("step", foreground="#cbd5e1", font=("Fira Code", 11))
        self.output_text.tag_configure("equation", foreground=self.accent_green, font=("Fira Code", 12, "bold"))
        self.output_text.tag_configure("info", foreground="#94a3b8", font=("Fira Code", 10))
        self.output_text.tag_configure("separator", foreground="#334155")
        
        # Footer
        footer = tk.Frame(self, bg="#1e293b", height=40)
        footer.pack(fill="x", side="bottom")
        footer.pack_propagate(False)
        
        footer_text = "Ctrl+Enter = Resolver  |  Soporta: ecuaciones | derivadas | integrales | factorización | estadística y más"
        tk.Label(footer, text=footer_text, font=("Segoe UI", 9),
                fg="#94a3b8", bg="#1e293b").pack(pady=10)
    
    def _make_button(self, parent, text, command, color):
        """Crea un botón estilizado"""
        btn = tk.Button(
            parent, text=text, command=command, bg=color, fg="#0b1120" if color != "#64748b" else self.text_light,
            font=("Segoe UI", 10, "bold"), activebackground=color,
            padx=15, pady=8, bd=0, relief="flat", cursor="hand2"
        )
        return btn
    
    def on_solve(self):
        """Resuelve el problema"""
        problem = self.input_text.get("1.0", "end").strip()
        if not problem:
            messagebox.showwarning("Aviso", "Escribe un problema para resolver")
            return
        
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        
        try:
            # Limpiar caracteres problemáticos
            problem_clean = problem.replace("°", "")  # Eliminar símbolo de grado
            problem_clean = problem_clean.replace("×", "*")  # Reemplazar × por *
            problem_clean = problem_clean.replace("÷", "/")  # Reemplazar ÷ por /
            
            steps, result = self.solver.solve(problem_clean)
            
            # Mostrar pasos con formato
            for step in steps:
                if step.startswith("="):
                    self.output_text.insert("end", step + "\n", "separator")
                elif ":" in step and not step.strip().startswith("Paso"):
                    self.output_text.insert("end", step + "\n", "equation")
                else:
                    self.output_text.insert("end", step + "\n", "step")
            
            # Mostrar resultado final
            self.output_text.insert("end", "\n" + "="*50 + "\n", "separator")
            self.output_text.insert("end", f"RESULTADO FINAL: {result}\n", "title")
            self.output_text.insert("end", "="*50 + "\n", "separator")
            
        except ValueError as e:
            self.output_text.insert("end", f"❌ Error de formato: {str(e)}\n\n", "info")
            self.output_text.insert("end", "Verifica que el problema este bien escrito.\n", "info")
            self.output_text.insert("end", "Ejemplos validos:\n", "info")
            self.output_text.insert("end", "  - 2x + 5 = 17\n", "step")
            self.output_text.insert("end", "  - x^2 - 5x + 6 = 0\n", "step")
            self.output_text.insert("end", "  - deriv: x^3 + 2*x^2\n", "step")
        except Exception as e:
            error_msg = str(e)
            self.output_text.insert("end", f"❌ Error: {error_msg}\n\n", "info")
            self.output_text.insert("end", "Consejos:\n", "info")
            self.output_text.insert("end", "  - Usa * para multiplicacion (2*x en vez de 2x)\n", "step")
            self.output_text.insert("end", "  - Usa ^ para exponentes (x^2 en vez de x²)\n", "step")
            self.output_text.insert("end", "  - Evita simbolos especiales\n", "step")
            self.output_text.insert("end", "  - Haz clic en EJEMPLOS para ver formatos validos\n", "step")
        
        self.output_text.config(state="disabled")
        self.output_text.see("1.0")
    
    def on_clear(self):
        """Limpia entrada y salida"""
        self.input_text.delete("1.0", "end")
        self.output_text.config(state="normal")
        self.output_text.delete("1.0", "end")
        self.output_text.config(state="disabled")
    
    def on_examples(self):
        """Muestra menú de ejemplos"""
        examples_window = tk.Toplevel(self)
        examples_window.title("📚 Ejemplos de Problemas")
        examples_window.geometry("600x700")
        examples_window.configure(bg=self.bg_darker)
        
        tk.Label(examples_window, text="EJEMPLOS DE PROBLEMAS", 
                font=("Segoe UI", 16, "bold"), fg=self.accent_blue, bg=self.bg_darker).pack(pady=20)
        
        # Crear frame con scroll
        canvas = tk.Canvas(examples_window, bg=self.bg_darker, highlightthickness=0)
        scrollbar = ttk.Scrollbar(examples_window, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_darker)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Ejemplos organizados por categoría
        examples = {
            "📐 ECUACIONES": [
                ("Ecuación lineal simple", "2x + 5 = 17"),
                ("Ecuación cuadrática", "x^2 - 5x + 6 = 0"),
                ("Ecuación con fracciones", "x/2 + 3 = 7"),
                ("Ecuación compleja", "3x^2 + 2x - 1 = 0"),
            ],
            "📊 CÁLCULO": [
                ("Derivada polinomial", "deriv: x^3 + 2*x^2 - 5*x + 1"),
                ("Derivada trigonométrica", "deriv: sin(x)*cos(x)"),
                ("Integral simple", "integral: x^2 + 3*x"),
                ("Límite", "limit: (x^2 - 1)/(x - 1), x->1"),
            ],
            "🔢 ÁLGEBRA": [
                ("Factorización", "factor: x^2 - 9"),
                ("Expandir expresión", "expand: (x + 2)*(x - 3)"),
                ("Simplificar", "simplify: (x^2 - 4)/(x - 2)"),
            ],
            "📈 ESTADÍSTICA": [
                ("Media", "mean: 5,10,15,20,25"),
                ("Varianza", "var: 2,4,6,8,10"),
                ("Desviación estándar", "stddev: 1,2,3,4,5"),
            ],
            "🎯 EXPRESIONES": [
                ("Evaluar expresión", "2*pi + sqrt(16)"),
                ("Trigonometría", "sin(pi/2) + cos(0)"),
            ]
        }
        
        for category, items in examples.items():
            # Categoría
            tk.Label(scrollable_frame, text=category, 
                    font=("Segoe UI", 12, "bold"), fg=self.accent_green, bg=self.bg_darker).pack(anchor="w", padx=20, pady=(15, 5))
            
            # Items
            for name, example in items:
                btn_container = tk.Frame(scrollable_frame, bg=self.bg_darker)
                btn_container.pack(fill="x", padx=30, pady=2)
                
                btn = tk.Button(
                    btn_container, text=f"  {name}  →  {example}", anchor="w",
                    font=("Fira Code", 9), bg="#1e293b", fg=self.text_light,
                    activebackground=self.accent_blue, activeforeground="#0b1120",
                    bd=0, relief="flat", cursor="hand2",
                    command=lambda ex=example: self._use_example(ex, examples_window)
                )
                btn.pack(fill="x", ipady=8)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
    
    def _use_example(self, example, window):
        """Usa un ejemplo y lo resuelve automáticamente"""
        self.input_text.delete("1.0", "end")
        self.input_text.insert("1.0", example)
        window.destroy()
        self.on_solve()


if __name__ == "__main__":
    app = CalculadoraGUI()
    app.mainloop()
