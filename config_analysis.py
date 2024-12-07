import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from itertools import combinations
from collections import Counter
import networkx as nx

file_path_is = "result_configs/is_results_combined.txt"
file_path_ds = "result_configs/ds_results_combined.txt"

num_combs = 15

color_mapping = {
        "prompt": "skyblue",
        "style": "lightgreen",
        "view": "salmon"
        }

def get_feature_type(df, feature):
    if feature in df["prompts"].explode().values:
        return "prompt"
    elif feature in df["style"].unique():
        return "style"
    elif feature in df["views"].explode().values:
        return "view"
    else:
        return "unknown"


with open(file_path_is, "r") as file:
    is_lines = file.readlines()

with open(file_path_ds, "r") as file:
    ds_lines = file.readlines()

def parse_lines(lines):
    data = []
    current_entry = {}
    for line in lines:
        line = line.strip()
        if not line:
            if current_entry:
                data.append(current_entry)
                current_entry = {}
        else:
            if line.startswith("prompts:"):
                prompts = line.replace("prompts:", "").strip().split("' '")
                current_entry["prompts"] = [p.strip("'") for p in prompts]
            elif line.startswith("style:"):
                style = line.replace("style:", "").strip().strip("'")
                current_entry["style"] = style
            elif line.startswith("views:"):
                views = line.replace("views:", "").strip().split("' '")
                current_entry["views"] = [v.strip("'") for v in views]
    if current_entry:
        data.append(current_entry)
    return data

def one_hot_encode(df):
    df_exploded = df.reset_index()

    df_exploded = df_exploded.explode("prompts").explode("views")

    one_hot_df = pd.get_dummies(df_exploded, columns = ["prompts", "style", "views"])
    one_hot_df = pd.get_dummies(df_exploded, columns = ["prompts", "style", "views"])

    one_hot_df = one_hot_df.groupby('index').max()
    return one_hot_df


data_is = parse_lines(is_lines)
data_ds = parse_lines(ds_lines)

is_df = pd.DataFrame(data_is)
ds_df = pd.DataFrame(data_ds)

def visualise(df, name):
    df["feature_prompts"] = df["prompts"].apply(lambda x: list(x))
    df["feature_views"] = df["views"].apply(lambda x: [v for v in x if v != "identity"])

    df["features"] = df.apply(
        lambda row: row["feature_prompts"] + [row["style"]] + row["feature_views"], axis=1
    )

    all_features = [feature for features_list in df["features"] for feature in features_list]
    feature_counts = Counter(all_features)
    most_common_features = feature_counts.most_common()

    combinations_count = Counter()
    for features_list in df["features"]:
        for size in range(2, 5):
            combinations_count.update(combinations(features_list, size))

    most_common_combinations = combinations_count.most_common()

    G = nx.Graph()

    relevant_features = set()
    for comb, _ in most_common_combinations[:num_combs]:
        relevant_features.update(comb)

    node_sizes = {feature: count for feature, count in most_common_features if feature in relevant_features}

    node_colors = []

    for feature, size in node_sizes.items():
        feature_type = get_feature_type(df, feature)
        G.add_node(feature, size=size, feature_type=feature_type)
        node_colors.append(color_mapping[feature_type])

    for (comb, count) in most_common_combinations[:num_combs]:
        for i in range(len(comb)):
            for j in range(i + 1, len(comb)):
                G.add_edge(comb[i], comb[j], weight=count)

    min_size = 500
    max_size_scale = 3000
    scaled_sizes = [
        max(min_size, node_sizes[node] * max_size_scale / max(node_sizes.values()))
        for node in G.nodes
    ]

    pos = nx.spring_layout(G)
    plt.figure(figsize=(10, 8))
    nx.draw_networkx_nodes(G, pos, node_size=scaled_sizes, node_color=node_colors, alpha=1.0)
    # edge_widths = [G[u][v]["weight"] for u, v in G.edges]
    nx.draw_networkx_edges(G, pos, width=1.5, alpha=0.7, edge_color="gray")
    labels = {node: node.replace("_", " ") for node in G.nodes}
    nx.draw_networkx_labels(G, pos, labels, font_size=10, font_color="black", font_weight="bold")

    legend_handles = [
        plt.Line2D([0], [0], marker="o", color="w", label="prompt", markersize=10,
                   markerfacecolor=color_mapping["prompt"]),
        plt.Line2D([0], [0], marker="o", color="w", label="style", markersize=10,
                   markerfacecolor=color_mapping["style"]),
        plt.Line2D([0], [0], marker="o", color="w", label="view", markersize=10, markerfacecolor=color_mapping["view"]),
    ]
    plt.legend(handles=legend_handles, loc="upper left", title="feature types")

    plt.title("network graph of feature combinations")
    plt.axis("off")
    plt.savefig(name)

visualise(is_df, "visualisations/is_results.png")
visualise(ds_df, "visualisations/ds_results.png")
