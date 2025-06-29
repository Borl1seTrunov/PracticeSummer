import flet as ft
from .components.page_layer import page_layer  
from .components.graphs import graphs
from .components.button import button
from .components.text_input import text_input

def config_view(page: ft.Page):
    """
    Страница конфига приложения
    """

    load_graph_button = button(page, "Загрузить граф")
    save_graph_button = button(page, "Сохранить граф")
    random_graph_button = button(page, "Случайный граф граф")

    prob_mut_textinput = text_input(page, "Вероятность мутации", "0.0 - 1.0")
    prob_crossover_textinput = text_input(page, "Вероятность скрещивания", "0.0 - 1.0")
    population_size_textinput = text_input(page, "Размер популяции", "Целое число")
    generation_count_textinput = text_input(page, "Количество поколений", "Целое число")
    count_vertext_textinput = text_input(page, "Количество вершин в случайном графе", "Целое число")

    return ft.View(
        "/config",
        controls=[
            page_layer(
                page=page, 
                content_page=ft.Column(
                    controls=[
                        ft.Container(
                            content=ft.Text(
                                "Параметры приложения",
                                text_align=ft.TextAlign.CENTER,
                                size=20,
                                weight=ft.FontWeight.BOLD,
                                color=ft.colors.WHITE
                            ),
                            padding=ft.padding.only(bottom=20),
                            alignment=ft.alignment.center,
                            col={"sm": 12}
                        ),
                        ft.Container(
                            content=ft.ResponsiveRow(
                                controls=[
                                    ft.Container(
                                        content=ft.ResponsiveRow(
                                            controls=[
                                                load_graph_button,
                                                save_graph_button,
                                                random_graph_button,
                                            ],
                                            spacing=10,
                                            alignment=ft.MainAxisAlignment.CENTER,
                                            expand=True
                                        ),
                                        col={"sm": 6, "md": 5},
                                        padding=ft.padding.all(20),
                                        border_radius=10,
                                        expand=True
                                    ),
                                    ft.Container(
                                        content=graphs(page, ft.Image()),
                                        col={"sm": 6, "md": 7},
                                        padding=ft.padding.all(10),
                                        border_radius=10,
                                        expand=True,
                                        alignment=ft.alignment.center
                                    )
                                ],
                                spacing=10,
                                vertical_alignment=ft.CrossAxisAlignment.STRETCH,
                                expand=True
                            ),
                            expand=True,
                            padding=ft.padding.symmetric(horizontal=20)
                        ),
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text(
                                        "Параметры генетического алгоритма",
                                        size=18,
                                        weight=ft.FontWeight.BOLD,
                                        text_align=ft.TextAlign.CENTER,
                                        color=ft.colors.WHITE
                                    ),
                                    ft.ResponsiveRow(
                                        controls=[
                                            prob_mut_textinput,
                                            prob_crossover_textinput,
                                            population_size_textinput,
                                            generation_count_textinput,
                                            count_vertext_textinput,
                                            ft.Dropdown(
                                                label="Тип отбора",
                                                label_style=ft.TextStyle(color=ft.colors.WHITE),
                                                options=[
                                                    ft.dropdown.Option("Рулетка"),
                                                    ft.dropdown.Option("Турнирный"),
                                                    ft.dropdown.Option("Ранговая"),
                                                ],
                                                col={"sm": 12},
                                                expand=True,
                                                border_color=ft.colors.WHITE,
                                                text_style=ft.TextStyle(color=ft.colors.WHITE)
                                            )
                                        ],
                                        spacing=20,
                                        run_spacing=10
                                    )
                                ],
                                spacing=20
                            ),
                            col={"sm": 12},
                            padding=ft.padding.all(20),
                            border_radius=10,
                            margin=ft.margin.only(top=20)
                        )
                    ],
                    expand=True,
                    spacing=0,
                )
            )
        ],
        padding=0,
    )