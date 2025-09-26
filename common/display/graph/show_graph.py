import networkx as nx

from ipywidgets import Output
from ipycytoscape import CytoscapeWidget
from IPython.display import display, clear_output

from common.logger import get_logger
from common.utils.json_data import get_pretty


out = Output()
logger = get_logger(__name__)


def log_clicks(node: dict):
    with out:
        clear_output()

        node_data = node["data"]
        logger.info(get_pretty(node_data))


def show_graph(
    graph: nx.DiGraph,
    style: dict,
    layout: str = "cola",
    # NOTE: https://blog.js.cytoscape.org/2020/05/11/layouts
):
    cytoscapeobj = CytoscapeWidget()
    cytoscapeobj.graph.add_graph_from_networkx(graph, directed=True)

    cytoscapeobj.set_layout(name=layout, animate=False)
    cytoscapeobj.set_style(style)
    cytoscapeobj.on(
        "node",
        "click",
        log_clicks,
    )

    display(out)
    display(cytoscapeobj)
