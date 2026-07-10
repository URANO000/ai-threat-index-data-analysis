import pandas as pd
from collections.abc import Hashable

class Cleaner:
    def __init__(self, dataframeList):
        self.dataframeList = dataframeList

    def clean_dataframeList(self):
        clean_dataframeList = []

        for df in self.dataframeList:
            clean_df = self.clean_dataframe(df)
            clean_dataframeList.append(clean_df)
        return clean_dataframeList
    
    def clean_dataframe(self, df):
        # Primero ocupamos saber el número de filas, columnas y tipos de variables
        print(df.info())

        print("\nPrimeras filas:")
        print(df.head())

        print("\nValores nulos:")
        print(df.isna().sum())

        # Normalizamos los nombres de las columnas
        df.columns = (
            df.columns.astype(str)
            .str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )

        # En algunos datasets, las columnas pueden contener listas/objs
        print("\nDuplicados:")

        hashable_cols = self.get_hashable_columns(df)
        print(df.duplicated(subset=hashable_cols).sum())
        # Eliminamos filas duplicadas

        clean_df = df.drop_duplicates(subset=hashable_cols).copy()

        # Eliminamos filas con valores nulos
        clean_df.dropna(axis='columns', how='all', inplace=True)  # Elimina columnas que son completamente nulas
        clean_df.dropna(axis='index', how='all', inplace=True) # Elimina filas que son completamente nulas

        clean_df = clean_df.infer_objects() # Inferir tipos de daots automáticamente

        #  Reemplazar valores nulos por 'Desconocido' si es de tipo categórico, y por la mediana si es numérico
        for column in clean_df.columns:
            if pd.api.types.is_numeric_dtype(clean_df[column]):
                clean_df[column] = clean_df[column].fillna(clean_df[column].median())
            else:
                clean_df[column] = clean_df[column].fillna("Desconocido")

        return clean_df
    
    def get_hashable_columns(self, df):
        hashable_cols = []

        for col in df.columns:
            # Ignorar columnas vacías
             if df[col].dropna().map(lambda x: isinstance(x, Hashable)).all():
                hashable_cols.append(col)

        return hashable_cols

        