import argparse
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def run(opt):
    sns.set_theme("notebook")
    stats_df = pd.DataFrame()
    for id, stats_path in opt["stats_files"]:
        df = pd.read_csv(stats_path, sep=",")
        df.loc[:, "scenario"] = id

        stats_df = pd.concat([stats_df, df], ignore_index=True)
    
    # City CO2 Emissions
    fig, ax = plt.subplots()
    stats_df["city_co2"] /= 1000
    sns.lineplot(data=stats_df, x="step", y="city_co2", hue="scenario", ax=ax)
    ax.set_xlabel("Step")
    ax.set_ylabel("CO2 Emission (g)")
    ax.set_title("CO2 Emissions (city)")
    fig.savefig("stats/co2_emissions_city.png", dpi=240, bbox_inches="tight")

    plt.clf()

    # Global CO2 Emissions
    fig, ax = plt.subplots()
    stats_df["global_co2"] /= 1000
    sns.lineplot(data=stats_df, x="step", y="global_co2", hue="scenario", ax=ax)
    ax.set_xlabel("Step")
    ax.set_ylabel("CO2 Emission (g)")
    ax.set_title("CO2 Emissions (global)")
    fig.savefig("stats/co2_emissions_global.png", dpi=240, bbox_inches="tight")

    plt.clf()

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