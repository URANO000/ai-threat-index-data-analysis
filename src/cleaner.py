import pandas as pd

class Cleaner:
    def __init__(self, dataframeList):
        self.dataframeList = dataframeList

    def clean_dataframeList(self):
        clean_dataframeList = []

        for df in self.dataframeList:
            clean_df = self.clean_dataframe(df)
            clean_dataframeList.append(clean_df)
        return self.clean_dataframeList
    
    def clean_dataframe(self, df):
        # Primero ocupamos saber el número de filas, columnas y tipos de variables
        print(f"Información del DataFrame : {df.info()}")
        print(f"Estadísticas descriptivas del DataFrame : {df.describe(include='all')}")

        # Normalizamos los nombres de las columnas
        df.columns = (df.columns
                      .str.strip() # Elimina espacios en blanco al inicio y al final del nombre
                      .str.lower() # Convierte el nombre a minúsculas
                      .str.replace(' ', '_')  # Espacios se reemplazan por guiones bajos
        )

        # Eliminamos filas duplicadas
        clean_df = df.drop_duplicates().copy()

        # Eliminamos filas con valores nulos
        clean_df.dropna(axis='columns', how='all', inplace=True)  # Elimina columnas que son completamente nulas
        clean_df.dropna(axis='index', how='all', inplace=True) # Elimina filas que son completamente nulas
        print(f"Información del DataFrame limpio : {clean_df.info()}")

        clean_df = clean_df.infer_objects() # Inferir tipos de daots automáticamente

        #  Reemplazar valores nulos por 'Desconocido' si es de tipo categórico, y por la mediana si es numérico
        for column in clean_df.columns:
            if pd.api.types.is_numeric_dtype(clean_df[column]):
                clean_df[column] = clean_df[column].fillna(clean_df[column].median())
            else:
                clean_df[column] = clean_df[column].fillna("Desconocido")

        return self.clean_df

        