import flet as ft

def home_view(page: ft.Page):
    def go_config(e):
        page.go("/config")

    return ft.View(
        "/",
        controls=[
            ft.Text("Основная", style="headlineMedium"),
            ft.ElevatedButton("Перейти к конфигу", on_click=go_config),
        ]
    )
