import flet as ft

def text_input(page: ft.Page, label: str, hint: str, *args, **kwargs) -> ft.TextField:
    """
    Компонент кастомного поля ввода
    """
    
    value = kwargs.pop("value", "")
    
    return ft.TextField(
        label=label,
        label_style=ft.TextStyle(
            color=ft.colors.WHITE,
            size=14,
            weight=ft.FontWeight.NORMAL
        ),
        hint_text=hint,
        value=value,
        border=ft.InputBorder.UNDERLINE,
        border_color="#FFFFFF",
        color="#FFFFFF",
        col={"sm": 12, "md": 6},
    )