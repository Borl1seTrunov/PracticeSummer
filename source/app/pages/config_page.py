import flet as ft
import json
import random
from typing import List
from .components.page_layer import page_layer  
from .components.graphs import graphs
from .components.button import button
from .components.text_input import text_input
from app.constants import (
    DEFAULT_PROB_MUT, DEFAULT_PROB_CROSSOVER, DEFAULT_POPULATION_SIZE,
    DEFAULT_GENERATION_COUNT, DEFAULT_VERTEX_COUNT, SELECTION_TYPES
)

def generate_random_graph(num_vertices: int = 6) -> List[List[int]]:
    graph = [[0]*num_vertices for _ in range(num_vertices)]
    for i in range(num_vertices):
        for j in range(i+1, num_vertices):
            edge = random.choice([0, 1])
            if edge:
                weight = random.randint(1, 10)
                graph[i][j] = weight
                graph[j][i] = weight
            else:
                graph[i][j] = 0
                graph[j][i] = 0
    return graph

def config_view(page: ft.Page) -> ft.View:
    initial_prob_mut: str = DEFAULT_PROB_MUT
    initial_prob_crossover: str = DEFAULT_PROB_CROSSOVER
    initial_population_size: str = DEFAULT_POPULATION_SIZE
    initial_generation_count: str = DEFAULT_GENERATION_COUNT
    initial_vertex_count: str = DEFAULT_VERTEX_COUNT

    if not hasattr(page, "params"):
        page.params = {
            "prob_mut": initial_prob_mut,
            "prob_crossover": initial_prob_crossover,
            "population_size": initial_population_size,
            "generation_count": initial_generation_count,
            "vertex_count": initial_vertex_count,
            "selection_type": SELECTION_TYPES[0]
        }

    if not hasattr(page, "current_graph"):
        page.current_graph = generate_random_graph(num_vertices=int(page.params["vertex_count"]))

    def on_prob_mut_change(e: ft.ControlEvent) -> None:
        page.params["prob_mut"] = e.control.value

    def on_prob_crossover_change(e: ft.ControlEvent) -> None:
        page.params["prob_crossover"] = e.control.value

    def on_population_size_change(e: ft.ControlEvent) -> None:
        page.params["population_size"] = e.control.value

    def on_generation_count_change(e: ft.ControlEvent) -> None:
        page.params["generation_count"] = e.control.value

    def on_vertex_count_change(e: ft.ControlEvent) -> None:
        page.params["vertex_count"] = e.control.value

    def on_selection_type_change(e: ft.ControlEvent) -> None:
        page.params["selection_type"] = e.control.value

    def on_random_graph_click(e: ft.ControlEvent) -> None:
        vertex_count = int(page.params.get("vertex_count", initial_vertex_count) or initial_vertex_count)
        page.current_graph = generate_random_graph(num_vertices=vertex_count)
        page._graph_img_base64 = None
        page._graph_img_graph_id = None
        page.views.clear()
        from app.pages.config_page import config_view
        page.views.append(config_view(page))
        page.update()

    if not hasattr(page, "file_picker"):
        page.file_picker = ft.FilePicker()
        page.overlay.append(page.file_picker)
        page.update()

    def on_save_graph_click(e: ft.ControlEvent) -> None:
        def save_result(result: ft.FilePickerResultEvent) -> None:
            if result.path:
                with open(result.path, "w", encoding="utf-8") as f:
                    json.dump(page.current_graph, f)
        page.file_picker.on_result = save_result
        page.file_picker.save_file(file_name="graph.json", allowed_extensions=["json"])

    def on_load_graph_click(e: ft.ControlEvent) -> None:
        def load_result(result: ft.FilePickerResultEvent) -> None:
            if result.files:
                file_path = result.files[0].path
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        loaded_graph = json.load(f)
                        if isinstance(loaded_graph, list) and all(isinstance(row, list) for row in loaded_graph):
                            page.current_graph = loaded_graph
                            page._graph_img_base64 = None
                            page._graph_img_graph_id = None
                            page.views.clear()
                            from app.pages.config_page import config_view
                            page.views.append(config_view(page))
                            page.update()
                except Exception as ex:
                    page.snack_bar = ft.SnackBar(ft.Text(f"Ошибка загрузки: {ex}"))
                    page.snack_bar.open = True
                    page.update()
        page.file_picker.on_result = load_result
        page.file_picker.pick_files(allow_multiple=False, allowed_extensions=["json"])

    load_graph_button = button(page, "Загрузить граф")
    save_graph_button = button(page, "Сохранить граф")
    random_graph_button = button(page, "Случайный граф")
    random_graph_button.on_click = on_random_graph_click
    save_graph_button.on_click = on_save_graph_click
    load_graph_button.on_click = on_load_graph_click

    prob_mut_textinput = text_input(
        page, "Вероятность мутации", "0.0 - 1.0", value=page.params["prob_mut"]
    )
    prob_mut_textinput.on_change = on_prob_mut_change

    prob_crossover_textinput = text_input(
        page, "Вероятность скрещивания", "0.0 - 1.0", value=page.params["prob_crossover"]
    )
    prob_crossover_textinput.on_change = on_prob_crossover_change

    population_size_textinput = text_input(
        page, "Размер популяции", "Целое число", value=page.params["population_size"]
    )
    population_size_textinput.on_change = on_population_size_change

    generation_count_textinput = text_input(
        page, "Количество поколений", "Целое число", value=page.params["generation_count"]
    )
    generation_count_textinput.on_change = on_generation_count_change

    count_vertext_textinput = text_input(
        page, "Количество вершин в случайном графе", "Целое число", value=page.params["vertex_count"]
    )
    count_vertext_textinput.on_change = on_vertex_count_change

    selection_dropdown = ft.Dropdown(
        label="Тип отбора",
        label_style=ft.TextStyle(color=ft.Colors.WHITE),
        options=[ft.dropdown.Option(t) for t in SELECTION_TYPES],
        value=page.params["selection_type"],
        col={"sm": 12},
        expand=True,
        border_color=ft.Colors.WHITE,
        text_style=ft.TextStyle(color=ft.Colors.WHITE),
        on_change=on_selection_type_change
    )

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
                                color=ft.Colors.WHITE
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
                                        content=graphs(
                                            page,
                                            page.current_graph,
                                            full_width=True
                                        ),
                                        col={"sm": 6, "md": 7},
                                        padding=ft.padding.all(10),
                                        border_radius=10,
                                        expand=True
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
                                        color=ft.Colors.WHITE
                                    ),
                                    ft.ResponsiveRow(
                                        controls=[
                                            prob_mut_textinput,
                                            prob_crossover_textinput,
                                            population_size_textinput,
                                            generation_count_textinput,
                                            count_vertext_textinput,
                                            selection_dropdown
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