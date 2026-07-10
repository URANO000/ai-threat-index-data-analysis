from loader import Loader
from cleaner import Cleaner
from analyzer import Analyzer
from pprint import pprint


def main():
    # Cargar los datos
    urls = ["https://huggingface.co/datasets/Anthropic/EconomicIndex/raw/main/labor_market_impacts/job_exposure.csv", "https://www.meritforgeai.com/data/ai-career-threat-index.json"]

    loader = Loader(urls)
    dataframeList = loader.load_dataframeList()

    # Limpiar los datos
    cleaner = Cleaner(dataframeList)
    df_clean = cleaner.clean_dataframeList()

    # Analizar los datos
    analyzer = Analyzer(df_clean)
    resultados = analyzer.analyze_dataframeList()

    for i, resultados in enumerate(resultados, start=1):
        print(f"\n{'=' * 60}")
        print(f"DataFrame {i}")
        print(f"{'=' * 60}")

        for key, value in resultados.items():
            print(f"\n{key}:")
            pprint(value, sort_dicts=False)


if __name__ == "__main__":
    main()