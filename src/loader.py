import pandas as pd

class Loader:
    def __init__(self, datasetList):
        self.datasetList = datasetList

    def load_dataframeList(self):
        dataframeList = []

        for dataset in self.datasetList:
            df = self._read_from_url(dataset)
            dataframeList.append(df)

        return dataframeList


    def _read_from_url(self, url):
        name = url.name.lower()

        if name.endswith('.csv'):
            return self.csv_robusto(url)
        elif name.endswith('.json'):
            return pd.read_json(url)
        else:
            raise ValueError(f"Extensión no compatible: {name}.")
        
    def csv_robusto(self,source):
        # Autodetección
        try:
            return pd.read_csv(source, sep=None, engine='python', decimal=',')
        except:
            pass

        # Forzar a decimal o semicolon
        try:
            return pd.read_csv(source, sep=';', decimal=',')
        except:
            pass

        try:
            return pd.read_csv(source, sep=',')
        except:
            pass

        raise ValueError("No se puedo interpretar el CSV con ningún método.")