import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np


def plot_error_band(data : pd.DataFrame, scenarios : list[str], column : str, xstep : int,
                    xlabel : str, ylabel : str, title : str, path : str):
    fig, ax = plt.subplots()
    for sce in scenarios:
        tmp_df = data[data["scenario"] == sce]
        tmp_df.reset_index(inplace=True)

        bin_ranges = np.arange(0, tmp_df.shape[0], xstep)
        tmp_df = tmp_df[[column]].groupby(pd.cut(tmp_df.index, bin_ranges)).agg(['mean', 'std'])
        tmp_df.reset_index(inplace=True)
        tmp_df.columns = [f"{x[0]}_{x[1]}" for x in tmp_df.columns]

        ax.plot(bin_ranges[:-1],  
                        tmp_df[f'{column}_mean'], label=sce)

        ax.fill_between(bin_ranges[:-1], tmp_df[f'{column}_mean'] - tmp_df[f'{column}_std'], 
                        tmp_df[f'{column}_mean'] + tmp_df[f'{column}_std'], alpha=0.2)

    ax.legend()
    ax.set_xlim(xmin=0, xmax=bin_ranges[-1])
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    fig.savefig(path, dpi=240, bbox_inches="tight")

def run(opt):
    sns.set_theme("notebook")
    stats_df = pd.DataFrame()
    scenarios = []
    for id, stats_path in opt["stats_files"]:
        df = pd.read_csv(stats_path, sep=",")
        df.loc[:, "scenario"] = id
        scenarios.append(id)
        stats_df = pd.concat([stats_df, df], ignore_index=True)

    stats_df["city_co2"] /= 1000
    plot_error_band(stats_df, scenarios, "city_co2",
                    xstep=50, xlabel="Step", ylabel="CO2 Emission (g)",
                    title="CO2 Emissions (city)", path="stats/co2_emissions_city.png")

    stats_df["global_co2"] /= 1000
    plot_error_band(stats_df, scenarios, "global_co2",
                    xstep=50, xlabel="Step", ylabel="CO2 Emission (g)",
                    title="CO2 Emissions (global)", path="stats/co2_emissions_global.png")

    # Active Vehicles
    fig, ax = plt.subplots()
    sns.lineplot(data=stats_df, x="step", y="active_vehicles", hue="scenario", ax=ax)
    ax.set_xlabel("Step")
    ax.set_ylabel("Active Vehicles")
    ax.set_title("Active Vehicles")
    fig.savefig("stats/active_vehicles.png", dpi=240, bbox_inches="tight")

    plt.clf()

    # Average Travel Time
    fig, ax = plt.subplots()
    sns.lineplot(data=stats_df, x="step", y="avg_travel_time", hue="scenario", ax=ax)
    ax.set_xlabel("Step")
    ax.set_ylabel("Travel Time (s)")
    ax.set_title("Average Travel Time (global)")
    fig.savefig("stats/avg_travel_time.png", dpi=240, bbox_inches="tight")

    plt.clf()

    # Average Waiting Time
    fig, ax = plt.subplots()
    sns.lineplot(data=stats_df, x="step", y="avg_waiting_time", hue="scenario", ax=ax)
    ax.set_yscale("symlog")
    ax.set_xlabel("Step")
    ax.set_ylabel("Travel Time")
    ax.set_title("Average Waiting Time (global)")
    fig.savefig("stats/avg_waiting_time.png", dpi=240, bbox_inches="tight")

    plt.clf()

    # Average Halt Count
    fig, ax = plt.subplots()
    sns.lineplot(data=stats_df, x="step", y="halt_count", hue="scenario", ax=ax)
    ax.set_xlabel("Step")
    ax.set_ylabel("Halt Count")
    ax.set_title("Halted Vehicles (global)")
    fig.savefig("stats/halt_count.png", dpi=240, bbox_inches="tight")

    plt.clf()

    # Tolls Profit
    fig, ax = plt.subplots()
    sns.lineplot(data=stats_df, x="step", y="tolls_profit", hue="scenario", ax=ax)
    ax.set_xlabel("Step")
    ax.set_ylabel("Profit (€)")
    ax.set_title("Profit gained from tolls (global)")
    fig.savefig("stats/tolls_profit.png", dpi=240, bbox_inches="tight")

    plt.clf()

    stats_table = dict()
    for scenario in scenarios:
        tmp = stats_df[stats_df["scenario"] == scenario]
        stats_table[scenario] = [tmp["city_co2"].sum(), tmp["global_co2"].sum()]

    stats_df.to_latex("stats/table.tex", index=False)

    total = pd.DataFrame()


def parse_opt():
    parser = argparse.ArgumentParser()

    def stats_file(arg):
        return arg.split(",")

    parser.add_argument("--stats-files", type=stats_file, required=True, nargs="+")
    args = parser.parse_args()
    return vars(args)

if __name__ == "__main__":
    opt = parse_opt()
    run(opt)