from app.pages.home import home_view
from app.pages.config_page import config_view
from app.pages.not_found import not_found_view

"""
Пути-вкладки приложения
/ корневой путь, страница работы самого алгоритма
/config путь с конфигурацией алгоритма, находятся параметры
/404 путь ненайденной страницы 
"""

routes = {
    "/": home_view,
    "/config": config_view,
    "/404": not_found_view,
}