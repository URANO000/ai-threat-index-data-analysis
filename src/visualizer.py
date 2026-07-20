import matplotlib.pyplot as plt
from textwrap import fill
import numpy as np

class Visualizer:
    def __init__(self, dataframeList):
        self.dataframeList = dataframeList

    def histogram_risk_score(self):
        df_meritforge = self.dataframeList[1]

        q1 = df_meritforge["score"].quantile(0.25)
        q3 = df_meritforge["score"].quantile(0.75)

        lowest_professions = df_meritforge.nsmallest(3, "score")
        highest_professions = df_meritforge.nlargest(3, "score")

        figure, axis = plt.subplots(figsize=(10, 7))

        frequencies, limits, bars = axis.hist(
            df_meritforge["score"],
            bins=10,
            edgecolor="black"
        )

        # Colorear los intervalos bajos, intermedios y altos
        for bar, lower, upper in zip(bars, limits[:-1], limits[1:]):
            center = (lower + upper) / 2

            if center <= q1:
                bar.set_facecolor("seagreen")
            elif center >= q3:
                bar.set_facecolor("indianred")
            else:
                bar.set_facecolor("cornflowerblue")

        axis.axvline(
            q1,
            color="darkgreen",
            linestyle="--",
            label=f"Primer cuartil: {q1:.2f}"
        )

        axis.axvline(
            q3,
            color="darkred",
            linestyle="--",
            label=f"Tercer cuartil: {q3:.2f}"
        )

        lowest_text = "\n".join(
            f"{row['title']}: {row['score']}"
            for _, row in lowest_professions.iterrows()
        )

        highest_text = "\n".join(
            f"{row['title']}: {row['score']}"
            for _, row in highest_professions.iterrows()
        )

        axis.text(
            0.02,
            0.97,
            "Menor riesgo\n" + lowest_text,
            transform=axis.transAxes,
            va="top",
            bbox=dict(
                boxstyle="round",
                facecolor="honeydew",
                edgecolor="seagreen"
            )
        )

        axis.text(
            0.98,
            0.97,
            "Mayor riesgo\n" + highest_text,
            transform=axis.transAxes,
            va="top",
            ha="right",
            bbox=dict(
                boxstyle="round",
                facecolor="mistyrose",
                edgecolor="indianred"
            )
        )

        axis.set_title(
            "Distribución del riesgo de desplazamiento por IA"
        )
        axis.set_xlabel("Puntuación de riesgo")
        axis.set_ylabel("Cantidad de profesiones")
        axis.grid(axis="y", alpha=0.3)
        axis.legend(loc="upper center")

        plt.tight_layout()
        plt.show()


    def histogram_exposure(self):
        df_anthropic = self.dataframeList[0]

        q1 = df_anthropic["observed_exposure"].quantile(0.25)
        q3 = df_anthropic["observed_exposure"].quantile(0.75)
        iqr = q3 - q1
        upper_limit = q3 + 1.5 * iqr

        zero_count = (
            df_anthropic["observed_exposure"] == 0
        ).sum()

        highest_professions = df_anthropic.nlargest(
            3,
            "observed_exposure"
        )

        figure, axis = plt.subplots(figsize=(10, 7))

        frequencies, limits, bars = axis.hist(
            df_anthropic["observed_exposure"],
            bins=10,
            edgecolor="black"
        )

        # Diferenciar exposición nula, habitual y atípicamente alta
        for position, (bar, lower) in enumerate(
            zip(bars, limits[:-1])
        ):
            if position == 0:
                bar.set_facecolor("seagreen")
            elif lower >= upper_limit:
                bar.set_facecolor("indianred")
            else:
                bar.set_facecolor("cornflowerblue")

        axis.axvline(
            upper_limit,
            color="darkred",
            linestyle="--",
            label=f"Límite de valores atípicos: {upper_limit:.4f}"
        )

        highest_text = "\n".join(
            f"{row['title']}: {row['observed_exposure']:.4f}"
            for _, row in highest_professions.iterrows()
        )

        axis.text(
            0.98,
            0.97,
            "Mayor exposición\n" + highest_text,
            transform=axis.transAxes,
            va="top",
            ha="right",
            bbox=dict(
                boxstyle="round",
                facecolor="mistyrose",
                edgecolor="indianred"
            )
        )

        axis.text(
            0.58,
            0.72,
            f"Profesiones con exposición nula: {zero_count}",
            transform=axis.transAxes,
            bbox=dict(
                boxstyle="round",
                facecolor="honeydew",
                edgecolor="seagreen"
            )
        )

        axis.set_title(
            "Distribución de la exposición laboral observada a la IA"
        )
        axis.set_xlabel("Exposición observada")
        axis.set_ylabel("Cantidad de profesiones")
        axis.grid(axis="y", alpha=0.3)
        axis.legend()

        plt.tight_layout()
        plt.show()  


    def correlation_matrix(self):
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

        labels = [
            "Riesgo",
            "Salario mínimo",
            "Salario máximo",
            "Riesgo T1-2025",
            "Riesgo T3-2025",
            "Riesgo T1-2026",
            "Riesgo T2-2026"
        ]

        correlation = df_meritforge[selected_columns].corr()

        # Ocultar la mitad superior porque repite los mismos valores
        mask = np.triu(
            np.ones_like(correlation, dtype=bool),
            k=1
        )

        masked_correlation = np.ma.array(
            correlation,
            mask=mask
        )

        color_map = plt.cm.coolwarm.copy()
        color_map.set_bad("white")

        figure, axis = plt.subplots(figsize=(9, 8))

        image = axis.imshow(
            masked_correlation,
            cmap=color_map,
            vmin=-1,
            vmax=1
        )

        axis.set_xticks(range(len(labels)))
        axis.set_xticklabels(
            labels,
            rotation=45,
            ha="right"
        )

        axis.set_yticks(range(len(labels)))
        axis.set_yticklabels(labels)

        for row in range(len(correlation)):
            for column in range(len(correlation)):
                if not mask[row, column]:
                    value = correlation.iloc[row, column]

                    text_color = (
                        "white"
                        if abs(value) >= 0.65
                        else "black"
                    )

                    axis.text(
                        column,
                        row,
                        f"{value:.2f}",
                        ha="center",
                        va="center",
                        color=text_color
                    )

        figure.colorbar(
            image,
            ax=axis,
            label="Correlación",
            shrink=0.85
        )

        axis.set_title(
            "Relaciones entre riesgo, salarios y valores históricos"
        )

        plt.tight_layout()
        plt.show()


    def boxplot_exposure(self):
        df_anthropic = self.dataframeList[0]

        q1 = df_anthropic["observed_exposure"].quantile(0.25)
        q3 = df_anthropic["observed_exposure"].quantile(0.75)
        iqr = q3 - q1

        upper_limit = q3 + 1.5 * iqr

        outliers = df_anthropic[
            df_anthropic["observed_exposure"] > upper_limit
        ]

        figure, axis = plt.subplots(figsize=(9, 5))

        axis.boxplot(
            df_anthropic["observed_exposure"],
            vert=False,
            patch_artist=True,
            boxprops=dict(facecolor="lightblue"),
            medianprops=dict(color="darkblue", linewidth=2),
            flierprops=dict(
                marker="o",
                markerfacecolor="indianred",
                markeredgecolor="darkred",
                alpha=0.7
            )
        )

        axis.axvline(
            upper_limit,
            color="darkred",
            linestyle="--",
            label=f"Límite superior: {upper_limit:.4f}"
        )

        axis.text(
            0.98,
            0.88,
            f"Valores atípicos: {len(outliers)}",
            transform=axis.transAxes,
            ha="right",
            bbox=dict(
                boxstyle="round",
                facecolor="mistyrose",
                edgecolor="indianred"
            )
        )

        axis.set_title(
            "Valores atípicos de exposición laboral observada"
        )
        axis.set_xlabel("Exposición observada")
        axis.set_yticks([1])
        axis.set_yticklabels(["Profesiones"])
        axis.grid(axis="x", alpha=0.3)
        axis.legend()

        plt.tight_layout()
        plt.show()

    def boxplot_risk_score(self):
        df_meritforge = self.dataframeList[1]

        q1 = df_meritforge["score"].quantile(0.25)
        q3 = df_meritforge["score"].quantile(0.75)
        iqr = q3 - q1

        lower_limit = q1 - 1.5 * iqr
        upper_limit = q3 + 1.5 * iqr

        outliers = df_meritforge[
            (df_meritforge["score"] < lower_limit) |
            (df_meritforge["score"] > upper_limit)
        ]

        figure, axis = plt.subplots(figsize=(9, 5))

        axis.boxplot(
            df_meritforge["score"],
            vert=False,
            patch_artist=True,
            boxprops=dict(facecolor="lightcoral"),
            medianprops=dict(color="darkred", linewidth=2),
            flierprops=dict(
                marker="o",
                markerfacecolor="indianred",
                markeredgecolor="darkred"
            )
        )

        axis.axvline(
            lower_limit,
            color="darkgreen",
            linestyle="--",
            label=f"Límite inferior: {lower_limit:.2f}"
        )

        axis.axvline(
            upper_limit,
            color="darkred",
            linestyle="--",
            label=f"Límite superior: {upper_limit:.2f}"
        )

        axis.text(
            0.98,
            0.88,
            f"Valores atípicos: {len(outliers)}",
            transform=axis.transAxes,
            ha="right",
            bbox=dict(
                boxstyle="round",
                facecolor="honeydew",
                edgecolor="seagreen"
            )
        )

        axis.set_title(
            "Valores atípicos del índice de amenaza profesional"
        )
        axis.set_xlabel("Puntuación de riesgo")
        axis.set_yticks([1])
        axis.set_yticklabels(["Profesiones"])
        axis.grid(axis="x", alpha=0.3)
        axis.legend()

        plt.tight_layout()
        plt.show()

    def zero_exposure_professions(self):
        df_anthropic = self.dataframeList[0]

        zero_professions = (
            df_anthropic[
                df_anthropic["observed_exposure"] == 0
            ]
            .sort_values("title")
            .head(10)
        )

        zero_count = (
            df_anthropic["observed_exposure"] == 0
        ).sum()

        labels = zero_professions["title"].map(
            lambda title: fill(title, 42)
        )

        figure, axis = plt.subplots(figsize=(9, 7))

        axis.scatter(
            zero_professions["observed_exposure"],
            labels,
            color="seagreen",
            s=100,
            edgecolor="black"
        )

        axis.set_title(
            "Ejemplos de profesiones con exposición nula\n"
            f"Total de profesiones con exposición nula: {zero_count}"
        )
        axis.set_xlabel("Exposición observada")
        axis.set_xlim(-0.01, 0.05)
        axis.grid(axis="x", alpha=0.3)

        plt.tight_layout()
        plt.show()


    def highest_exposure_professions(self):
        df_anthropic = self.dataframeList[0]

        highest_exposure = (
            df_anthropic
            .nlargest(10, "observed_exposure")
            .sort_values("observed_exposure")
        )

        labels = highest_exposure["title"].map(
            lambda title: fill(title, 42)
        )

        figure, axis = plt.subplots(figsize=(10, 7))

        bars = axis.barh(
            labels,
            highest_exposure["observed_exposure"],
            color="indianred",
            edgecolor="black"
        )

        axis.set_title(
            "Diez profesiones con mayor exposición observada a la IA"
        )
        axis.set_xlabel("Exposición observada")
        axis.set_xlim(0, 0.85)
        axis.grid(axis="x", alpha=0.3)

        axis.bar_label(
            bars,
            fmt="%.4f",
            padding=3
        )

        plt.tight_layout()
        plt.show()

    def lowest_risk_professions(self):
        df_meritforge = self.dataframeList[1]

        lowest_risk = (
            df_meritforge
            .nsmallest(10, "score")
            .sort_values("score", ascending=False)
        )

        figure, axis = plt.subplots(figsize=(9, 7))

        bars = axis.barh(
            lowest_risk["title"],
            lowest_risk["score"],
            color="seagreen",
            edgecolor="black"
        )

        axis.set_title(
            "Diez profesiones con menor riesgo de desplazamiento"
        )
        axis.set_xlabel("Puntuación de riesgo")
        axis.set_xlim(0, 100)
        axis.grid(axis="x", alpha=0.3)
        axis.bar_label(bars, padding=3)

        plt.tight_layout()
        plt.show()

    def highest_risk_professions(self):
        df_meritforge = self.dataframeList[1]

        highest_risk = (
            df_meritforge
            .nlargest(10, "score")
            .sort_values("score")
        )

        figure, axis = plt.subplots(figsize=(9, 7))

        bars = axis.barh(
            highest_risk["title"],
            highest_risk["score"],
            color="indianred",
            edgecolor="black"
        )

        axis.set_title(
            "Diez profesiones con mayor riesgo de desplazamiento"
        )
        axis.set_xlabel("Puntuación de riesgo")
        axis.set_xlim(0, 100)
        axis.grid(axis="x", alpha=0.3)
        axis.bar_label(bars, padding=3)

        plt.tight_layout()
        plt.show()