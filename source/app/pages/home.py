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
            graph[i][j] = edge
            graph[j][i] = edge
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

    return ft.View(
        "/",
        controls=[
            page_layer(
                page=page, 
                content_page=ft.Column(
                    controls=[
                        graphs(page, graph),
                        work_component(page),
                    ],
                    expand=True,
                    spacing=0,
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                )
            )
        ],
        padding=0
    )