import flet as ft

def button(page: ft.Page, text : str, bgcolor : str | ft.Colors = "#711BFF", col={"sm":12}) -> ft.Button:
    """
    Компонент кастомной кнопки
    """
    
    return  ft.Button(
        text=text,
        col=col,
        style=ft.ButtonStyle(
            color="#FFFFFF",
            shape=ft.RoundedRectangleBorder(radius=10)
        ),
        height=75,
        bgcolor=bgcolor
    )