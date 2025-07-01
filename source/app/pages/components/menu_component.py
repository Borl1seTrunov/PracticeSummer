import flet as ft

def menu(page: ft.Page) -> ft.Column:
    """
    Компонент бокового меню
    """
    menu_items = [
        ("Алгоритм", "/"),
        ("Параметры", "/config"),
        ("О приложении", "/404"),
    ]
    controls = []
    for text, route in menu_items:
        is_active = page.route == route
        controls.append(
            ft.Container(
                content=ft.TextButton(
                    text,
                    style=ft.ButtonStyle(
                        color="#FFFFFF" if is_active else "#000000",
                        bgcolor="#711BFF" if is_active else ft.Colors.TRANSPARENT,
                        overlay_color=ft.Colors.TRANSPARENT,
                        shadow_color=ft.Colors.TRANSPARENT,
                        surface_tint_color=ft.Colors.TRANSPARENT,
                    ),
                    on_click=lambda e, r=route: page.go(r)
                ),
                width=200,
                alignment=ft.alignment.center,
                bgcolor="#711BFF" if is_active else ft.Colors.TRANSPARENT,
                border_radius=10,
                padding=5
            )
        )
    return ft.Column(
        controls=controls,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        expand=True,
    )