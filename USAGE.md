# Calculadora PreCálculo Pro - Guía de Uso

## Problemas Soportados

### 🔢 Ecuaciones Algebraicas
```
2x + 5 = 17                    # Ecuación lineal
x^2 - 5x + 6 = 0              # Ecuación cuadrática
x^3 - 6x^2 + 11x - 6 = 0      # Ecuación cúbica
2x + y = 5                     # Variables múltiples
```

### 📈 Cálculo Diferencial
```
deriv: x^3                      # Derivada simple
deriv: sin(x)*cos(x) + e^x      # Derivada compleja
d: x^2 + 2x                     # Alias corto
```

### ∫ Cálculo Integral
```
integral: x^2 + 2x              # Integral simple
integral: sin(x)*cos(x)         # Integral trigonométrica
∫: e^x                          # Símbolo integral
```

### 📊 Límites
```
lim: (x^2 - 1)/(x - 1), 1       # Límite finito
lim: 1/x, 0                     # Límite infinito
limit: sin(x)/x, 0              # Formato alternativo
```

### 🧮 Álgebra Simbólica
```
factor: x^2 - 9                 # Factorizar
expand: (x + 3)(x - 2)(x + 1)   # Expandir
simplify: (x^2 - 1)/(x - 1)     # Simplificar
apart: (2x + 3)/(x^2 - 1)       # Fracciones parciales
```

### 📊 Estadística
```
mean: 5,10,15,20,25             # Media/Promedio
var: 2,4,6,8,10                 # Varianza
std: 3,6,9,12,15                # Desviación estándar
μ: 1,2,3,4,5                    # Alias para media
σ²: 1,2,3                       # Alias para varianza
σ: 1,2,3                        # Alias para desv. estándar
```

### 🎯 Combinatoria
```
comb: 10,3                       # Combinaciones C(n,r)
perm: 10,3                       # Permutaciones P(n,r)
C(5,2)                          # Formato alternativo
P(5,2)                          # Formato alternativo
```

### 🔢 Expresiones Matemáticas Simples
```
sin(pi/6) + cos(pi/3)           # Trigonometría
log(100, 10)                    # Logaritmos
e^2 + 2^8                       # Exponenciales
sqrt(16) + sqrt(25)             # Raíces
abs(-5) + abs(3)                # Valor absoluto
```

## 🎨 Notación Soportada

### Símbolos Especiales
- `π` → pi (número π)
- `e` o `E` → número de Euler
- `∞` → infinito (oo)
- `√` → raíz cuadrada (sqrt)
- `°` → grados a radianes

### Funciones Trigonométricas
- `sin, cos, tan` - Trigonométricas básicas
- `asin, acos, atan` - Trigonométricas inversas
- `sinh, cosh, tanh` - Trigonométricas hiperbólicas

### Funciones Especiales
- `sqrt(x)` - Raíz cuadrada
- `abs(x)` - Valor absoluto
- `log(x, base)` - Logaritmo con base
- `exp(x)` - e^x
- `factorial(n)` - n!
- `binomial(n,k)` - C(n,k)

## 💡 Ejemplos

### Resolver una ecuación cuadrática
**Entrada:** `x^2 - 5x + 6 = 0`
**Salida:**
```
Resolver para x:
   x^2 - 5x + 6 = 0
✓ Solución 1: x = 2
✓ Solución 2: x = 3
```

### Encontrar una derivada
**Entrada:** `deriv: x^3 + 2x^2`
**Salida:**
```
Función: x^3 + 2x^2
f'(x) = 3*x^2 + 4*x
```

### Calcular estadística
**Entrada:** `mean: 5,10,15,20,25`
**Salida:**
```
Datos: [5, 10, 15, 20, 25]
μ = (Σx) / n = 75 / 5
✓ μ = 15
```

## ⌨️ Atajos

- **Ctrl+Enter** - Resuelve el problema (igual que botón Resolver)
- **Botón 🔍 Resolver** - Ejecuta el cálculo
- **Botón 🗑️ Limpiar** - Borra entrada y salida
- **Botón 📚 Ejemplos** - Muestra ejemplos disponibles

## 📝 Notas Importantes

1. **Multiplicación implícita**: `2x` se interpreta como `2*x`
2. **Potencias**: Usa `^` o `**` (ambos funcionan)
3. **Decimal**: Usa `.` para separador decimal
4. **Variables**: Se soportan múltiples variables (x, y, z, etc.)
5. **Paréntesis**: Usa paréntesis para claridad: `(x+1)/(x-2)`

## ❌ Resolución de Problemas

Si una expresión no se resuelve:
1. Verifica la sintaxis (paréntesis balanceados)
2. Usa notación clara: `2*x` en lugar de `2x`
3. Para ecuaciones, usa formato: `expr1 = expr2`
4. Intenta con pasos detallados si es posible

---

**¿Necesitas ayuda?** Usa la pestaña de Ejemplos para ver casos de uso comunes.
