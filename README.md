# 🧠 Algoritmo de Memoria - memorice IA

## 📋 Descripción
Este algoritmo permite que la IA juegue memorice de forma inteligente recordando todas las cartas que ya ha visto. Tiene memoria perfecta y nunca olvida una carta.

---

## 🔄 Funcionamiento Paso a Paso

### 📊 **PASO 1: ¿Tengo parejas conocidas?**

```python
for sym, idxs in self.knowledge.items():
    cand = [i for i in idxs if i not in self.matched_cards and i not in self.revealed]
    if len(cand) >= 2:
        a, b = cand[:2]
        self.ai_play_pair(a,b)
        return
```

**¿Qué hace?**
- 🔍 Revisa el diccionario `self.knowledge` que guarda todos los símbolos ya vistos
- 🎯 Para cada símbolo, busca si tiene 2 o más posiciones disponibles
- ✅ Si encuentra una pareja completa, la juega inmediatamente
- 🚪 Sale del algoritmo (no sigue a los otros pasos)

**Ejemplo:**
```
Diccionario: {'🍎': {2, 15}, '🍌': {7}}
Resultado: Juega cartas en posiciones 2 y 15 (ambas son 🍎)
```

---

### 🎲 **PASO 2: Explorar cartas desconocidas**

```python
pool_unseen = [cartas que nunca he visto]
if not pool_unseen:
    pool_unseen = [cualquier carta disponible]
a = random.choice(pool_unseen)
self.safe_click(a)
```

**¿Qué hace?**
- 👀 Crea una lista de cartas que nunca ha visto
- 🔄 Si ya vio todas, usa cualquier carta disponible
- 🎰 Elige una carta al azar de esa lista
- 👆 Hace click en esa carta (primera carta del par)

**Ejemplo:**
```
Cartas nunca vistas: [3, 5, 8, 12, 20, 25]
Elige aleatoriamente: posición 8
```

---

### 🔍 **PASO 3: Buscar pareja para la primera carta**

```python
sym = self.symbols[a]  # Símbolo de la carta que acabo de voltear
known = [posiciones donde ya vi este símbolo]
if known:
    b = known[0]  # Juego la pareja conocida
else:
    b = random.choice(pool2)  # Exploro otra carta al azar
self.safe_click(b)
```

**¿Qué hace?**
- 🏷️ Obtiene el símbolo de la carta que acaba de voltear
- 🔎 Busca si ya conoce otras posiciones con el mismo símbolo
- ✅ Si conoce la pareja: la juega inmediatamente
- 🎲 Si no la conoce: elige otra carta al azar
- 👆 Hace click en la segunda carta

**Ejemplo:**
```
Volteé posición 8, es una 🍊
¿Conozco otras 🍊? Sí, en posición 23
Resultado: Juego posición 23 (pareja segura)
```

---

## 🗂️ Variables Importantes

### 📚 `self.knowledge`
```python
{
    '🍎': {2, 15},    # Vi manzanas en posiciones 2 y 15
    '🍌': {7},        # Vi banana en posición 7
    '🍇': {12, 23}    # Vi uvas en posiciones 12 y 23
}
```

### 🎯 `cand` (candidatos)
- Lista de posiciones del mismo símbolo que están disponibles para jugar

### 👁️ `pool_unseen` 
- Lista de cartas que nunca ha visto la IA

### 🤝 `known`
- Lista de posiciones donde ya vio el mismo símbolo que la carta recién volteada

### 🎲 `pool2`
- Lista de cartas desconocidas para elegir como segunda carta (no cuenta la recién volteada)

---

## 🎯 Estrategia del Algoritmo

### ✅ **Fortalezas:**
- 🧠 **Memoria perfecta**: Nunca olvida una carta
- 🎯 **Prioriza parejas seguras**: Siempre juega lo que sabe
- ⚡ **Rápido en decisiones**: No hace cálculos complejos

### ❌ **Debilidades:**
- 🎰 **Exploración aleatoria**: No es estratégico al explorar
- 🔄 **Puede repetir errores**: Elige cartas al azar sin aprender patrones

---

## 🔄 Flujo Completo

```
🎮 Empieza el turno
    ↓
🔍 ¿Tengo parejas conocidas?
    ↓
   SÍ → 🎯 Jugar pareja → ✅ Fin del turno
    ↓
   NO → 🎲 Elegir carta desconocida → 👆 Click 1
    ↓
🔎 ¿Conozco la pareja de esta carta?
    ↓
   SÍ → 🎯 Jugar pareja conocida → 👆 Click 2
    ↓
   NO → 🎰 Elegir carta al azar → 👆 Click 2
    ↓
✅ Fin del turno
```

---

## 💡 Resumen Simple

El algoritmo funciona como una persona con **memoria perfecta** pero que **explora sin estrategia**:

1. 🧠 Recuerda todas las cartas que ha visto
2. 🎯 Siempre juega parejas seguras primero
3. 🎲 Cuando no sabe, explora al azar
4. 📝 Aprende de cada carta nueva que voltea

**Es eficiente para recordar, pero no para explorar.**

# 🎯 Algoritmo Greedy-BFS - Memorice IA

## 📋 Descripción
Este algoritmo usa un sistema de puntuación inteligente para evaluar múltiples opciones antes de tomar una decisión. No elige al azar, sino que calcula el "valor" de cada movimiento posible y selecciona el mejor.

---

## ⚙️ Parámetros Importantes

### 🏷️ **`alpha = 0.25` (Factor de peso)**
Controla la importancia entre parejas conocidas vs. ganar información:
- 75% de importancia a parejas conocidas
- 25% de importancia a información nueva

### 📏 **`sample_cap = 12` (Límite de evaluación)**
Máximo de opciones a evaluar para evitar lentitud:
- Si hay más de 12 candidatos: toma muestra aleatoria
- Balancea calidad de decisión vs. velocidad

---

## 🔄 Funcionamiento Paso a Paso

### 📊 **PASO 1: ¿Tengo parejas conocidas? (Idéntico a Memoria)**

```python
for sym, idxs in self.knowledge.items():
    cand = [i for i in idxs if i not in self.matched_cards and i not in self.revealed]
    if len(cand) >= 2:
        a, b = cand[:2]
        self.ai_play_pair(a, b)
        return
```

**¿Qué hace?**
- 🔍 Busca parejas ya conocidas en el diccionario
- 🎯 Si encuentra una pareja disponible, la juega inmediatamente
- 🚪 Sale del algoritmo (máxima prioridad)

---

### 🎲 **PASO 2: Preparar candidatos para evaluación**

```python
unseen = [i for i in range(N) if self.is_unseen(i)]
first_candidates = unseen if unseen else [todas las disponibles]
```

**¿Qué hace?**
- 👀 Crea lista de cartas nunca vistas
- 🔄 Si ya vio todas, usa cualquier carta disponible
- 📏 Aplica sampling si hay más de 12 candidatos

**Ejemplo:**
```python
unseen = [4, 6, 10, 11, 13, 14, 16, 17, 18, 19, 20, 21, 22, 24, 25, 26]  # 16 cartas
# Sampling: 16 > 12, toma muestra aleatoria
first_candidates = [10, 14, 18, 22, 26, 30, 33, 16, 20, 24, 28, 32]  # 12 candidatos
```

---

### 🧮 **PASO 3: Sistema de evaluación inteligente**

#### **Inicialización:**
```python
best = None           # Mejor movimiento encontrado
best_score = -1e9     # Puntuación muy baja para comparar
```

#### **Evaluación de cada candidato:**
```python
for a in first_candidates:  # Evalúa cada carta como primera opción
```

### **🎯 CASO A: Carta con pareja conocida (SCORE MÁXIMO)**

```python
partner = self.known_partner_for(a)
if partner is not None:
    match_now = 1      # 🏆 Pareja garantizada
    info_gain = 0      # No gana información nueva
    score = 1 + 0.25 * 0 = 1.0  # PUNTUACIÓN MÁXIMA
    
    if score > best_score:
        best_score = score
        best = (a, partner)
    continue  # Salta evaluación exploratoria
```

**Ejemplo:**
```python
# Carta A = 14, ya conoce su pareja en posición 28
score = 1.0  # Imbatible
```

### **🔍 CASO B: Exploración inteligente**

```python
# Obtener candidatos para segunda carta
pool_b = [todas las cartas disponibles excepto 'a']
candidates_b = pool_b (con sampling si es necesario)

for b in candidates_b:  # Evalúa cada combinación (a, b)
```

#### **Sistema de puntuación por información:**
```python
match_now = 0  # No sabemos si es pareja
gain = 1 if self.is_unseen(a) else 0  # +1 si carta A nunca vista
if self.is_unseen(b):
    gain += 1                         # +1 si carta B nunca vista
if self.known_partner_for(b) is not None:
    gain += 0.25                      # +0.25 si B tiene pareja conocida

score = match_now + alpha * gain
```

#### **Ejemplos de puntuación:**

**Dos cartas nuevas:**
```python
# (10, 18) - Ambas nunca vistas
gain = 1 + 1 = 2
score = 0 + 0.25 * 2 = 0.50
```

**Una carta nueva, una conocida:**
```python
# (10, 7) - A nueva, B ya vista
gain = 1 + 0 = 1  
score = 0 + 0.25 * 1 = 0.25
```

**Carta nueva + carta con pareja conocida:**
```python
# (10, 5) - A nueva, B tiene pareja conocida
gain = 1 + 0 + 0.25 = 1.25
score = 0 + 0.25 * 1.25 = 0.31
```

#### **Actualización del mejor movimiento:**
```python
if score > best_score:
    best_score = score
    best = (a, b)
```

---

### 🎮 **PASO 4: Ejecutar mejor movimiento**

```python
if best is None:
    return  # No encontró movimiento válido

a, b = best  # Desempaqueta mejor movimiento encontrado
self.safe_click(a)
self.master.after_idle(lambda: self.safe_click(b))
```

---

## 🗂️ Variables Importantes

### 🔍 **`first_candidates`**
- Lista de cartas nunca vistas (máximo 12)
- Evaluadas como primera carta del movimiento

### 🎯 **`pool_b`**
- Todas las cartas disponibles excepto la carta 'a'
- Evaluadas como segunda carta del movimiento

### 🤝 **`candidates_b`**
- Muestra de `pool_b` (máximo 12 para eficiencia)

### 🏆 **`best` y `best_score`**
- Mejor movimiento y puntuación encontrados hasta el momento

---

## ⚖️ Comparación de Puntuaciones

| Tipo de Movimiento | Score | Ejemplo |
|-------------------|--------|---------|
| **Pareja conocida** | 1.0 | (5, 23) - ambas 🍎 conocidas |
| **Dos cartas nuevas** | 0.50 | (10, 18) - exploración máxima |
| **Nueva + con pareja** | 0.31 | (10, 5) - B tiene pareja conocida |
| **Una carta nueva** | 0.25 | (10, 7) - B ya conocida |
| **Ambas conocidas** | 0.06 | (2, 15) - repetir información |

---

## 🎯 Estrategia del Algoritmo

### ✅ **Fortalezas:**
- 🧠 **Evaluación inteligente**: Compara múltiples opciones antes de decidir
- 🎯 **Prioriza certeza**: Las parejas conocidas siempre ganan
- 📊 **Sistema de puntuación**: Valora tanto aciertos como información
- 🔍 **Exploración estratégica**: Prefiere cartas nuevas sobre repetidas

### ❌ **Debilidades:**
- ⏱️ **Más lento**: Hace más cálculos que el algoritmo de memoria
- 🔢 **Complejidad**: O(n²) evaluaciones en el peor caso
- 🎲 **Sampling aleatorio**: Puede perder la opción óptima por muestreo

---

## 🔄 Flujo Completo

```
🎮 Empieza el turno
    ↓
🔍 ¿Tengo parejas conocidas?
    ↓
   SÍ → 🎯 Jugar pareja → ✅ Fin del turno
    ↓
   NO → 📊 Preparar candidatos (max 12)
    ↓
🧮 Para cada carta A:
    ↓
   🤔 ¿A tiene pareja conocida?
    ↓
   SÍ → 🏆 Score = 1.0
    ↓
   NO → 🔍 Evaluar combinaciones (A, B)
         📊 Calcular score por información
    ↓
✅ Elegir movimiento con mejor score
    ↓
👆 Ejecutar clicks
```

---

## 📈 Ejemplo de Evaluación Completa

```python
# Estado del juego:
self.knowledge = {'🍎': {5, 23}, '🍌': {7}}
first_candidates = [10, 14, 18, 22]

# Evaluaciones:
Carta 10: Sin pareja → Mejor combo (10, 18) = 0.50
Carta 14: Con pareja → Score = 1.0  ← GANADOR
Carta 18: Sin pareja → Mejor combo (18, 22) = 0.50
Carta 22: Sin pareja → Mejor combo (22, 26) = 0.25

# Resultado: Ejecuta (14, pareja_de_14)
```

---

## 💡 Resumen Simple

El algoritmo funciona como un **estratega que evalúa todas las opciones**:

1. 🔍 **Analiza** múltiples posibilidades en lugar de elegir al azar
2. 🏆 **Prioriza** parejas conocidas (score máximo)
3. 📊 **Valora** la información nueva al explorar
4. 🎯 **Elige** siempre la opción con mejor puntuación
5. ⚡ **Optimiza** velocidad con sampling inteligente

**Es más lento que memoria, pero toma decisiones más inteligentes.**

# 📊 Tiempos de Ejecución
![image alt](https://github.com/andres-trrs/Memorice-IA/blob/db7a592f3cc3902e597afdbafb701b6f384b2b21/1.png)

# 📊 Número de movimientos
![image alt](https://github.com/andres-trrs/Memorice-IA/blob/d33a02612389634c47ac6d53669d08d7830d75b9/2.png)
