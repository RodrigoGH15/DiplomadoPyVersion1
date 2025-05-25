import pandas as pd


def read_csv_files(file_name: str):
    path = r"C:\Users\Rodri\Desktop\Diplomado\Tarea 3"
    df = pd.read_csv(rf"{path}\{file_name}", parse_dates=["Fecha"])
    return df


def test():
    # df_a = read_csv_files("accion_a.csv")
    df_b = read_csv_files("accion_b.csv")
    # print(df_a.dtypes)
    print(df_b.dtypes)


if __name__ == "__main__":
    from rich import print

    print()
    test()
