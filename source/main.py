import flet as ft
from app.app import App

"""
Точка входа в программу
"""

def main(page: ft.Page) -> None:
    app = App(page)
    app.build()

if __name__ == "__main__":
    ft.app(target=main)