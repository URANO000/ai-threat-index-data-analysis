from loader import Loader
from cleaner import Cleaner
from analyzer import Analyzer
from pprint import pprint
from visualizer import Visualizer


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

    # Identificar valores atípicos de la exposición observada
    exposure_outliers = analyzer.detect_outliers(
        df_clean[0],
        "observed_exposure"
    )

    print("\nValores atípicos de exposición observada")
    print("Límite inferior:", exposure_outliers["lower_limit"])
    print("Límite superior:", exposure_outliers["upper_limit"])
    print("Cantidad de valores atípicos:", len(exposure_outliers["outliers"]))

    print(
        exposure_outliers["outliers"][
            ["title", "observed_exposure"]
        ]
        .sort_values("observed_exposure", ascending=False)
        .head(10)
    )

    # Identificar valores atípicos de la puntuación de riesgo
    score_outliers = analyzer.detect_outliers(
        df_clean[1],
        "score"
    )

    print("\nValores atípicos de la puntuación de riesgo")
    print("Límite inferior:", score_outliers["lower_limit"])
    print("Límite superior:", score_outliers["upper_limit"])
    print("Cantidad de valores atípicos:", len(score_outliers["outliers"]))

    print(
        score_outliers["outliers"][
            ["title", "score"]
        ]
        .sort_values("score", ascending=False)
    )

    visualizer = Visualizer(df_clean)

    # Distribuciones enriquecidas
    visualizer.histogram_exposure()
    visualizer.histogram_risk_score()

    # Profesiones según exposición
    visualizer.zero_exposure_professions()
    visualizer.highest_exposure_professions()

    # Profesiones según riesgo
    visualizer.lowest_risk_professions()
    visualizer.highest_risk_professions()

    # Relaciones entre variables
    visualizer.correlation_matrix()

    # Valores atípicos
    visualizer.boxplot_exposure()
    visualizer.boxplot_risk_score()

if __name__ == "__main__":
    main()