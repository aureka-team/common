# NOTE: https://js.cytoscape.org/#style/labels
test_style = [
    {
        "selector": "node",
        "style": {
            "font-size": "15px",
            "label": "data(name)",
            "text-valign": "center",
            "color": "white",
            "background-color": "#89ddff",
            "text-outline-width": 2,
            "text-outline-color": "#888",
        },
    },
    {
        "selector": "edge",
        "style": {
            "font-weight": "bold",
            "font-size": "10px",
            "label": "data(projects)",
            "curve-style": "bezier",
            "target-arrow-shape": "triangle",
            "text-rotation": "autorotate",
            "color": "#6E6C6F",
        },
    },
]
