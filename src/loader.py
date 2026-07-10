import pandas as pd
import urllib.request
import json

class Loader:
    def __init__(self, datasetList):
        self.datasetList = datasetList

    def load_dataframeList(self):
        dataframeList = []

        for dataset in self.datasetList:
            df = self._read_from_url(dataset)

            if df is None:
                raise ValueError(f"No se pudo cargar {dataset}")

            dataframeList.append(df)

        return dataframeList


    def _read_from_url(self, url):
        name = url.lower()

        if name.endswith('.csv'):
            return self.csv_robusto(url)
        elif name.endswith('.json'): 
            return self.json_robusto(url)
        else:
            raise ValueError(f"Extensión no compatible: {name}.")
        
    def csv_robusto(self,source):
        # Autodetección
        try:
            return pd.read_csv(source, sep=None, engine='python', decimal=',')
        except Exception as e:
            print(f"Autodetección fallida: {e}")

        # Forzar a decimal o semicolon
        try:
            return pd.read_csv(source, sep=';', decimal=',')
        except Exception as e:
            print(f"Semicolon ha fallado: {e}")

        try:
            return pd.read_csv(source, sep=',')
        except Exception as e:
            print(f"Comma ha fallado: {e}")

        raise ValueError("No se puedo interpretar el CSV con ningún método.")
    
    def json_robusto(self, source):
        with urllib.request.urlopen(source) as response:
            data = json.load(response)

        if isinstance(data, list):
            return pd.DataFrame(data)
        
        if "roles" in data:
            return pd.json_normalize(data["roles"])
        
        return pd.json_normalize(data)