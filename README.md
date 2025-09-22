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

![image alt] ([https://github.com/andres-trrs/Memorice-IA/blob/main/images/1.png?raw=true](https://github.com/andres-trrs/Memorice-IA/blob/db7a592f3cc3902e597afdbafb701b6f384b2b21/1.png))
