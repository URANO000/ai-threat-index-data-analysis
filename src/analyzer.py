import pandas as pd
import numpy as np

class Analyzer:
    def __init__(self, dataframeList):
        self.dataframeList = dataframeList

    def analyze_dataframeList(self):
        results = []

        for df in self.dataframeList:
            result = self.analyze_dataframe(df)
            results.append(result)

        return results
    
    # Detectar tipos
    def detect_types(self, df):

        numeric_cols = df.select_dtypes(include=np.number).columns
        categorical_cols = df.select_dtypes(include=['object', 'string']).columns
        boolean_cols = df.select_dtypes(include='bool').columns

        return numeric_cols, categorical_cols, boolean_cols
    
    # Análisis descriptivo
    def descriptive_statistics(self, df, numeric_cols):

        stats = {} # diccionario

        for col in numeric_cols:
            stats[col] = {
                "promedio" : float(df[col].mean()),
                "mediana" : float(df[col].median()),
                "std" : float(df[col].std()), # Cualquier cosa, es la desviación estándar
                "min" : float(df[col].min()),
                "max" : float(df[col].max())
            }

        return stats
    

    # Retornar todos los datos de un solo
    def analyze_dataframe(self, df):

        numeric_cols, categorical_cols, boolean_cols = self.detect_types(df)
        stats = self.descriptive_statistics(df, numeric_cols)


        return {
            "Columnas Numéricas" : numeric_cols.tolist(),
            "Columnas Categóricas" : categorical_cols.tolist(),
            "Columnas Booleanas": boolean_cols.tolist(),
            "Estadísticas": stats
        }