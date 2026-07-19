import matplotlib.pyplot as plt


class Visualizer:
    def __init__(self, dataframeList):
        self.dataframeList = dataframeList

    def histogram_exposure(self):
        df_anthropic = self.dataframeList[0]

        plt.figure(figsize=(8, 5))

        plt.hist(
            df_anthropic["observed_exposure"],
            bins=10,
            color="cornflowerblue",
            edgecolor="black"
        )

        plt.title("Distribución de la exposición laboral observada a la IA")
        plt.xlabel("Exposición observada")
        plt.ylabel("Cantidad de profesiones")
        plt.grid(axis="y", alpha=0.3)

        plt.tight_layout()
        plt.show()

    def histogram_risk_score(self):
        df_meritforge = self.dataframeList[1]

        plt.figure(figsize=(8, 5))

        plt.hist(
            df_meritforge["score"],
            bins=10,
            color="lightcoral",
            edgecolor="black"
        )

        plt.title("Distribución del índice de amenaza profesional")
        plt.xlabel("Puntuación de riesgo")
        plt.ylabel("Cantidad de profesiones")
        plt.grid(axis="y", alpha=0.3)

        plt.tight_layout()
        plt.show()

    def boxplot_exposure(self):
        # El DataFrame 1 corresponde al dataset de Anthropic
        df_anthropic = self.dataframeList[0]

        plt.figure(figsize=(8, 5))

        plt.boxplot(
            df_anthropic["observed_exposure"],
            vert=False,
            patch_artist=True,
            boxprops=dict(facecolor="lightblue"),
            medianprops=dict(color="darkblue", linewidth=2)
        )

        plt.title("Valores de exposición laboral observada a la IA")
        plt.xlabel("Exposición observada")
        plt.yticks([1], ["Profesiones"])
        plt.grid(axis="x", alpha=0.3)

        plt.tight_layout()
        plt.show()

    def boxplot_risk_score(self):
        # El DataFrame 2 corresponde al dataset de MeritForge
        df_meritforge = self.dataframeList[1]

        plt.figure(figsize=(8, 5))

        plt.boxplot(
            df_meritforge["score"],
            vert=False,
            patch_artist=True,
            boxprops=dict(facecolor="lightcoral"),
            medianprops=dict(color="darkred", linewidth=2)
        )

        plt.title("Valores del índice de amenaza profesional")
        plt.xlabel("Puntuación de riesgo")
        plt.yticks([1], ["Profesiones"])
        plt.grid(axis="x", alpha=0.3)

        plt.tight_layout()
        plt.show()

    def correlation_matrix(self):
        # El DataFrame 2 corresponde al dataset de MeritForge
        df_meritforge = self.dataframeList[1]

        selected_columns = [
            "score",
            "salary.low",
            "salary.high",
            "historicalscores.q1_2025",
            "historicalscores.q3_2025",
            "historicalscores.q1_2026",
            "historicalscores.q2_2026"
        ]

        correlation = df_meritforge[selected_columns].corr()

        labels = [
            "Riesgo",
            "Salario mínimo",
            "Salario máximo",
            "Riesgo T1-2025",
            "Riesgo T3-2025",
            "Riesgo T1-2026",
            "Riesgo T2-2026"
        ]

        plt.figure(figsize=(10, 8))

        image = plt.imshow(
            correlation,
            cmap="coolwarm",
            vmin=-1,
            vmax=1
        )

        plt.colorbar(image, label="Correlación")

        plt.xticks(
            range(len(labels)),
            labels,
            rotation=45,
            ha="right"
        )

        plt.yticks(
            range(len(labels)),
            labels
        )

        for row in range(len(correlation)):
            for column in range(len(correlation)):
                plt.text(
                    column,
                    row,
                    f"{correlation.iloc[row, column]:.2f}",
                    ha="center",
                    va="center",
                    color="black"
                )

        plt.title("Matriz de correlación de variables laborales")
        plt.tight_layout()
        plt.show()