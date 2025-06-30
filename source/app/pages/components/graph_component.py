import flet as ft
import io
import base64

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
    plt.figure(figsize=(3,2))
    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, node_color='skyblue', edge_color='gray')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    plt.close()
    buf.seek(0)
    img_base64 = base64.b64encode(buf.read()).decode('utf-8')
    return img_base64

def graph_component(page: ft.Page, graph_or_image, size: int = 4) -> ft.Container:
    """
    Компонент графика
    """
    
    if isinstance(graph_or_image, ft.Image):
        content = graph_or_image
    elif isinstance(graph_or_image, list):
        if not hasattr(page, "_graph_img_base64") or getattr(page, "_graph_img_graph_id", None) != id(graph_or_image):
            img_base64 = render_graph_image(graph_or_image)
            page._graph_img_base64 = img_base64
            page._graph_img_graph_id = id(graph_or_image)
        else:
            img_base64 = page._graph_img_base64
        content = ft.Image(src_base64=img_base64, width=300, height=200)
    else:
        content = ft.Container()

    return ft.Container(
        content=ft.Card(
            content=ft.Container(
                content,
                padding=10,
            ),
            elevation=5,
            color=ft.colors.WHITE,
            surface_tint_color=ft.colors.WHITE,
        ),
        col={"sm": size, "xs": 12},
        padding=5,
    )