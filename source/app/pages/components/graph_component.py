import flet as ft

def graph_component(page: ft.Page, graph : ft.Image, size : int = 4) -> ft.Container:
    """
    Компонент графика
    """
    return ft.Container(
        content=ft.Card(
            content=ft.Container(
                graph,
                padding=10,
            ),
            elevation=5,
            color=ft.colors.WHITE,
            surface_tint_color=ft.colors.WHITE,
        ),
        col={"sm": size, "xs": 12},
        padding=5,
    )