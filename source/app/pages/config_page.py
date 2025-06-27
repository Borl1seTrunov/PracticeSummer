import flet as ft

def config_view(page: ft.Page):
    def go_home(e):
        page.go("/")

    return ft.View(
        "/config",
        controls=[
            ft.Text("О приложении", style="headlineMedium"),
            ft.Text("Конфиг алгоритма."),
            ft.ElevatedButton("Назад на главную", on_click=go_home),
        ]
    )
