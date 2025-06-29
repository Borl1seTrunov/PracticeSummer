import flet as ft

def menu(page: ft.Page) -> ft.Column:
    """
    Компонент бокового меню
    """
    
    return ft.Column(
        controls=[
            ft.Container(
                content=ft.TextButton(
                    "Алгоритм",
                    style=ft.ButtonStyle(
                        color="#000000",
                        overlay_color=ft.Colors.TRANSPARENT,
                        shadow_color=ft.Colors.TRANSPARENT,
                        surface_tint_color=ft.Colors.TRANSPARENT,
                    ),
                    on_click=lambda e: page.go("/")
                ),
                width=200,
                alignment=ft.alignment.center,
            ),
            ft.Container(
                content=ft.TextButton(
                    "Параметры",
                    style=ft.ButtonStyle(
                        color="#000000",
                        overlay_color=ft.Colors.TRANSPARENT,
                        shadow_color=ft.Colors.TRANSPARENT,
                        surface_tint_color=ft.Colors.TRANSPARENT,
                    ),
                    on_click=lambda e: page.go("/config")
                ),
                width=200,
                alignment=ft.alignment.center,
            ),
            ft.Container(
                content=ft.TextButton(
                    "О приложении",
                    style=ft.ButtonStyle(
                        color="#000000",
                        overlay_color=ft.Colors.TRANSPARENT,
                        shadow_color=ft.Colors.TRANSPARENT,
                        surface_tint_color=ft.Colors.TRANSPARENT,
                    ),
                    on_click=lambda e: page.go("/404")
                ),
                width=200,
                alignment=ft.alignment.center,
            ),
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
    )