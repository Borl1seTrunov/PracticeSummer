import flet as ft

from .button import button

def work_component(page : ft.Page) -> ft.Container:
    """
    Компонента запуска и отладочной информации алгоритма
    """

    run_algo_button = button(page, "Запустить алгоритм")
    prev_step_button = button(page, "<-", "#6000FF", {"sm":6})
    next_step_button = button(page, "->", "#A46DFF", {"sm":6})

    return ft.Container(
        content=ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.ResponsiveRow(
                                controls=[
                                    run_algo_button,
                                    prev_step_button,
                                    next_step_button,
                                ],
                            )
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        alignment=ft.MainAxisAlignment.CENTER,
                        expand=True
                    ),
                    col={"sm":4},
                    expand=True,
                    bgcolor=ft.Colors.TRANSPARENT,
                    padding=10
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=ft.Text(
                                    "Отладочные сообщения",
                                    text_align=ft.TextAlign.CENTER,
                                    size=20,
                                    width=float("inf"),
                                ),
                                alignment=ft.alignment.center,
                                padding=ft.padding.only(bottom=10),
                            ),
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.Text("Алгоритм запущен", size=16),
                                        *[ft.Text(f"Отладочное сообщение номер {str(i + 1)}", width=float("inf"), size=16) for i in range(100)]
                                    ],
                                    scroll=ft.ScrollMode.AUTO,
                                ),
                                expand=True,
                            )
                        ],
                        expand=True,
                    ),
                    col={"sm":8},
                    expand=True,
                    bgcolor=ft.colors.BLUE,
                    border_radius=30,
                    padding=20,
                )
            ],
            expand=True
        ),
        expand=3,
        alignment=ft.alignment.center,
        padding=10
    )