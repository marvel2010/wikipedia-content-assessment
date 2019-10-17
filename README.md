# Wikipedia Content Assessment

### Goal

The goal of this project is to analyze the structure of the Wikipedia graph with respect to content quality. We conjecture that high-quality articles are disproportionaly less likely to link to low-quality articles. If this is true, then information about the Wikipedia graph may be very helpful in predicting the quality of an article, an interesting Machine Learning task.

### Content

Wikipedia articles are assessed by WikiProjects according the Content assessment guidelines. The content assessment guidelines put content into one of seven categories: FA, A, GA, B, C, Start, Stub.

See [this Wikipedia page](https://en.wikipedia.org/wiki/Wikipedia:Content_assessment) for more details.

### Graph Structure

We represent all the articles in a given category as a graph. The vertices of the graph are the articles and an arc represent a link from one article to another.

We use the python package NetworkX to represent these graphs.

### Example

```python
from wikipedia_category_graph import WikipediaCategoryGraph
wikipedia_cat_graph_class_egt = WikipediaCategoryGraph("Extremal graph theory")

wikipedia_cat_graph_class_egt.construct_graph(depth=1)
wikipedia_cat_graph_class_egt.print_node_information()
wikipedia_cat_graph_class_egt.print_edge_information()
wikipedia_cat_graph_class_egt.graph_to_file("Extremal_graph_theory-depth1-full.txt")
```