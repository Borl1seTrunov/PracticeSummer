import flet as ft
from app.config import APP_NAME
from app.routes import routes

class App:
    """
    Класс приложения
    """
    
    def __init__(self, page: ft.Page):
        self.page = page
        self.page.title = APP_NAME
        self.page.theme_mode = ft.ThemeMode.DARK
        self.page.on_route_change = self.route_change
        self.page.on_view_pop = self.view_pop

    def build(self):
        self.page.appbar = ft.AppBar(title=ft.Text(APP_NAME))
        self.page.go(self.page.route)

    def route_change(self, e):
        self.page.views.clear()
        route = self.page.route
        view_func = routes.get(route, routes["/404"])
        self.page.views.append(view_func(self.page))
        self.page.update()

    def view_pop(self, e):
        self.page.views.pop()
        self.page.update()
