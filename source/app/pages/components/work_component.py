import flet as ft

def work_component(page : ft.Page) -> ft.Container:
    """
    Компонента запуска и отладочной информации алгоритма
    """
    
    return ft.Container(
        content=ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.ResponsiveRow(
                                controls=[
                                    ft.Button(
                                        text="Запустить алгоритм",
                                        col={"sm":12},
                                        style=ft.ButtonStyle(
                                            color="#FFFFFF",
                                            shape=ft.RoundedRectangleBorder(radius=10)
                                        ),
                                        height=78,
                                        bgcolor="#711BFF"
                                    ),
                                    ft.Button(
                                        text="<-",
                                        col={"sm":6},
                                        style=ft.ButtonStyle(
                                            color="#FFFFFF",
                                            shape=ft.RoundedRectangleBorder(radius=10)
                                        ),
                                        bgcolor="#6000FF",
                                        height=50
                                    ),
                                    ft.Button(
                                        text="->",
                                        col={"sm":6},
                                        style=ft.ButtonStyle(
                                            color="#FFFFFF",
                                            shape=ft.RoundedRectangleBorder(radius=10)
                                        ),
                                        bgcolor="#A46DFF",
                                        height=50
                                    )
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