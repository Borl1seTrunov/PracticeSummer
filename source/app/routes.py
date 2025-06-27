from app.pages.home import home_view
from app.pages.config_page import config_view
from app.pages.not_found import not_found_view

routes = {
    "/": home_view,
    "/config": config_view,
    "/404": not_found_view,
}