import flet as ft

def not_found_view(page: ft.Page):
    def go_home(e):
        page.go("/")

    return ft.View(
        "/404",
        controls=[
            ft.Text("Страница не найдена", style="headlineMedium", color="red"),
            ft.ElevatedButton("На главную", on_click=go_home),
        ]
    )
