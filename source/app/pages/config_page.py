import flet as ft

from .components.page_layer import page_layer  

def config_view(page: ft.Page):
    """
    Страница конфига приложения
    """
    
    return ft.View(
        "/config",
        controls=[
            page_layer(
                page=page, 
                content_page=ft.Text(
                        "Конфиг алгоритма",
                        text_align=ft.TextAlign.CENTER
                    ),
                )
        ],
        padding=0
    )
