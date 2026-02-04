"""
Solver avanzado con pasos detallados tipo Mathway/PhotoMath
"""
import sympy as sp
from sympy import (
    Symbol, symbols, solve, diff, integrate, limit, summation,
    expand, factor, simplify, apart, together, cancel, gcd, lcm,
    sin, cos, tan, asin, acos, atan, sinh, cosh, tanh,
    exp, log, sqrt, Abs, Rational, oo, I, pi, E,
    roots, degree, Poly, fraction, solve_univariate_inequality,
    S, nsimplify, collect, apart, series, Sum, Product,
    binomial, factorial, floor, ceiling, atan2
)
from sympy.parsing.sympy_parser import (
    parse_expr,
    standard_transformations,
    implicit_multiplication_application,
    convert_xor
)
import re
from typing import Tuple, List, Optional, Any

TRANSFORMS = (standard_transformations + (implicit_multiplication_application, convert_xor))


class DetailedSolver:
    """Resolvedor con pasos detallados tipo Mathway"""
    
    def __init__(self):
        self.steps = []
        self.x = Symbol('x')
        
    def _add_step(self, description: str, math_expr: str = "", is_title=False):
        """Añade un paso a la solución"""
        if is_title:
            self.steps.append(f"\n{'='*60}")
            self.steps.append(f"  {description}")
            self.steps.append(f"{'='*60}\n")
        else:
            self.steps.append(f"{description}")
            if math_expr:
                self.steps.append(f"  {math_expr}")
    
    def _format_expr(self, expr):
        """Formatea una expresión para visualización"""
        try:
            return sp.pretty(expr, use_unicode=False)
        except:
            return str(expr)
    
    def _parse_expr(self, text: str):
        """Parsea expresión matemática"""
        text = text.replace('π', 'pi').replace('∞', 'oo').replace('√', 'sqrt')
        return parse_expr(text, transformations=TRANSFORMS, evaluate=False, local_dict={
            'sin': sin, 'cos': cos, 'tan': tan,
            'asin': asin, 'acos': acos, 'atan': atan,
            'sinh': sinh, 'cosh': cosh, 'tanh': tanh,
            'exp': exp, 'log': log, 'sqrt': sqrt, 'abs': Abs,
            'pi': pi, 'e': E, 'E': E, 'I': I, 'oo': oo,
            'factorial': factorial, 'binomial': binomial,
            'floor': floor, 'ceiling': ceiling,
        })
    
    # ============ ECUACIONES LINEALES ============
    def solve_linear_equation(self, text: str) -> Tuple[List[str], Any]:
        """Resuelve ecuaciones lineales ax + b = c paso por paso"""
        self.steps = []
        parts = text.split('=')
        if len(parts) != 2:
            raise ValueError("Formato inválido para ecuación")
        
        left_str, right_str = parts
        left = self._parse_expr(left_str.strip())
        right = self._parse_expr(right_str.strip())
        
        self._add_step("RESOLVER ECUACIÓN LINEAL", is_title=True)
        self._add_step(f"Ecuación original:", f"{self._format_expr(left)} = {self._format_expr(right)}")
        
        eq = sp.Eq(left, right)
        self._add_step("\nPaso 1: Mover todos los términos con variable al lado izquierdo")
        rearranged = sp.Eq(left - right, 0)
        self._add_step(f"", f"{self._format_expr(left - right)} = 0")
        
        solutions = solve(eq, self.x)
        if solutions:
            sol = solutions[0]
            self._add_step(f"\nPaso 2: Despejar la variable")
            self._add_step(f"", f"x = {self._format_expr(sol)}")
            
            # Verificación
            verification = left.subs(self.x, sol)
            self._add_step(f"\nPaso 3: Verificación")
            self._add_step(f"Sustituir x = {self._format_expr(sol)} en la ecuación original:", 
                         f"{self._format_expr(verification)} = {self._format_expr(right)}")
            
            return self.steps, sol
        return self.steps, None
    
    # ============ ECUACIONES CUADRÁTICAS ============
    def solve_quadratic_equation(self, text: str) -> Tuple[List[str], Any]:
        """Resuelve ecuaciones cuadrticas ax^2 + bx + c = 0"""
        self.steps = []
        parts = text.split('=')
        left = self._parse_expr(parts[0].strip())
        right = self._parse_expr(parts[1].strip()) if len(parts) > 1 else 0
        
        self._add_step("RESOLVER ECUACIÓN CUADRÁTICA", is_title=True)
        self._add_step(f"Ecuación:", f"{self._format_expr(left)} = {self._format_expr(right)}")
        
        eq = sp.Eq(left, right)
        
        # Estándar form
        standard = left - right
        self._add_step(f"\nPaso 1: Llevar a forma estandar ax^2 + bx + c = 0")
        self._add_step(f"", f"{self._format_expr(standard)} = 0")
        
        # Extraer coeficientes
        poly = sp.Poly(standard, self.x)
        coeffs = poly.all_coeffs()
        
        if len(coeffs) >= 3:
            a, b, c = coeffs[0], coeffs[1], coeffs[2]
            self._add_step(f"\nPaso 2: Identificar coeficientes")
            self._add_step(f"a = {a}, b = {b}, c = {c}")
            
            # Discriminante
            discriminant = b**2 - 4*a*c
            self._add_step(f"\nPaso 3: Calcular discriminante (Delta = b^2 - 4ac)")
            self._add_step(f"", f"Delta = ({b})^2 - 4({a})({c})")
            self._add_step(f"Delta = {sp.expand(discriminant)}")
            
            # Fórmula cuadrática
            self._add_step(f"\nPaso 4: Aplicar fórmula cuadrática")
            self._add_step(f"x = (-b +/- sqrt(Delta)) / (2a)")
            self._add_step(f"x = (-({b}) +/- sqrt({discriminant})) / (2*{a})")
        
        solutions = solve(eq, self.x)
        self._add_step(f"\nPaso 5: Soluciones")
        for i, sol in enumerate(solutions, 1):
            numeric = complex(sol.evalf()) if sol.has(I) else float(sol.evalf())
            self._add_step(f"x_{i} = {self._format_expr(sol)}")
            if isinstance(numeric, complex):
                self._add_step(f"    ~ {numeric:.6f}")
            else:
                self._add_step(f"    ~ {numeric:.6f}")
        
        return self.steps, solutions
    
    # ============ DERIVADAS ============
    def solve_derivative(self, text: str) -> Tuple[List[str], Any]:
        """Calcula derivada con pasos detallados"""
        self.steps = []
        expr_text = text.split(':', 1)[1].strip() if ':' in text else text
        expr = self._parse_expr(expr_text)
        
        self._add_step("CALCULAR DERIVADA", is_title=True)
        self._add_step(f"Función original:", f"f(x) = {self._format_expr(expr)}")
        
        # Expandir si es necesario
        if isinstance(expr, sp.Mul) or isinstance(expr, sp.Add):
            expanded = expand(expr)
            if expanded != expr:
                self._add_step(f"\nPaso 1: Expandir la función")
                self._add_step(f"f(x) = {self._format_expr(expanded)}")
                expr = expanded
        
        self._add_step(f"\nPaso 2: Aplicar reglas de derivación")
        
        # Desglosar por términos
        if isinstance(expr, sp.Add):
            self._add_step(f"Derivar término por término:")
            for term in expr.as_ordered_terms():
                term_deriv = diff(term, self.x)
                self._add_step(f"  • d/dx({self._format_expr(term)}) = {self._format_expr(term_deriv)}")
        
        derivative = diff(expr, self.x)
        simplified = simplify(derivative)
        
        self._add_step(f"\nPaso 3: Derivada")
        self._add_step(f"f'(x) = {self._format_expr(derivative)}")
        
        if simplified != derivative:
            self._add_step(f"\nPaso 4: Simplificar")
            self._add_step(f"f'(x) = {self._format_expr(simplified)}")
            derivative = simplified
        
        return self.steps, derivative
    
    # ============ INTEGRALES ============
    def solve_integral(self, text: str) -> Tuple[List[str], Any]:
        """Calcula integral con pasos detallados"""
        self.steps = []
        expr_text = text.split(':', 1)[1].strip() if ':' in text else text
        expr = self._parse_expr(expr_text)
        
        self._add_step("CALCULAR INTEGRAL INDEFINIDA", is_title=True)
        self._add_step(f"Integrando:", f"∫ {self._format_expr(expr)} dx")
        
        self._add_step(f"\nPaso 1: Identificar el tipo de integral")
        
        # Determinar método
        if expr == 1:
            method = "Integral simple"
        elif expr.is_polynomial():
            method = "Integral polinomica - aplicar regla de potencia"
        else:
            method = "Integral general"
        
        self._add_step(f"Metodo: {method}")
        
        try:
            integral = integrate(expr, self.x)
            
            self._add_step(f"\nPaso 2: Integrar")
            self._add_step(f"Integral de {self._format_expr(expr)} = {self._format_expr(integral)}")
            
            self._add_step(f"\nPaso 3: Resultado final (integral indefinida)")
            self._add_step(f"Resultado: {self._format_expr(integral)} + C")
            self._add_step(f"\nNota: C es la constante arbitraria de integracion")
            
            return self.steps, integral
        except:
            self._add_step(f"\nNo se puede integrar analiticamente")
            return self.steps, None
    
    # ============ FACTORIZACIÓN ============
    def solve_factorization(self, text: str) -> Tuple[List[str], Any]:
        """Factoriza expresiones paso por paso"""
        self.steps = []
        expr_text = text.split(':', 1)[1].strip() if ':' in text else text
        expr = self._parse_expr(expr_text)
        
        self._add_step("FACTORIZAR EXPRESIÓN", is_title=True)
        self._add_step(f"Expresión original:", f"{self._format_expr(expr)}")
        
        # Intentar encontrar MCD
        if isinstance(expr, sp.Add):
            self._add_step(f"\nPaso 1: Identificar términos")
            for term in expr.as_ordered_terms():
                self._add_step(f"  • {self._format_expr(term)}")
            
            # GCD de coeficientes
            coeffs = [sp.Integer(c) for term in expr.as_ordered_terms() 
                     for c in term.as_coefficients_dict().values() if c.is_number]
            if coeffs:
                common = sp.gcd(*coeffs) if len(coeffs) > 1 else coeffs[0]
                if common != 1:
                    self._add_step(f"\nPaso 2: Factor común = {common}")
        
        factored = factor(expr)
        self._add_step(f"\nPaso 3: Factorizar")
        self._add_step(f"{self._format_expr(expr)} = {self._format_expr(factored)}")
        
        # Verificar
        self._add_step(f"\nPaso 4: Verificación (expandir el resultado)")
        expanded = expand(factored)
        self._add_step(f"{self._format_expr(expanded)} ✓")
        
        return self.steps, factored
    
    # ============ EXPANSIÓN ============
    def solve_expansion(self, text: str) -> Tuple[List[str], Any]:
        """Expande expresiones paso por paso"""
        self.steps = []
        expr_text = text.split(':', 1)[1].strip() if ':' in text else text
        expr = self._parse_expr(expr_text)
        
        self._add_step("EXPANDIR EXPRESIÓN", is_title=True)
        self._add_step(f"Expresión:", f"{self._format_expr(expr)}")
        
        if isinstance(expr, sp.Mul):
            self._add_step(f"\nPaso 1: Distribuir multiplicación")
            factors = expr.as_ordered_factors()
            self._add_step(f"Factores: {', '.join(str(f) for f in factors)}")
        
        expanded = expand(expr)
        self._add_step(f"\nPaso 2: Aplicar distribución")
        self._add_step(f"Resultado: {self._format_expr(expanded)}")
        
        return self.steps, expanded
    
    # ============ SIMPLIFICACIÓN ============
    def solve_simplification(self, text: str) -> Tuple[List[str], Any]:
        """Simplifica expresiones paso por paso"""
        self.steps = []
        expr_text = text.split(':', 1)[1].strip() if ':' in text else text
        expr = self._parse_expr(expr_text)
        
        self._add_step("SIMPLIFICAR EXPRESIÓN", is_title=True)
        self._add_step(f"Expresión original:", f"{self._format_expr(expr)}")
        
        # Cancelar denominadores comunes
        if isinstance(expr, sp.Rational) or (isinstance(expr, sp.Mul) and any(isinstance(a, sp.Pow) for a in expr.as_ordered_factors())):
            self._add_step(f"\nPaso 1: Cancelar factores comunes")
        
        simplified = simplify(expr)
        
        self._add_step(f"\nPaso 2: Expresión simplificada")
        self._add_step(f"{self._format_expr(simplified)}")
        
        if not simplified.free_symbols:
            numeric = float(simplified.evalf())
            self._add_step(f"\nValor numérico: {numeric:.10g}")
        
        return self.steps, simplified
    
    # ============ LÍMITES ============
    def solve_limit(self, text: str) -> Tuple[List[str], Any]:
        """Calcula límites paso por paso"""
        self.steps = []
        try:
            expr_text, point = text.split(':', 1)[1].rsplit(',', 1)
        except:
            raise ValueError("Formato: lim: expr, punto")
        
        expr = self._parse_expr(expr_text.strip())
        point_val = float(point.strip()) if point.strip() != 'oo' else oo
        
        self._add_step("CALCULAR LIMITE", is_title=True)
        self._add_step(f"Limite:", f"lim (x→{point.strip()}) [{self._format_expr(expr)}]")
        
        self._add_step(f"\nPaso 1: Evaluar la funcion en x = {point.strip()}")
        try:
            eval_at_point = expr.subs(self.x, point_val)
            self._add_step(f"Sustitucion directa: {self._format_expr(eval_at_point)}")
        except:
            self._add_step(f"Sustitucion directa no posible (indeterminacion)")
        
        self._add_step(f"\nPaso 2: Calcular el limite")
        lim = limit(expr, self.x, point_val)
        self._add_step(f"lim (x→{point.strip()}) {self._format_expr(expr)} = {self._format_expr(lim)}")
        
        return self.steps, lim
    
    # ============ ESTADÍSTICA ============
    def solve_statistics(self, stat_type: str, data_str: str) -> Tuple[List[str], Any]:
        """Calcula estadísticas paso por paso"""
        self.steps = []
        try:
            data = [float(x.strip()) for x in data_str.split(',')]
        except:
            raise ValueError("Datos inválidos")
        
        if stat_type == 'mean':
            self._add_step("CALCULAR MEDIA (PROMEDIO)", is_title=True)
            self._add_step(f"Datos:", f"{data}")
            self._add_step(f"\nPaso 1: Formula de la media")
            self._add_step(f"mu = (Suma x) / n")
            
            total = sum(data)
            n = len(data)
            self._add_step(f"\nPaso 2: Sumar todos los valores")
            self._add_step(f"Suma x = {' + '.join(map(str, data))} = {total}")
            
            self._add_step(f"\nPaso 3: Dividir entre cantidad de datos")
            self._add_step(f"mu = {total} / {n} = {total/n:.6g}")
            
            return self.steps, total/n
        
        elif stat_type == 'variance':
            self._add_step("CALCULAR VARIANZA", is_title=True)
            self._add_step(f"Datos:", f"{data}")
            
            mean_val = sum(data) / len(data)
            self._add_step(f"\nPaso 1: Calcular la media")
            self._add_step(f"mu = {mean_val:.6g}")
            
            self._add_step(f"\nPaso 2: Calcular desviaciones de la media")
            deviations = [(x - mean_val) for x in data]
            for i, (x, dev) in enumerate(zip(data, deviations)):
                self._add_step(f"x_{i+1} - mu = {x} - {mean_val:.4f} = {dev:.6g}")
            
            self._add_step(f"\nPaso 3: Elevar desviaciones al cuadrado")
            squared_devs = [dev**2 for dev in deviations]
            for i, (dev, sq) in enumerate(zip(deviations, squared_devs)):
                self._add_step(f"({dev:.6g})^2 = {sq:.6g}")
            
            variance = sum(squared_devs) / len(data)
            self._add_step(f"\nPaso 4: Calcular varianza")
            self._add_step(f"sigma^2 = (Suma(x-mu)^2) / n = {sum(squared_devs):.6g} / {len(data)} = {variance:.6g}")
            
            return self.steps, variance
        
        elif stat_type == 'stddev':
            self._add_step("CALCULAR DESVIACION ESTANDAR", is_title=True)
            self._add_step(f"Datos:", f"{data}")
            
            mean_val = sum(data) / len(data)
            variance = sum((x - mean_val)**2 for x in data) / len(data)
            stddev = variance ** 0.5
            
            self._add_step(f"\nPaso 1: Calcular varianza")
            self._add_step(f"sigma^2 = {variance:.6g}")
            
            self._add_step(f"\nPaso 2: Calcular desviacion estandar")
            self._add_step(f"sigma = raiz(sigma^2) = raiz({variance:.6g}) = {stddev:.6g}")
            
            return self.steps, stddev
        
        return self.steps, None
    
    # ============ MÉTODO PRINCIPAL ============
    def solve(self, problem: str) -> Tuple[List[str], Any]:
        """Método principal para resolver cualquier problema"""
        text = problem.strip()
        lowered = text.lower()
        
        # Detectar tipo de problema
        if lowered.startswith(('deriv:', 'd:', 'derivative:')):
            return self.solve_derivative(text)
        
        elif lowered.startswith(('integral:', '∫:', 'int:')):
            return self.solve_integral(text)
        
        elif lowered.startswith(('lim:', 'limit:')):
            return self.solve_limit(text)
        
        elif lowered.startswith('factor:'):
            return self.solve_factorization(text)
        
        elif lowered.startswith('expand:'):
            return self.solve_expansion(text)
        
        elif lowered.startswith(('simplify:', 'simpl:')):
            return self.solve_simplification(text)
        
        elif lowered.startswith(('mean:', 'μ:', 'media:')):
            data = text.split(':', 1)[1].strip()
            return self.solve_statistics('mean', data)
        
        elif lowered.startswith(('var:', 'variance:', 'σ²:')):
            data = text.split(':', 1)[1].strip()
            return self.solve_statistics('variance', data)
        
        elif lowered.startswith(('std:', 'stdev:', 'σ:')):
            data = text.split(':', 1)[1].strip()
            return self.solve_statistics('stddev', data)
        
        elif '=' in text:
            # Detectar tipo de ecuación
            expr_str = text.split('=')[0].strip()
            expr = self._parse_expr(expr_str)
            
            # Contar grado
            try:
                poly = sp.Poly(expr - self._parse_expr(text.split('=')[1].strip()), self.x)
                deg = degree(poly, self.x)
                
                if deg == 1:
                    return self.solve_linear_equation(text)
                elif deg == 2:
                    return self.solve_quadratic_equation(text)
            except:
                pass
            
            # Ecuación general
            return self.solve_linear_equation(text)
        
        # Expresión simple
        self.steps = []
        expr = self._parse_expr(text)
        self._add_step("EVALUAR EXPRESIÓN", is_title=True)
        self._add_step(f"Expresión:", f"{self._format_expr(expr)}")
        
        if not expr.free_symbols:
            result = float(expr.evalf())
            self._add_step(f"\nResultado:", f"{result:.10g}")
            return self.steps, result
        
        return self.steps, expr


# Crear instancia global
solver = DetailedSolver()
