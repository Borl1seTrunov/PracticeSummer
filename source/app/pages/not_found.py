import flet as ft

from .components.menu_component import header   

def not_found_view(page: ft.Page):
    return ft.View(
        "/",
        controls=[
            ft.ResponsiveRow(
                controls=[
                    ft.Container(
                        content=header(page),
                        col={"sm":3},
                        bgcolor="#F1F1F1",
                        expand=True
                    ),
                    ft.Container(
                        content=ft.Text(
                            "Страница не найдена",
                            text_align=ft.TextAlign.CENTER
                        ),
                        col={"sm":9},
                        expand=True,
                    )
                ],
                spacing=0,
                expand=True,
            ),
        ],
        padding=0
    )
