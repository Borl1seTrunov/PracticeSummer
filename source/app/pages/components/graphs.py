import flet as ft

from .graph_component import graph_component


def graphs(page : ft.Page, *args) -> ft.Container:
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
        controls.append(graph_component(page, graph, 6 if images else 12))
    for plot in images:
        controls.append(graph_component(page, plot, 6 if graph and len(images)==1 else 4))

    return ft.Container(
        ft.ResponsiveRow(
            controls=controls,
            spacing=10,
        ),
        col={"sm": 12},
        bgcolor="#F1F1F1",
        border_radius=30,
        expand=2,
        alignment=ft.alignment.center,
        padding=10,
    )