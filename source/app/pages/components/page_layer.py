import flet as ft
from .menu_component import menu   

def page_layer(page: ft.Page, content_page) -> ft.ResponsiveRow:
    """
    Компонент основного слоя страницы приложения
    Справа находится меню размером, слева находится основной контент страницы
    """
    
    return ft.ResponsiveRow(
        controls=[
            ft.Container(
                content=menu(page),
                col={"sm":2},
                bgcolor="#F1F1F1",
                expand=True
            ),
            ft.Container(
                content=content_page,
                col={"sm":10},
                expand=True,
                padding=10
            )
        ],
        spacing=10,
        expand=True,
    )