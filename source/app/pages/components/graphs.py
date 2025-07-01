import flet as ft
import io
import base64
from .graph_component import graph_component


def render_mst_graph_image(graph_matrix, mst_matrix=None):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    import networkx as nx

    G = nx.Graph()
    n = len(graph_matrix)
    G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i+1, n):
            weight = graph_matrix[i][j]
            if weight:
                G.add_edge(i, j, weight=weight)
    mst_edges = set()
    if mst_matrix is not None and len(mst_matrix) == n:
        for i in range(n):
            for j in range(i+1, n):
                if j < len(mst_matrix[i]) and mst_matrix[i][j]:
                    mst_edges.add((i, j))
    plt.figure(figsize=(3,2))
    pos = nx.spring_layout(G)
    if mst_matrix is not None and len(mst_matrix) == n:
        normal_edges = [e for e in G.edges if e not in mst_edges]
        nx.draw_networkx_edges(G, pos, edgelist=normal_edges, edge_color='gray')
        nx.draw_networkx_edges(G, pos, edgelist=list(mst_edges), edge_color='red', width=2)
    else:
        nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray')
    nx.draw_networkx_nodes(G, pos, node_color='skyblue')
    nx.draw_networkx_labels(G, pos)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64

def render_fitness_plot(fitness_history):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    buf = io.BytesIO()
    plt.figure(figsize=(3,2))
    plt.plot(fitness_history, marker='o')
    plt.xlabel('Поколение')
    plt.ylabel('Вес МОД')
    plt.title('Динамика веса МОД по поколениям')
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64

def graphs(page: ft.Page, *args, full_width=False) -> ft.Container:
    """
    Компонент главной страницы с графиками
    """
    graph = None
    images = []
    if args and not isinstance(args[0], ft.Image):
        graph = args[0]
        images = args[1:]
    else:
        images = args

    controls = []
    if graph is not None:
        col = {"sm": 12} if full_width else {"sm": 4}
        controls.append(graph_component(page, graph, col=col, cache_original=True))
    for plot in images:
        col = {"sm": 4}
        controls.append(graph_component(page, plot, col=col))

    return ft.Container(
        ft.ResponsiveRow(
            controls=controls,
            spacing=10,
            alignment=ft.alignment.center,
        ),
        col={"sm": 12},
        bgcolor="#F1F1F1",
        border_radius=30,
        expand=2,
        alignment=ft.alignment.center,
        padding=10,
    )