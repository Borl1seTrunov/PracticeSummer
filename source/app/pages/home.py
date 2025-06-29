import flet as ft

from .components.page_layer import page_layer 

def home_view(page: ft.Page):
    """
    Страница с работой алгоритма
    """
    return ft.View(
        "/",
        controls=[
            page_layer(
                page=page, 
                content_page=ft.Text(
                        "Main",
                        text_align=ft.TextAlign.CENTER
                    ),
                )
        ],
        padding=0
    )
