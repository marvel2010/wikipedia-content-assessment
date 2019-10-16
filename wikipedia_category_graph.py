import wikipediaapi
import networkx as nx


class WikipediaCategoryGraph:

    def __init__(self, category_name):
        self.wikipedia_api = wikipediaapi.Wikipedia('en')
        self.category_name = category_name
        self.graph = nx.DiGraph()

    def construct_graph(self, depth):
        self._construct_graph_nodes(depth)
        self._construct_graph_edges()

    def print_node_information(self):
        ratings_count = {}
        print("Number of Nodes: %s" % len(self.graph.nodes))
        for node in self.graph.nodes:
            rating = self.graph.nodes[node]["rating"]
            # print("\t", node.encode(), rating)
            ratings_count[rating] = ratings_count.get(rating, 0) + 1
        print("Ratings Distribution:")
        for rating in sorted(ratings_count.keys()):
            print("\tRating %s: %s" % (rating, ratings_count[rating]))

    def print_edge_information(self):
        ratings_pair_count = {}
        print("Number of Arcs: %s" % len(self.graph.edges))
        for edge in self.graph.edges:
            # print("\t", edge[0].encode(), edge[1].encode())
            rating_pair = (self.graph.nodes[edge[0]]["rating"], self.graph.nodes[edge[1]]["rating"])
            ratings_pair_count[rating_pair] = ratings_pair_count.get(rating_pair, 0) + 1
        print("Ratings Distribution:")
        for rating_pair in sorted(ratings_pair_count.keys()):
            print("\tArcs %s: %s" % (rating_pair, ratings_pair_count[rating_pair]))

    def graph_to_file(self):
        for number, node in enumerate(self.graph.nodes):
            self.graph.nodes[node]["number"] = number
        print("Nodes")
        for node in self.graph.nodes:
            print(self.graph.nodes[node]["number"], self.graph.nodes[node]["rating"])
        print("Edges")
        for edge in self.graph.edges:
            print(self.graph.nodes[edge[0]]["number"], self.graph.nodes[edge[1]]["number"])

    def extract_wikipedia_rating(self, article_title):
        """Determines the rating of the wikipedia article.

        Note that this function greedily finds the first project which has
            assigned a rating to the article. Do not use this if you would
            like an article's rating only from a specific wikipedia project.

        Returns:
            rating: 0, 1, 2, 3, 4, 5, or 6. If no rating is found, then -1.
        """
        article_talk_page = self.wikipedia_api.page("Talk:%s" % article_title)
        categories = article_talk_page.categories.keys()
        for category in categories:
            if "FA-Class" in category:
                return 6
            elif "A-Class" in category:
                return 5
            elif "GA-Class" in category:
                return 4
            elif "B-Class" in category:
                return 3
            elif "C-Class" in category:
                return 2
            elif "Start-Class" in category:
                return 1
            elif "Stub-Class" in category:
                return 0
            else:
                continue
        return -1

    def _construct_graph_nodes(self, depth):
        category_page = self.wikipedia_api.page("Category:%s" % self.category_name)
        self._construct_graph_nodes_helper(category_page.categorymembers, depth_remaining=depth)

    def _construct_graph_nodes_helper(self, category_members, depth_remaining=1):
        for c in category_members.values():
            if c.ns == wikipediaapi.Namespace.MAIN:
                # add node
                self.graph.add_node(c.title, rating=self.extract_wikipedia_rating(c.title))
            elif c.ns == wikipediaapi.Namespace.CATEGORY and depth_remaining:
                # recurse
                self._construct_graph_nodes_helper(c.categorymembers, depth_remaining=depth_remaining-1)
            else:
                continue

    def _construct_graph_edges(self):
        nodes_set = set(self.graph.nodes)
        for article in self.graph.nodes():
            article_page = self.wikipedia_api.page(article)
            article_links = article_page.links.keys()
            for linked_article in article_links:
                if linked_article in nodes_set:
                    self.graph.add_edge(article, linked_article)
