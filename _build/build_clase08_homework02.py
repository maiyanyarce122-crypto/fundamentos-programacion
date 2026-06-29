"""Construye curso/clase08/homework02.ipynb — mini proyecto: reporte integrador automatizado.

Proyecto final: el estudiante implementa, pieza a pieza, un generador de
reporte de ciencia de datos que funciona sobre cualquier dataset CSV numérico.
Las partes se construyen de forma incremental y la última las integra todas.

compartir_ns=True porque las partes se usan entre sí.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hwtools import construir_homework, validar  # noqa: E402

NI = 'raise NotImplementedError("Implementa esta función")'

ejercicios = [
    {
        "n": 1,
        "titulo": "Parte 1 — perfilar_dataset(df)",
        "enunciado": (
            "Implementa `perfilar_dataset(df)` que reciba un DataFrame y devuelva\n"
            "un dict con el perfil completo:\n\n"
            "```python\n"
            "{\n"
            "  'filas': int,\n"
            "  'columnas': int,\n"
            "  'duplicados': int,\n"
            "  'nulos_total': int,\n"
            "  'nulos_por_columna': dict,   # solo col con nulos\n"
            "  'columnas_numericas': list,\n"
            "  'columnas_categoricas': list,\n"
            "}\n"
            "```\n\n"
            "**Pista:** usa `df.select_dtypes(include='number').columns.tolist()` y\n"
            "`df.select_dtypes(exclude='number').columns.tolist()`."
        ),
        "plantilla": (
            "import pandas as pd\nimport numpy as np\n\n"
            "def perfilar_dataset(df):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {ni}"
        ).format(ni=NI),
        "solucion": (
            "import pandas as pd\nimport numpy as np\n\n"
            "def perfilar_dataset(df):\n"
            "    nulos = df.isnull().sum()\n"
            "    nulos_por_col = {c: int(v) for c, v in nulos[nulos > 0].items()}\n"
            "    return {\n"
            "        'filas':                len(df),\n"
            "        'columnas':             len(df.columns),\n"
            "        'duplicados':           int(df.duplicated().sum()),\n"
            "        'nulos_total':          int(df.isnull().sum().sum()),\n"
            "        'nulos_por_columna':    nulos_por_col,\n"
            "        'columnas_numericas':   df.select_dtypes(include='number').columns.tolist(),\n"
            "        'columnas_categoricas': df.select_dtypes(exclude='number').columns.tolist(),\n"
            "    }"
        ),
        "visibles": [
            "import pandas as pd, numpy as np",
            "_df_p = pd.DataFrame({'a': [1.0, np.nan, 1.0], 'b': ['x', 'y', 'x']})",
            "_r1 = perfilar_dataset(_df_p)",
            "assert _r1['filas'] == 3",
            "assert _r1['columnas'] == 2",
            "assert _r1['nulos_total'] == 1",
        ],
        "ocultos": [
            "assert _r1['duplicados'] == 1",
            "assert _r1['nulos_por_columna'] == {'a': 1}",
            "assert 'a' in _r1['columnas_numericas']",
            "assert 'b' in _r1['columnas_categoricas']",
        ],
    },
    {
        "n": 2,
        "titulo": "Parte 2 — estadisticas_numericas(df)",
        "enunciado": (
            "Implementa `estadisticas_numericas(df)` que devuelva un **DataFrame**\n"
            "con una fila por columna numérica y las columnas:\n"
            "`media`, `mediana`, `std`, `minimo`, `maximo`, `skewness`.\n\n"
            "Redondea todos los valores a 2 decimales.\n\n"
            "**Pista:** filtra con `df.select_dtypes(include='number')` y\n"
            "construye el DataFrame a mano con `pd.DataFrame({...})`."
        ),
        "plantilla": (
            "import pandas as pd\nimport numpy as np\n\n"
            "def estadisticas_numericas(df):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {ni}"
        ).format(ni=NI),
        "solucion": (
            "import pandas as pd\nimport numpy as np\n\n"
            "def estadisticas_numericas(df):\n"
            "    num = df.select_dtypes(include='number')\n"
            "    resultado = pd.DataFrame({\n"
            "        'media':    num.mean(),\n"
            "        'mediana':  num.median(),\n"
            "        'std':      num.std(),\n"
            "        'minimo':   num.min(),\n"
            "        'maximo':   num.max(),\n"
            "        'skewness': num.skew(),\n"
            "    }).round(2)\n"
            "    return resultado"
        ),
        "visibles": [
            "import pandas as pd",
            "_df_e = pd.DataFrame({'x': [1.0, 2.0, 3.0], 'y': [10.0, 20.0, 30.0], 'z': ['a','b','c']})",
            "_r2 = estadisticas_numericas(_df_e)",
            "assert isinstance(_r2, pd.DataFrame)",
            "assert 'media' in _r2.columns and 'skewness' in _r2.columns",
            "assert set(_r2.index) == {'x', 'y'}",
        ],
        "ocultos": [
            "assert abs(_r2.loc['x', 'media'] - 2.0) < 1e-3",
            "assert abs(_r2.loc['y', 'mediana'] - 20.0) < 1e-3",
            "_df_e2 = pd.DataFrame({'a': [1.0, 1.0, 1.0]})",
            "_r2b = estadisticas_numericas(_df_e2)",
            "assert _r2b.loc['a', 'minimo'] == _r2b.loc['a', 'maximo']",
        ],
    },
    {
        "n": 3,
        "titulo": "Parte 3 — detectar_outliers(df, columna, umbral)",
        "enunciado": (
            "Implementa `detectar_outliers(df, columna, umbral=3.0)` que:\n\n"
            "1. Calcule el z-score de `columna` usando NumPy.\n"
            "2. Devuelva el subconjunto de filas con `|z| > umbral`.\n"
            "3. Incluya una columna extra `'zscore'` con el valor del z.\n\n"
            "**Ejemplo:**\n"
            "```python\n"
            "out = detectar_outliers(df, 'monto')\n"
            "# out tiene todas las columnas de df + 'zscore'\n"
            "```"
        ),
        "plantilla": (
            "import pandas as pd\nimport numpy as np\n\n"
            "def detectar_outliers(df, columna, umbral=3.0):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {ni}"
        ).format(ni=NI),
        "solucion": (
            "import pandas as pd\nimport numpy as np\n\n"
            "def detectar_outliers(df, columna, umbral=3.0):\n"
            "    valores = df[columna].to_numpy().astype(float)\n"
            "    z = (valores - valores.mean()) / valores.std()\n"
            "    mask = np.abs(z) > umbral\n"
            "    resultado = df[mask].copy()\n"
            "    resultado['zscore'] = z[mask]\n"
            "    return resultado.reset_index(drop=True)"
        ),
        "visibles": [
            "import pandas as pd, numpy as np",
            "_s_big = pd.Series(list(range(1, 21)) + [500])",
            "_df_o = pd.DataFrame({'val': _s_big})",
            "_out3 = detectar_outliers(_df_o, 'val')",
            "assert isinstance(_out3, pd.DataFrame)",
            "assert 'zscore' in _out3.columns",
            "assert 500 in _out3['val'].values",
        ],
        "ocultos": [
            "_out3b = detectar_outliers(_df_o, 'val', umbral=10.0)",
            "assert len(_out3b) == 0",
            "_out3c = detectar_outliers(_df_o, 'val', umbral=1.0)",
            "assert len(_out3c) >= len(_out3)",
        ],
    },
    {
        "n": 4,
        "titulo": "Parte 4 — top_valores(df, columna_grupo, columna_valor, n)",
        "enunciado": (
            "Implementa `top_valores(df, columna_grupo, columna_valor, n=5)` que:\n\n"
            "1. Agrupe por `columna_grupo`.\n"
            "2. Sume `columna_valor` por grupo.\n"
            "3. Devuelva los `n` grupos con mayor suma, como DataFrame con:\n"
            "   - índice = `columna_grupo`\n"
            "   - columna `'total'`\n"
            "   - columna `'pct'` (porcentaje del total general, redondeado a 1 decimal)\n\n"
            "**Ejemplo:**\n"
            "```python\n"
            "top_valores(df, 'ciudad', 'monto', 3)\n"
            "# las 3 ciudades con mayor monto + su porcentaje del total\n"
            "```"
        ),
        "plantilla": (
            "import pandas as pd\n\n"
            "def top_valores(df, columna_grupo, columna_valor, n=5):\n"
            "    # ✏️ TU CÓDIGO AQUÍ\n"
            "    {ni}"
        ).format(ni=NI),
        "solucion": (
            "import pandas as pd\n\n"
            "def top_valores(df, columna_grupo, columna_valor, n=5):\n"
            "    totales = df.groupby(columna_grupo)[columna_valor].sum()\n"
            "    top     = totales.nlargest(n)\n"
            "    gran_total = totales.sum()\n"
            "    resultado = pd.DataFrame({\n"
            "        'total': top,\n"
            "        'pct':   (top / gran_total * 100).round(1),\n"
            "    })\n"
            "    return resultado"
        ),
        "visibles": [
            "import pandas as pd",
            "_df_t = pd.DataFrame({'grp': list('AAABBBCCC'), 'val': [10,20,30,5,5,5,1,1,1]})",
            "_top4 = top_valores(_df_t, 'grp', 'val', 2)",
            "assert isinstance(_top4, pd.DataFrame)",
            "assert 'total' in _top4.columns and 'pct' in _top4.columns",
            "assert len(_top4) == 2",
        ],
        "ocultos": [
            "assert _top4.index[0] == 'A'",
            "assert abs(_top4.loc['A', 'total'] - 60) < 1e-3",
            "assert abs(_top4['pct'].sum() - (60+15)/78*100) < 0.2",
        ],
    },
    {
        "n": 5,
        "titulo": "Parte 5 — correlacion_variables(df)",
        "enunciado": (
            "Implementa `correlacion_variables(df)` que calcule la **matriz de\n"
            "correlación** de las columnas numéricas y devuelva un DataFrame\n"
            "redondeado a 3 decimales.\n\n"
            "También devuelve el **par de variables más correlacionado** (excluyendo\n"
            "la diagonal) como una tupla `(var1, var2, r)`.\n\n"
            "Devuelve: `(matriz_corr, (var1, var2, r))`\n\n"
            "**Pista:** usa `df.corr()`, luego convierte a numpy con `.to_numpy().copy()`,\n"
            "pon el diagonal en 0 con `np.fill_diagonal`, y usa `np.argmax` + `np.unravel_index`."
        ),
        "plantilla": (
            "import pandas as pd\nimport numpy as np\n\n"
            "def correlacion_variables(df):\n"
            "    # ✏️ TU CÓDIGO AQUÍ — devuelve (DataFrame, (str, str, float))\n"
            "    {ni}"
        ).format(ni=NI),
        "solucion": (
            "import pandas as pd\nimport numpy as np\n\n"
            "def correlacion_variables(df):\n"
            "    num  = df.select_dtypes(include='number')\n"
            "    corr = num.corr().round(3)\n"
            "    arr  = corr.to_numpy().copy().astype(float)\n"
            "    np.fill_diagonal(arr, 0)\n"
            "    idx  = np.unravel_index(np.argmax(np.abs(arr)), arr.shape)\n"
            "    var1 = corr.index[idx[0]]\n"
            "    var2 = corr.columns[idx[1]]\n"
            "    r    = float(corr.iloc[idx[0], idx[1]])\n"
            "    return corr, (var1, var2, r)"
        ),
        "visibles": [
            "import pandas as pd, numpy as np",
            "_df_c = pd.DataFrame({'x': [1.0,2.0,3.0,4.0], 'y': [2.0,4.0,6.0,8.0], 'z': [1.0,0.0,1.0,0.0]})",
            "_mat, _par = correlacion_variables(_df_c)",
            "assert isinstance(_mat, pd.DataFrame)",
            "assert isinstance(_par, tuple) and len(_par) == 3",
        ],
        "ocultos": [
            "assert abs(_mat.loc['x', 'y'] - 1.0) < 1e-3",
            "assert set(_par[:2]) == {'x', 'y'}",
            "assert abs(_par[2]) >= abs(_mat.loc['x', 'z'])",
        ],
    },
    {
        "n": 6,
        "titulo": "Parte 6 — generar_reporte(df, titulo)",
        "enunciado": (
            "Implementa `generar_reporte(df, titulo='Reporte de datos')` que\n"
            "integre todas las partes anteriores y devuelva un dict con el\n"
            "reporte completo:\n\n"
            "```python\n"
            "{\n"
            "  'titulo':             str,\n"
            "  'perfil':             dict,          # perfilar_dataset\n"
            "  'estadisticas':       pd.DataFrame,  # estadisticas_numericas\n"
            "  'n_outliers':         int,            # count de detectar_outliers (umbral=3)\n"
            "  'correlacion_max':    tuple,          # (var1, var2, r) de correlacion_variables\n"
            "}\n"
            "```\n\n"
            "Usa `'monto'` como columna para `detectar_outliers`. Si el df no tiene\n"
            "`'monto'`, usa la primera columna numérica del perfil."
        ),
        "plantilla": (
            "import pandas as pd\nimport numpy as np\n\n"
            "def generar_reporte(df, titulo='Reporte de datos'):\n"
            "    # ✏️ TU CÓDIGO AQUÍ — integra perfilar_dataset, estadisticas_numericas,\n"
            "    # detectar_outliers y correlacion_variables\n"
            "    {ni}"
        ).format(ni=NI),
        "solucion": (
            "import pandas as pd\nimport numpy as np\n\n"
            "def generar_reporte(df, titulo='Reporte de datos'):\n"
            "    perfil = perfilar_dataset(df)\n"
            "    estadisticas = estadisticas_numericas(df)\n"
            "    col_num = 'monto' if 'monto' in perfil['columnas_numericas'] else perfil['columnas_numericas'][0]\n"
            "    out = detectar_outliers(df, col_num)\n"
            "    _, par_corr = correlacion_variables(df)\n"
            "    return {\n"
            "        'titulo':          titulo,\n"
            "        'perfil':          perfil,\n"
            "        'estadisticas':    estadisticas,\n"
            "        'n_outliers':      len(out),\n"
            "        'correlacion_max': par_corr,\n"
            "    }"
        ),
        "visibles": [
            "import pandas as pd, numpy as np",
            "_df_r = pd.DataFrame({'monto': list(range(1,21)) + [500], 'cat': ['a']*21})",
            "_rep = generar_reporte(_df_r, titulo='Test')",
            "assert isinstance(_rep, dict)",
            "assert {'titulo','perfil','estadisticas','n_outliers','correlacion_max'} <= set(_rep.keys())",
            "assert _rep['titulo'] == 'Test'",
        ],
        "ocultos": [
            "assert _rep['n_outliers'] >= 1",
            "assert isinstance(_rep['estadisticas'], pd.DataFrame)",
            "assert isinstance(_rep['correlacion_max'], tuple)",
            "assert _rep['perfil']['filas'] == 21",
        ],
    },
]

meta = {
    "intro_md": r"""
# Clase 8 · Tarea 02 — Mini proyecto: generador de reportes de datos

### Proyecto integrador final · pipeline completo

En esta tarea construyes, pieza a pieza, un **generador automático de reportes**
que puede analizar cualquier DataFrame y producir un resumen ejecutivo completo.

```
DataFrame
    │
    ▼
[Parte 1] perfilar_dataset      → dimensiones, nulos, tipos
    │
    ▼
[Parte 2] estadisticas_numericas → media, std, skewness por columna
    │
    ▼
[Parte 3] detectar_outliers      → filas atípicas con z-score
    │
    ▼
[Parte 4] top_valores            → ranking de grupos
    │
    ▼
[Parte 5] correlacion_variables  → relaciones entre columnas
    │
    ▼
[Parte 6] generar_reporte        → INTEGRACIÓN TOTAL
```

**Instrucciones**

1. Implementa cada parte en su celda correspondiente.
2. Las partes 3–6 dependen de las anteriores — resuélvelas en orden.
3. La Parte 6 integra todo: si las 5 anteriores pasan, la 6 también pasará.

> 🎯 **Meta:** al terminar, `generar_reporte(df)` funciona sobre
> **cualquier** DataFrame CSV con columnas numéricas.
""",
    "cierre_md": r"""
---
## ¡Proyecto final completado!

Construiste un generador de reportes que combina todos los conceptos del curso:

| Parte | Concepto |
|---|---|
| `perfilar_dataset` | Estructuras de datos + Pandas |
| `estadisticas_numericas` | `groupby`, `agg`, `skew` |
| `detectar_outliers` | NumPy vectorizado |
| `top_valores` | `nlargest`, porcentajes |
| `correlacion_variables` | Álgebra lineal con NumPy |
| `generar_reporte` | **Integración total** |

### Reto opcional (sin calificar)

- Agrega una función `visualizar_reporte(reporte)` que genere 2–3 gráficos
  a partir del dict devuelto por `generar_reporte`.
- Convierte el reporte a un string formateado legible para imprimir en
  consola (similar a un dashboard en texto).
- ¿Cómo exportarías el reporte a un archivo JSON para compartirlo?
  (**Pista:** `json.dumps`, pero los DataFrames necesitan `.to_dict()`.)

### Reflexión final

> *"El objetivo del análisis de datos no es producir gráficos o tablas —*
> *es tomar mejores decisiones con evidencia."*

Las herramientas que aprendiste (Python, NumPy, Pandas) son medios, no fines.
Lo importante es el pensamiento algorítmico que desarrollaste: descomponer un
problema complejo en funciones pequeñas, verificables y reutilizables.

Eso es exactamente lo que hacen los científicos de datos profesionales.

> ✅ **Curso completado.** Tienes las bases para seguir con machine learning,
> visualización avanzada, SQL, o cualquier herramienta del ecosistema de datos.
""",
}


# ============================================================ #
# VALIDACIÓN EN TIEMPO DE BUILD
# ============================================================ #
def _validar():
    import pandas as pd
    import numpy as np
    validar(ejercicios, compartir_ns=True)

_validar()

# ============================================================ #
# BUILD
# ============================================================ #
dest = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..", "curso", "clase08", "homework02.ipynb",
)
construir_homework(
    meta,
    ejercicios,
    os.path.abspath(dest),
    os.path.join(os.path.dirname(__file__), "solved", "clase08_homework02_solved.ipynb"),
)
print(f"✔  Generado: {dest}")
