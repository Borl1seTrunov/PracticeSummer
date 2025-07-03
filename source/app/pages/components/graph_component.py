import flet as ft
import io
import base64
import math

import plotly.graph_objects as go
import networkx as nx

def grid_layout(n):
    """
    Размещает n вершин на квадратной сетке.
    """
    side = math.ceil(math.sqrt(n))
    spacing = 1.0
    pos = {}
    for idx in range(n):
        row = idx // side
        col = idx % side
        pos[idx] = (col * spacing, -row * spacing)
    return pos

def render_graph_image(graph_matrix):
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
    plt.figure(figsize=(10, 7))
    pos = grid_layout(n)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray')
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
    plt.figure(figsize=(6, 3))
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

def plotly_graph_html(graph_matrix):
    G = nx.Graph()
    n = len(graph_matrix)
    G.add_nodes_from(range(n))
    for i in range(n):
        for j in range(i+1, n):
            weight = graph_matrix[i][j]
            if weight:
                G.add_edge(i, j, weight=weight)
    pos = nx.spring_layout(G, seed=42)
    edge_x = []
    edge_y = []
    for edge in G.edges():
        x0, y0 = pos[edge[0]]
        x1, y1 = pos[edge[1]]
        edge_x += [x0, x1, None]
        edge_y += [y0, y1, None]
    edge_trace = go.Scatter(
        x=edge_x, y=edge_y,
        line=dict(width=2, color='#888'),
        hoverinfo='none',
        mode='lines')
    node_x = []
    node_y = []
    for node in G.nodes():
        x, y = pos[node]
        node_x.append(x)
        node_y.append(y)
    node_trace = go.Scatter(
        x=node_x, y=node_y,
        mode='markers+text',
        hoverinfo='text',
        marker=dict(
            showscale=False,
            color='skyblue',
            size=30,
            line_width=2),
        text=[str(i) for i in G.nodes()],
        textposition="middle center"
    )
    fig = go.Figure(data=[edge_trace, node_trace],
                    layout=go.Layout(
                        showlegend=False,
                        hovermode='closest',
                        margin=dict(t=0, b=0, l=0, r=0),
                        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
                        autosize=True,
                        width=None, height=None
                    ))
    return fig.to_html(full_html=False)

def is_adjacency_matrix(obj):
    return (
        isinstance(obj, list) and
        all(isinstance(row, list) and len(row) == len(obj) for row in obj)
    )

def is_weight_history(obj):
    return (
        isinstance(obj, list) and
        all(isinstance(x, (int, float)) for x in obj) and len(obj) > 1
    )

def graph_component(page: ft.Page, graph_or_image, size: int = 4, col=None, cache_original=False) -> ft.Container:
    """
    Компонент графика (matplotlib + ft.Image)
    """
    if isinstance(graph_or_image, ft.Image):
        content = graph_or_image
    elif is_adjacency_matrix(graph_or_image):
        if cache_original:
            if not hasattr(page, "_original_graph_img_base64") or getattr(page, "_original_graph_img_graph_id", None) != id(graph_or_image):
                img_base64 = render_graph_image(graph_or_image)
                page._original_graph_img_base64 = img_base64
                page._original_graph_img_graph_id = id(graph_or_image)
            else:
                img_base64 = page._original_graph_img_base64
        else:
            if not hasattr(page, "_graph_img_base64") or getattr(page, "_graph_img_graph_id", None) != id(graph_or_image):
                img_base64 = render_graph_image(graph_or_image)
                page._graph_img_base64 = img_base64
                page._graph_img_graph_id = id(graph_or_image)
            else:
                img_base64 = page._graph_img_base64
        content = ft.Image(src_base64=img_base64, expand=True)
    elif is_weight_history(graph_or_image):
        img_base64 = render_fitness_plot(graph_or_image)
        content = ft.Image(src_base64=img_base64, expand=True)
    else:
        content = ft.Container(expand=True)
    return ft.Container(
        content=content,
        col=col if col else {"sm": size, "xs": 12},
        expand=True
    )

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
    plt.figure(figsize=(20, 12))
    pos = grid_layout(n)
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