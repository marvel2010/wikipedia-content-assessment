from wikipedia_category_graph import WikipediaCategoryGraph
from networkx.readwrite import node_link_data
import json

CATEGORY_TITLE = "Board games"
OUTPUT_FILENAME = "results/board_games.json"

wikipedia_cat_graph_class_egt = WikipediaCategoryGraph(CATEGORY_TITLE)
wikipedia_cat_graph_class_egt.construct_graph(depth=2)
data = node_link_data(wikipedia_cat_graph_class_egt.graph)

with open(OUTPUT_FILENAME, "w") as outfile:
    json.dump(data, outfile)
