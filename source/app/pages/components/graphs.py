import flet as ft

from .graph_component import graph_component


def graphs(page : ft.Page, *args) -> ft.Container:
    """
    Компонент главной страницы с графиками
    в зависимости от количества графиков меняется размер графа на сетке
    """
    
    size_graph : int = int(12 / len(args)) 
    size_graph = size_graph if size_graph > 1 else 12

    return ft.Container(
        ft.ResponsiveRow(
            controls=[graph_component(page, plot, size_graph) for plot in args],
            spacing=10,
        ),
        col={"sm": 12},
        bgcolor="#F1F1F1",
        border_radius=30,
        expand=2,
        alignment=ft.alignment.center,
        padding=10,
    )