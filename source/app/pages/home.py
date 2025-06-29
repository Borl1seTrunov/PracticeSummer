import flet as ft

from .components.page_layer import page_layer
from .components.graphs import graphs
from .components.work_component import work_component

def home_view(page: ft.Page):
    """
    Страница с работой алгоритма
    """

    plot1, plot2, plot3 = [ft.Image() for _ in range(3)]

    return ft.View(
        "/",
        controls=[
            page_layer(
                page=page, 
                content_page=ft.Column(
                    controls=[
                        graphs(page, plot1, plot2, plot3),
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