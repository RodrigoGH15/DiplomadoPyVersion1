from datetime import date

import matplotlib.pyplot as plt
import pandas as pd


def read_csv_files(file_name: str) -> pd.DataFrame:
    path = r"C:\Users\Rodri\Desktop\Diplomado\Tarea 3"
    df = pd.read_csv(rf"{path}\{file_name}", parse_dates=["Fecha"])
    df.columns = [
        "ref_date",
        "open",
        "high",
        "low",
        "close",
        "volume",
        "series",
    ]
    return df


def set_date_index(
    from_date: date, ref_date: date, df: pd.DataFrame
) -> pd.DataFrame:
    df["ref_date"] = pd.to_datetime(df["ref_date"]).dt.date
    new_index = pd.date_range(start=from_date, end=ref_date, freq="B")
    df = df.set_index("ref_date").reindex(new_index)
    return df


def test():
    # pregunta 1
    df_a = read_csv_files("accion_a.csv")
    df_b = read_csv_files("accion_b.csv")
    from_date = date(2024, 1, 2)
    ref_date = max(df_a["ref_date"].max(), df_b["ref_date"].max())
    df_a = set_date_index(from_date=from_date, ref_date=ref_date, df=df_a)
    df_b = set_date_index(from_date=from_date, ref_date=ref_date, df=df_b)
    """La UDF read_csv_files retorna un pl dataframe como se pidió y con la
    UDF set_date_index se elige el índice con las fechas desde el 2024-1-2"""

    # pregunta 2
    prices_df = pd.concat([df_a["close"], df_b["close"]], axis=1)
    prices_df.columns = ["accion_a", "accion_b"]
    df_a = df_a.drop(columns=["series"])
    df_b = df_b.drop(columns=["series"])
    """Se crea el df prices_df con los precios de cierre y se eliminan las
    columnas con los nombres de las acciones."""

    # pregunta 3
    prices_df["a_rets"] = prices_df["accion_a"].pct_change()
    prices_df["b_rets"] = prices_df["accion_b"].pct_change()
    prices_df = prices_df.loc[:, ["a_rets", "b_rets", "accion_a", "accion_b"]]
    """Se calculan los retornos diarios y se reordenan las columnas para
    tener los retornos primero."""

    # pregunta 4
    min_max_prices = {  # noqa: F841
        "accion_a": [prices_df["accion_a"].min(), prices_df["accion_a"].max()],
        "accion_b": [prices_df["accion_b"].min(), prices_df["accion_b"].max()],
        "a_rets": [prices_df["a_rets"].min(), prices_df["a_rets"].max()],
        "b_rets": [prices_df["b_rets"].min(), prices_df["b_rets"].max()],
    }
    # Se asume que se refiere a las series del prices df.
    """Se crea el diccionario min_max_prices con los valores mínimos y máximos
    de los precios y retornos."""

    # pregunta 5
    min_max_vol_dates = {  # noqa: F841
        "accion_a": [df_a["volume"].idxmin(), df_a["volume"].idxmax()],
        "accion_b": [df_b["volume"].idxmin(), df_b["volume"].idxmax()],
    }
    """Se crea el diccionario min_max_vol_dates con las fechas de los
    volúmenes mínimos y máximos de cada acción."""

    # pregunta 6
    prices_df["a_diff"] = df_a["high"] - df_a["low"]
    prices_df["b_diff"] = df_b["high"] - df_b["low"]
    max_diff_dates = {  # noqa: F841
        "accion_a": prices_df["a_diff"].idxmax(),
        "accion_b": prices_df["b_diff"].idxmax(),
    }

    # Asumí que como hablan de agregar dos columnas, entonces había que
    # agregarlas al prices_df. Si en realidad había que agregar esas columnas a
    # los df originales, entonces la solución sería:
    # df_a["diff"] = df_a["high"] - df_a["low"]
    # df_b["diff"] = df_b["high"] - df_b["low"]
    # max_diff_dates = {
    #     "accion_a": df_a["diff"].idxmax(),
    #     "accion_b": df_b["diff"].idxmax(),
    # }

    """Se agregan las columnas con la diferencia entre el precio más alto y
    el más bajo del día y se crea el diccionario max_diff_dates con las fechas
    en las que se dio la mayor diferencia para cada acción."""

    # pregunta 7
    plt.plot(prices_df["accion_a"], label="Acción A", color="#1f77b4")
    plt.plot(prices_df["accion_b"], label="Acción B", color="#003366")
    plt.title("Precios de Cierre de Acción A y Acción B")
    plt.xlabel("Fecha")
    plt.ylabel("Precio de Cierre")
    plt.legend()
    plt.grid(True)
    plt.show()

    """Se grafica con líneas los precios de cierre de ambas acciones en el
    mismo gráfico."""

    # pregunta 8
    plt.scatter(prices_df["a_rets"], prices_df["b_rets"], c="#1f77b4")
    plt.title(
        "Gráfico de Dispersión de Retornos Diarios (Acción A vs. Acción B)"
    )
    plt.xlabel("Retornos Diarios Acción A")
    plt.ylabel("Retornos Diarios Acción B")
    plt.grid(True)
    plt.show()
    """Se crea un gráfico de dispersión con los retornos diarios de una acción
    contra la otra."""


if __name__ == "__main__":
    from rich import print

    print()
    test()
