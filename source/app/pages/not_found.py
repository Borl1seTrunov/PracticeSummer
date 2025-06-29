import flet as ft

from .components.page_layer import page_layer   

def not_found_view(page: ft.Page):
    """
    Страница 404
    """
    return ft.View(
        "/404",
        controls=[
            page_layer(
                page=page, 
                content_page=ft.Text(
                        "Page not found",
                        text_align=ft.TextAlign.CENTER
                    ),
                )
        ],
        padding=0
    )