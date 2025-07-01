import flet as ft
import random
from typing import List

from .components.page_layer import page_layer
from .components.graphs import graphs
from .components.work_component import work_component

def generate_random_graph(num_vertices: int = 6) -> List[List[int]]:
    graph = [[0]*num_vertices for _ in range(num_vertices)]
    for i in range(num_vertices):
        for j in range(i+1, num_vertices):
            edge = random.choice([0, 1])
            if edge:
                weight = random.randint(1, 10)
                graph[i][j] = weight
                graph[j][i] = weight
            else:
                graph[i][j] = 0
                graph[j][i] = 0
    return graph

def home_view(page: ft.Page) -> ft.View:
    """
    Страница с работой алгоритма
    """

    if not hasattr(page, "current_graph"):
        vertex_count: int = 6
        if hasattr(page, "params"):
            try:
                vertex_count = int(page.params.get("vertex_count", 6))
            except Exception:
                vertex_count = 6
        else:
            vertex_count = 6
        page.current_graph = generate_random_graph(num_vertices=vertex_count)

    graph = page.current_graph

    if not hasattr(page, "graphs_container"):
        page.graphs_container = ft.Container()
    page.graphs_container.content = graphs(
        page,
        graph,
        getattr(page, 'mst_graph', None),
        getattr(page, 'mst_weights_history', None)
    )

    return ft.View(
        "/",
        controls=[
            page_layer(
                page=page, 
                content_page=ft.Column(
                    controls=[
                        ft.Container(
                            content=page.graphs_container,
                            expand=1,
                            padding=20
                        ),
                        ft.Container(
                            content=work_component(page),
                            expand=1,
                            padding=20,
                            bgcolor=ft.Colors.TRANSPARENT
                        ),
                    ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.START,
                )
            )
        ],
        padding=0
    )