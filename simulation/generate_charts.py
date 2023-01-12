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

    ax.set_ylim(0)
    fig.savefig(path, dpi=240, bbox_inches="tight")
    plt.close(fig)
    plt.clf()

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

    stats_df["out_co2"] /= 1000
    plot_error_band(stats_df, scenarios, "out_co2",
                    xstep=50, xlabel="Step", ylabel="CO2 Emission (g)",
                    title="CO2 Emissions (out)", path="stats/co2_emissions_out.png")

    # Active Vehicles
    fig, ax = plt.subplots()
    sns.lineplot(data=stats_df, x="step", y="active_vehicles", hue="scenario", ax=ax)
    ax.set_xlabel("Step")
    ax.set_ylabel("Active Vehicles")
    ax.set_title("Active Vehicles")
    fig.savefig("stats/active_vehicles.png", dpi=240, bbox_inches="tight")
    plt.close(fig)
    plt.clf()

    # # Average Travel Time
    # fig, ax = plt.subplots()
    # sns.lineplot(data=stats_df, x="step", y="avg_travel_time", hue="scenario", ax=ax)
    # ax.set_xlabel("Step")
    # ax.set_ylabel("Travel Time (s)")
    # ax.set_title("Average Travel Time (global)")
    # fig.savefig("stats/avg_travel_time.png", dpi=240, bbox_inches="tight")

    # plt.clf()

    # plot_error_band(stats_df, scenarios, "avg_travel_time",
    #                 xstep=50, xlabel="Step", ylabel="Travel Time (s)",
    #                 title="Travel Time", path="stats/travel_time.png")

    # Average Waiting Time
    # fig, ax = plt.subplots()
    # sns.lineplot(data=stats_df, x="step", y="avg_waiting_time", hue="scenario", ax=ax)
    # ax.set_yscale("symlog")
    # ax.set_xlabel("Step")
    # ax.set_ylabel("Travel Time")
    # ax.set_title("Average Waiting Time (global)")
    # fig.savefig("stats/avg_waiting_time.png", dpi=240, bbox_inches="tight")

    # plt.clf()

    # # Average Halt Count
    # fig, ax = plt.subplots()
    # sns.lineplot(data=stats_df, x="step", y="halt_count", hue="scenario", ax=ax)
    # ax.set_xlabel("Step")
    # ax.set_ylabel("Halt Count")
    # ax.set_title("Halted Vehicles (global)")
    # fig.savefig("stats/halt_count.png", dpi=240, bbox_inches="tight")

    # plt.clf()

    # Tolls Profit
    fig, ax = plt.subplots()
    sns.lineplot(data=stats_df, x="step", y="tolls_profit", hue="scenario", ax=ax)
    ax.set_xlabel("Step")
    ax.set_ylabel("Profit (€)")
    ax.set_title("Profit gained from tolls (global)")
    fig.savefig("stats/tolls_profit.png", dpi=240, bbox_inches="tight")
    plt.close(fig)
    plt.clf()

    stats_table = {"metric" : ["CO2 (city)",  "Halt (city)", "Wait Time (city)", "Travel time (city)",
                                "Halt (out)", "Wait Time (out)", "Travel Time (out)", "CO2 (out)", "CO2 (global)"]}


    throughput_df = pd.DataFrame(columns=["index", "global", "city", "scenario"])
    fig, axs = plt.subplots(1,3)
    for idx, sce in enumerate(scenarios):
        tmp_df = stats_df[stats_df["scenario"] == sce]
        tmp_df.reset_index(inplace=True)

        bin_size = 25
        bins = np.arange(0, tmp_df.shape[0], bin_size)
        v_count_stats = tmp_df[["city_entered", "city_exited","global_entered","global_exited"]].groupby(pd.cut(tmp_df.index, bins)).agg(['sum'])
        v_count_stats.reset_index(inplace=True)
        v_count_stats.columns = [f"{x[0]}" for x in v_count_stats.columns]

        calculated = pd.DataFrame(columns=throughput_df.columns)
        calculated["index"] = bins
        calculated["global"] = v_count_stats["global_exited"] / bin_size
        calculated["city"] = v_count_stats["city_exited"] / bin_size
        calculated["scenario"] = sce

        throughput_df = pd.concat([throughput_df, calculated], axis=0)

    fig, ax = plt.subplots()
    sns.boxplot(data=throughput_df, y="global", x="scenario", ax=ax)
    ax.set_xlabel("Scenario")
    ax.set_ylabel("Global Throughput (s^-1)")
    ax.set_title("Throughput on the network (global)")
    fig.savefig("stats/global_throughput.png", dpi=240, bbox_inches="tight")
    plt.close(fig)
    plt.clf()

    # print("Throughput values")
    # print(throughput_df)
    # print(throughput_df.groupby("scenario").agg(["mean", "std"]))

    unit = 1000000.0
    for scenario in scenarios:
        tmp = stats_df[stats_df["scenario"] == scenario]
        # print(tmp.head())
        stats_table[scenario] = [
            tmp["city_co2"].sum()/unit, 
            tmp["city_halt"].mean(),
            tmp["city_wait_time"].mean(),
            tmp["city_travel_time"].mean(),
            tmp["out_halt"].mean(),
            tmp["out_wait_time"].mean(),
            tmp["out_travel_time"].mean(),
            tmp["out_co2"].sum()/unit,
            tmp["global_co2"].sum()/unit,
        ]

    total = pd.DataFrame(stats_table)

    total = total.round(2)

    # total = total.applymap(lambda x : round(x, 3) if type(x) == str else x)
    total.to_latex("stats/table.tex", index=False)


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