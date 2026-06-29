"""Construye curso/clase08/homework01.ipynb — 8 ejercicios autocalificables del proyecto integrador.

Cada ejercicio combina NumPy + Pandas + lógica condicional para resolver
un problema realista de análisis de datos.

compartir_ns=True porque las funciones se usan entre sí.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hwtools import construir_homework, validar  # noqa: E402

NI = 'raise NotImplementedError("Implementa esta función")'

ejercicios = [
    {
        "n": 1,
        "titulo": "pipeline_cargar(ruta_csv)",
        "enunciado": (
            "Implementa `pipeline_cargar(ruta_csv)` que:\n\n"
            "1. Cargue el CSV en un DataFrame.\n"
            "2. Convierta la columna `'fecha'` a `datetime`.\n"
            "3. Filtre filas con `monto <= 0`.\n"
            "4. Elimine filas con `NaN` en `['monto', 'categoria', 'ciudad']`.\n"
            "5. Reinicie el índice (`reset_index(drop=True)`).\n\n"
            "Devuelve el DataFrame limpio.\n\n"
            "**Ejemplo:** `df = pipeline_cargar('transacciones.csv')` → DataFrame sin nulos ni montos inválidos."
        ),
        "plantilla": (
            "import pandas as pd\n\n"
            "def pipeline_cargar(ruta_csv):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    " + NI
        ),
        "solucion": (
            "import pandas as pd\n\n"
            "def pipeline_cargar(ruta_csv):\n"
            "    df = pd.read_csv(ruta_csv)\n"
            "    df['fecha'] = pd.to_datetime(df['fecha'])\n"
            "    df = df[df['monto'] > 0]\n"
            "    df = df.dropna(subset=['monto', 'categoria', 'ciudad'])\n"
            "    return df.reset_index(drop=True)"
        ),
        "visibles": [
            "import pandas as pd, os, tempfile",
            "_tmp = tempfile.NamedTemporaryFile(suffix='.csv', mode='w', delete=False)",
            "_tmp.write('fecha,monto,categoria,ciudad,metodo_pago\\n2024-01-01,50000,alimentos,Bogota,efectivo\\n2024-01-02,-100,ropa,Cali,tarjeta\\n2024-01-06,30000,hogar,Cali,transferencia\\n2024-01-07,40000,electronica,Bogota,efectivo\\n')",
            "_tmp.flush(); _tmp.close()",
            "_df = pipeline_cargar(_tmp.name)",
            "assert isinstance(_df, pd.DataFrame)",
            "assert _df['monto'].min() > 0",
            "assert _df.isnull().sum().sum() == 0",
        ],
        "ocultos": [
            "import pandas as pd",
            "assert pd.api.types.is_datetime64_any_dtype(_df['fecha'])",
            "assert list(_df.index) == list(range(len(_df)))",
            "assert len(_df) == 3",
        ],
    },
    {
        "n": 2,
        "titulo": "agregar_features_temporales(df)",
        "enunciado": (
            "Implementa `agregar_features_temporales(df)` que reciba un DataFrame\n"
            "con columna `'fecha'` (datetime) y **devuelva una copia** con tres\n"
            "columnas nuevas:\n\n"
            "- `'mes'`: número de mes (1–12)\n"
            "- `'dia_semana'`: día de la semana (0=lunes … 6=domingo)\n"
            "- `'es_fin_semana'`: 1 si día_semana ∈ {5,6}, 0 si no\n\n"
            "**Ejemplo:**\n"
            "```python\n"
            "df2 = agregar_features_temporales(df)\n"
            "# df2 tiene columnas 'mes', 'dia_semana', 'es_fin_semana'\n"
            "```"
        ),
        "plantilla": (
            "import pandas as pd\n\n"
            "def agregar_features_temporales(df):\n"
            "    # ✏️ TU CÓDIGO AQUÍ — devuelve df.copy() con columnas nuevas\n"
            "    " + NI
        ),
        "solucion": (
            "import pandas as pd\n\n"
            "def agregar_features_temporales(df):\n"
            "    df2 = df.copy()\n"
            "    df2['mes']          = df2['fecha'].dt.month\n"
            "    df2['dia_semana']   = df2['fecha'].dt.dayofweek\n"
            "    df2['es_fin_semana'] = df2['dia_semana'].isin([5, 6]).astype(int)\n"
            "    return df2"
        ),
        "visibles": [
            "import pandas as pd",
            "_df2 = agregar_features_temporales(_df)",
            "assert 'mes' in _df2.columns",
            "assert 'dia_semana' in _df2.columns",
            "assert 'es_fin_semana' in _df2.columns",
        ],
        "ocultos": [
            "assert _df2['mes'].between(1, 12).all()",
            "assert _df2['dia_semana'].between(0, 6).all()",
            "assert set(_df2['es_fin_semana'].unique()).issubset({0, 1})",
            "assert len(_df2) == len(_df)",
        ],
    },
    {
        "n": 3,
        "titulo": "estadisticas_por_grupo(df, columna_grupo)",
        "enunciado": (
            "Implementa `estadisticas_por_grupo(df, columna_grupo)` que agrupe\n"
            "el DataFrame por `columna_grupo` y devuelva un DataFrame con:\n\n"
            "- `'total'`: suma de `monto`\n"
            "- `'promedio'`: media de `monto`\n"
            "- `'mediana'`: mediana de `monto`\n"
            "- `'n'`: número de transacciones\n\n"
            "Ordenado por `'total'` descendente. Redondear a 2 decimales.\n\n"
            "**Ejemplo:** `estadisticas_por_grupo(df, 'ciudad')` → tabla con una fila por ciudad."
        ),
        "plantilla": (
            "import pandas as pd\n\n"
            "def estadisticas_por_grupo(df, columna_grupo):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    " + NI
        ),
        "solucion": (
            "import pandas as pd\n\n"
            "def estadisticas_por_grupo(df, columna_grupo):\n"
            "    resultado = df.groupby(columna_grupo)['monto'].agg(\n"
            "        total='sum', promedio='mean', mediana='median', n='count'\n"
            "    ).round(2).sort_values('total', ascending=False)\n"
            "    return resultado"
        ),
        "visibles": [
            "import pandas as pd",
            "_est = estadisticas_por_grupo(_df, 'ciudad')",
            "assert isinstance(_est, pd.DataFrame)",
            "assert set(_est.columns) >= {'total', 'promedio', 'mediana', 'n'}",
        ],
        "ocultos": [
            "assert _est['total'].iloc[0] >= _est['total'].iloc[-1]",
            "_est2 = estadisticas_por_grupo(_df, 'categoria')",
            "assert _est2['n'].sum() == len(_df)",
            "assert (_est2['n'] > 0).all()",
        ],
    },
    {
        "n": 4,
        "titulo": "detectar_outliers_zscore(df, umbral)",
        "enunciado": (
            "Implementa `detectar_outliers_zscore(df, umbral=3.0)` que:\n\n"
            "1. Calcule el z-score del `monto` usando NumPy.\n"
            "2. Devuelva el subconjunto de filas donde `|z| > umbral`.\n\n"
            "Fórmula: `z = (monto - media) / std`\n\n"
            "**Ejemplo:**\n"
            "```python\n"
            "outliers = detectar_outliers_zscore(df)   # umbral por defecto 3\n"
            "len(outliers)  # número de filas atípicas\n"
            "```"
        ),
        "plantilla": (
            "import pandas as pd\nimport numpy as np\n\n"
            "def detectar_outliers_zscore(df, umbral=3.0):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    " + NI
        ),
        "solucion": (
            "import pandas as pd\nimport numpy as np\n\n"
            "def detectar_outliers_zscore(df, umbral=3.0):\n"
            "    montos = df['monto'].to_numpy()\n"
            "    z = (montos - montos.mean()) / montos.std()\n"
            "    return df[np.abs(z) > umbral].copy()"
        ),
        "visibles": [
            "import pandas as pd, numpy as np",
            "_out = detectar_outliers_zscore(_df)",
            "assert isinstance(_out, pd.DataFrame)",
            "assert set(_out.columns) == set(_df.columns)",
        ],
        "ocultos": [
            "assert len(_out) < len(_df)",
            "_out2 = detectar_outliers_zscore(_df, umbral=10.0)",
            "assert len(_out2) <= len(_out)",
            "_out3 = detectar_outliers_zscore(_df, umbral=0.5)",
            "assert len(_out3) >= len(_out)",
        ],
    },
    {
        "n": 5,
        "titulo": "concentracion_pareto(df)",
        "enunciado": (
            "Implementa `concentracion_pareto(df)` que calcule qué porcentaje\n"
            "de transacciones (del más alto al más bajo) explica el **80% del\n"
            "monto total**.\n\n"
            "Algoritmo:\n"
            "1. Ordenar montos de mayor a menor.\n"
            "2. Calcular el monto acumulado.\n"
            "3. Encontrar el índice donde el acumulado supera el 80% del total.\n"
            "4. Devolver ese porcentaje de filas como float (0–100).\n\n"
            "**Ejemplo:** si las 30 transacciones más altas de 120 explican el 80%,\n"
            "la función devuelve `25.0` (30/120 × 100)."
        ),
        "plantilla": (
            "import pandas as pd\nimport numpy as np\n\n"
            "def concentracion_pareto(df):\n"
            "    # ✏️ TU CÓDIGO AQUÍ — devuelve float (0-100)\n"
            "    " + NI
        ),
        "solucion": (
            "import pandas as pd\nimport numpy as np\n\n"
            "def concentracion_pareto(df):\n"
            "    montos_ord = df['monto'].sort_values(ascending=False).to_numpy()\n"
            "    total      = montos_ord.sum()\n"
            "    acum       = np.cumsum(montos_ord)\n"
            "    idx        = np.searchsorted(acum, total * 0.80)\n"
            "    return float((idx + 1) / len(montos_ord) * 100)"
        ),
        "visibles": [
            "import pandas as pd, numpy as np",
            "_pct = concentracion_pareto(_df)",
            "assert isinstance(_pct, float)",
            "assert 0 < _pct <= 100",
        ],
        "ocultos": [
            "import pandas as pd, numpy as np",
            "# Crear dataset completamente uniforme: Pareto = 80% exacto",
            "_df_unif = pd.DataFrame({'monto': [100.0] * 100})",
            "_pct_unif = concentracion_pareto(_df_unif)",
            "assert abs(_pct_unif - 80.0) < 2.0",
        ],
    },
    {
        "n": 6,
        "titulo": "pivot_ciudad_categoria(df)",
        "enunciado": (
            "Implementa `pivot_ciudad_categoria(df)` que devuelva una **tabla pivot**\n"
            "con ciudades en filas, categorías en columnas, y la **suma de montos** como valores.\n\n"
            "Rellena los NaN con 0. Redondea a 0 decimales.\n\n"
            "Usa `pd.pivot_table`.\n\n"
            "**Ejemplo:**\n"
            "```\n"
            "              alimentos  deportes  electronica  hogar    ropa\n"
            "ciudad\n"
            "Barranquilla  123456.0   234567.0  ...          ...      ...\n"
            "Bogota        ...        ...       ...          ...      ...\n"
            "```"
        ),
        "plantilla": (
            "import pandas as pd\n\n"
            "def pivot_ciudad_categoria(df):\n"
            "    # ✏️ TU CÓDIGO AQUÍ — usa pd.pivot_table\n"
            "    " + NI
        ),
        "solucion": (
            "import pandas as pd\n\n"
            "def pivot_ciudad_categoria(df):\n"
            "    piv = pd.pivot_table(\n"
            "        df, values='monto', index='ciudad',\n"
            "        columns='categoria', aggfunc='sum', fill_value=0\n"
            "    ).round(0)\n"
            "    return piv"
        ),
        "visibles": [
            "import pandas as pd",
            "_piv = pivot_ciudad_categoria(_df)",
            "assert isinstance(_piv, pd.DataFrame)",
            "assert _piv.isnull().sum().sum() == 0",
        ],
        "ocultos": [
            "assert _piv.index.name == 'ciudad'",
            "assert _piv.columns.name == 'categoria'",
            "assert (_piv >= 0).all().all()",
            "assert abs(_piv.values.sum() - _df['monto'].sum()) < 1.0",
        ],
    },
    {
        "n": 7,
        "titulo": "comparar_semana_finde(df)",
        "enunciado": (
            "Implementa `comparar_semana_finde(df)` que devuelva un diccionario\n"
            "comparando el ticket promedio en días de semana vs. fin de semana:\n\n"
            "```python\n"
            "{\n"
            "  'semana':    float,   # promedio lunes-viernes\n"
            "  'finde':     float,   # promedio sábado-domingo\n"
            "  'diferencia_pct': float,  # (finde - semana) / semana * 100\n"
            "}\n"
            "```\n\n"
            "Asume que `df` tiene columna `'es_fin_semana'` (0/1).\n"
            "Si `df` no tiene esa columna, créala internamente usando `dt.dayofweek`."
        ),
        "plantilla": (
            "import pandas as pd\n\n"
            "def comparar_semana_finde(df):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    " + NI
        ),
        "solucion": (
            "import pandas as pd\n\n"
            "def comparar_semana_finde(df):\n"
            "    df2 = df.copy()\n"
            "    if 'es_fin_semana' not in df2.columns:\n"
            "        df2['es_fin_semana'] = df2['fecha'].dt.dayofweek.isin([5,6]).astype(int)\n"
            "    semana = df2[df2['es_fin_semana'] == 0]['monto'].mean()\n"
            "    finde  = df2[df2['es_fin_semana'] == 1]['monto'].mean()\n"
            "    dif    = (finde - semana) / semana * 100 if semana > 0 else 0.0\n"
            "    return {'semana': round(semana, 2), 'finde': round(finde, 2),\n"
            "            'diferencia_pct': round(dif, 2)}"
        ),
        "visibles": [
            "import pandas as pd",
            "_comp = comparar_semana_finde(_df2)",
            "assert isinstance(_comp, dict)",
            "assert {'semana', 'finde', 'diferencia_pct'} <= set(_comp.keys())",
        ],
        "ocultos": [
            "assert isinstance(_comp['semana'], float)",
            "assert isinstance(_comp['finde'], float)",
            "assert isinstance(_comp['diferencia_pct'], float)",
            "assert _comp['semana'] > 0 and _comp['finde'] > 0",
        ],
    },
    {
        "n": 8,
        "titulo": "resumen_ejecutivo(df)",
        "enunciado": (
            "Implementa `resumen_ejecutivo(df)` que integre todo el pipeline y\n"
            "devuelva un diccionario con las métricas clave del negocio:\n\n"
            "```python\n"
            "{\n"
            "  'total_ventas':    float,\n"
            "  'ticket_promedio': float,\n"
            "  'ticket_mediano':  float,\n"
            "  'ciudad_top':      str,     # ciudad con mayor volumen\n"
            "  'categoria_top':   str,     # categoría con mayor volumen\n"
            "  'metodo_top':      str,     # método de pago más usado\n"
            "  'pct_outliers':    float,   # % de transacciones outlier (z>3)\n"
            "}\n"
            "```\n\n"
            "Usa las funciones `estadisticas_por_grupo` y `detectar_outliers_zscore`."
        ),
        "plantilla": (
            "import pandas as pd\nimport numpy as np\n\n"
            "def resumen_ejecutivo(df):\n"
            "    # ✏️ TU CÓDIGO AQUÍ — usa estadisticas_por_grupo y detectar_outliers_zscore\n"
            "    " + NI
        ),
        "solucion": (
            "import pandas as pd\nimport numpy as np\n\n"
            "def resumen_ejecutivo(df):\n"
            "    ciudad_top   = df.groupby('ciudad')['monto'].sum().idxmax()\n"
            "    categoria_top = df.groupby('categoria')['monto'].sum().idxmax()\n"
            "    metodo_top   = df['metodo_pago'].value_counts().idxmax()\n"
            "    outliers     = detectar_outliers_zscore(df)\n"
            "    pct_out      = len(outliers) / len(df) * 100 if len(df) > 0 else 0.0\n"
            "    return {\n"
            "        'total_ventas':    round(float(df['monto'].sum()), 2),\n"
            "        'ticket_promedio': round(float(df['monto'].mean()), 2),\n"
            "        'ticket_mediano':  round(float(df['monto'].median()), 2),\n"
            "        'ciudad_top':      ciudad_top,\n"
            "        'categoria_top':   categoria_top,\n"
            "        'metodo_top':      metodo_top,\n"
            "        'pct_outliers':    round(pct_out, 2),\n"
            "    }"
        ),
        "visibles": [
            "import pandas as pd, numpy as np",
            "_res = resumen_ejecutivo(_df)",
            "assert isinstance(_res, dict)",
            "assert {'total_ventas','ticket_promedio','ciudad_top','categoria_top'} <= set(_res.keys())",
            "assert _res['total_ventas'] > 0",
        ],
        "ocultos": [
            "assert isinstance(_res['ciudad_top'], str)",
            "assert isinstance(_res['categoria_top'], str)",
            "assert isinstance(_res['metodo_top'], str)",
            "assert 0 <= _res['pct_outliers'] <= 100",
            "assert _res['ticket_promedio'] >= _res['ticket_mediano'] * 0.5",
        ],
    },
]

meta = {
    "intro_md": r"""
# Clase 8 · Tarea 01 — Funciones del pipeline integrador

### Proyecto integrador · ejercicios autocalificables

En esta tarea implementas las funciones de un pipeline de ciencia de datos
completo. Cada función es un bloque independiente que después usarás en
conjunto para el mini proyecto de la Tarea 02.

```
pipeline_cargar
      │
      ▼
agregar_features_temporales
      │
      ▼
estadisticas_por_grupo ──┐
detectar_outliers_zscore  │──▶ resumen_ejecutivo
concentracion_pareto    ──┘
pivot_ciudad_categoria
comparar_semana_finde
```

**Instrucciones**

1. Implementa cada función en su celda correspondiente.
2. Ejecuta los tests de cada función hasta ver ✅.
3. Las funciones se usan entre sí: resuélvelas en orden.

> 🧠 Traza el flujo de datos antes de programar:
> ¿qué entra? ¿qué sale? ¿qué validaciones necesito?
""",
    "cierre_md": r"""
---
## ¡Tarea completada!

Implementaste un conjunto completo de funciones para un pipeline de análisis:

| Función | Concepto principal |
|---|---|
| `pipeline_cargar` | Carga + limpieza automatizada |
| `agregar_features_temporales` | Ingeniería de features |
| `estadisticas_por_grupo` | `groupby` + `agg` |
| `detectar_outliers_zscore` | NumPy vectorizado |
| `concentracion_pareto` | `np.cumsum` + `np.searchsorted` |
| `pivot_ciudad_categoria` | `pd.pivot_table` |
| `comparar_semana_finde` | Análisis temporal + comparación |
| `resumen_ejecutivo` | **Integración total** |

### Reto opcional (sin calificar)

- Modifica `resumen_ejecutivo` para que incluya `'skewness'` del monto.
- Agrega a `comparar_semana_finde` el número de transacciones de cada grupo.
- ¿Cómo cambiarías `concentracion_pareto` para que acepte un umbral
  diferente al 80%?

> 💡 En la Tarea 02 usarás estas funciones para generar un reporte completo
> sobre un dataset nuevo.
""",
}

# ============================================================ #
# VALIDACIÓN EN TIEMPO DE BUILD
# ============================================================ #
def _validar():
    import pandas as pd
    import numpy as np

    ruta_csv = os.path.join(
        os.path.dirname(__file__), "..", "curso", "datasets", "transacciones.csv"
    )
    validar(ejercicios, compartir_ns=True)

_validar()

# ============================================================ #
# BUILD
# ============================================================ #
dest = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "curso", "clase08", "homework01.ipynb",
)
construir_homework(
    meta,
    ejercicios,
    os.path.abspath(dest),
    os.path.join(os.path.dirname(__file__), "solved", "clase08_homework01_solved.ipynb"),
)
print(f"✔  Generado: {dest}")
