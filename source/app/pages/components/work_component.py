import flet as ft
from app.genetic_algorithm import GeneticAlgorithmMST
from .button import button
from .graphs import graphs

def work_component(page : ft.Page) -> ft.Container:
    """
    Компонента запуска и отладочной информации алгоритма
    """
    result_text = ft.Text("Результат будет здесь", size=16, color="#000000")
    debug_column = ft.Column(controls=[], scroll=ft.ScrollMode.AUTO)
    slider_value_text = ft.Text("Поколение: 0", size=14, color="#ffffff")
    mst_weight_text = ft.Text("Вес МОД: -", size=14, color="#ffffff")
    slider = ft.Slider(min=0, max=0, divisions=1, value=0, label="0", on_change=None)

    page.mst_graphs_by_gen = []
    page.mst_weights_by_gen = []

    page.ga_step_state = {
        'ga': None,
        'population': None,
        'generation': 0,
        'fitness_history': [],
        'best_individual': None,
        'best_fitness': float('inf'),
        'best_edges': None,
        'mst_graphs_by_gen': [],
        'mst_weights_by_gen': [],
        'done': False
    }

    def move_slider(delta):
        new_value = int(slider.value) + delta
        new_value = max(slider.min, min(slider.max, new_value))
        slider.value = new_value
        slider.label = str(int(slider.value))
        slider.update()
        update_slider_info(slider)
        update_nav_buttons()

    def update_nav_buttons():
        left_btn.disabled = slider.value <= slider.min
        right_btn.disabled = slider.value >= slider.max
        left_btn.update()
        right_btn.update()

    left_btn = ft.IconButton(ft.Icons.ARROW_LEFT, on_click=lambda e: move_slider(-1))
    right_btn = ft.IconButton(ft.Icons.ARROW_RIGHT, on_click=lambda e: move_slider(1))
    left_btn.disabled = True
    right_btn.disabled = True

    def run_algorithm(e):
        graph = page.current_graph
        params = page.params if hasattr(page, 'params') else {}
        selection_type = params.get('selection_type', 'Турнир')
        num_nodes = len(graph)
        nodes = list(range(num_nodes))
        edge_dict = {}
        for i in range(num_nodes):
            for j in range(i+1, num_nodes):
                if graph[i][j]:
                    edge_dict[(i, j)] = graph[i][j]
                    edge_dict[(j, i)] = graph[i][j]
        ga = GeneticAlgorithmMST(
            graph=edge_dict,
            population_size=int(params.get('population_size', 50)),
            generations=int(params.get('generation_count', 100)),
            crossover_rate=float(params.get('prob_crossover', 0.8)),
            mutation_rate=float(params.get('prob_mut', 0.05)),
            selection_type=selection_type
        )
        debug_column.controls.clear()
        page.best_mst_graph = None
        page.best_mst_weight = None
        page.mst_graphs_by_gen = []
        page.mst_weights_by_gen = []
        def debug_callback(gen, best, best_edges_gen, fitness_history):
            mst_matrix = [[0 for _ in range(num_nodes)] for _ in range(num_nodes)]
            for edge in best_edges_gen:
                i, j = edge
                weight = ga.graph[edge]
                mst_matrix[i][j] = weight
                mst_matrix[j][i] = weight
            page.mst_graph = mst_matrix
            page.mst_weights_history = fitness_history[:gen+1]
            if len(page.mst_graphs_by_gen) <= gen:
                page.mst_graphs_by_gen.append(mst_matrix)
                page.mst_weights_by_gen.append(best)
            else:
                page.mst_graphs_by_gen[gen] = mst_matrix
                page.mst_weights_by_gen[gen] = best
            debug_column.controls.append(
                ft.Text(f"Поколение {gen}, Лучшая приспособленность: {best}", size=14, color="#000000")
            )
            debug_column.update()
            if page.best_mst_weight is None or best < page.best_mst_weight:
                page.best_mst_graph = [row[:] for row in mst_matrix]
                page.best_mst_weight = best
            if hasattr(page, 'graphs_container'):
                page.graphs_container.content = graphs(
                    page,
                    page.current_graph,
                    page.mst_graph,
                    page.mst_weights_history
                )
                page.graphs_container.update()
            page.update()
        best_edges, best_weight, best_fitness_history = ga.run(debug_callback=debug_callback)
        slider.max = len(page.mst_graphs_by_gen) - 1
        slider.divisions = max(1, len(page.mst_graphs_by_gen) - 1)
        slider.value = slider.max
        slider.label = str(int(slider.value))
        slider.update()
        update_slider_info(slider)
        update_nav_buttons()
        mst_matrix = getattr(page, 'best_mst_graph', None)
        best_weight = getattr(page, 'best_mst_weight', None)
        if mst_matrix is not None and best_weight is not None:
            unique_edges = set()
            total_weight = 0
            num_nodes = len(mst_matrix)
            result_lines = ["Минимальное остовное дерево:"]
            for i in range(num_nodes):
                for j in range(i+1, num_nodes):
                    if mst_matrix[i][j]:
                        unique_edges.add((i, j))
                        result_lines.append(f"{i} -- {j} (вес: {mst_matrix[i][j]})")
                        total_weight += mst_matrix[i][j]
            if len(unique_edges) != num_nodes - 1:
                result_lines = ["Остовное дерево не найдено"]
            else:
                result_lines.append(f"Суммарный вес: {total_weight}")
            result_text.value = "\n".join(result_lines)
            result_text.color = "#000000"
            result_text.update()

    def step_algorithm(e):
        if not page.ga_step_state['ga']:
            graph = page.current_graph
            params = page.params if hasattr(page, 'params') else {}
            selection_type = params.get('selection_type', 'Турнир')
            num_nodes = len(graph)
            edge_dict = {}
            for i in range(num_nodes):
                for j in range(i+1, num_nodes):
                    if graph[i][j]:
                        edge_dict[(i, j)] = graph[i][j]
                        edge_dict[(j, i)] = graph[i][j]
            ga = GeneticAlgorithmMST(
                graph=edge_dict,
                population_size=int(params.get('population_size', 50)),
                generations=int(params.get('generation_count', 100)),
                crossover_rate=float(params.get('prob_crossover', 0.8)),
                mutation_rate=float(params.get('prob_mut', 0.05)),
                selection_type=selection_type
            )
            population = ga._initialize_population()
            page.ga_step_state['ga'] = ga
            page.ga_step_state['population'] = population
            page.ga_step_state['generation'] = 0
            page.ga_step_state['fitness_history'] = []
            page.ga_step_state['best_individual'] = None
            page.ga_step_state['best_fitness'] = float('inf')
            page.ga_step_state['best_edges'] = None
            page.ga_step_state['mst_graphs_by_gen'] = []
            page.ga_step_state['mst_weights_by_gen'] = []
            page.ga_step_state['done'] = False
            debug_column.controls.clear()
            result_text.value = "Результат будет здесь"
            result_text.update()
        if page.ga_step_state['done']:
            return
        ga = page.ga_step_state['ga']
        population = page.ga_step_state['population']
        generation = page.ga_step_state['generation']
        fitness_history = page.ga_step_state['fitness_history']
        best_individual = page.ga_step_state['best_individual']
        best_fitness = page.ga_step_state['best_fitness']
        best_edges = page.ga_step_state['best_edges']
        mst_graphs_by_gen = page.ga_step_state['mst_graphs_by_gen']
        mst_weights_by_gen = page.ga_step_state['mst_weights_by_gen']
        if generation >= ga.generations:
            page.ga_step_state['done'] = True
            return
        fitnesses = [ga._fitness(ind) for ind in population]
        current_best = min(fitnesses)
        idx_best = fitnesses.index(current_best)
        if current_best < best_fitness:
            best_fitness = current_best
            best_individual = population[idx_best][:]
            best_edges = [edge for edge, bit in zip(ga.edges, best_individual) if bit]
        fitness_history.append(best_fitness)
        num_nodes = len(ga.nodes)
        mst_matrix = [[0 for _ in range(num_nodes)] for _ in range(num_nodes)]
        for edge in [edge for edge, bit in zip(ga.edges, population[idx_best]) if bit]:
            i, j = edge
            if i < num_nodes and j < num_nodes:
                weight = ga.graph[edge]
                mst_matrix[i][j] = weight
                mst_matrix[j][i] = weight
        if len(mst_graphs_by_gen) < ga.generations:
            mst_graphs_by_gen.append(mst_matrix)
            mst_weights_by_gen.append(current_best)
        debug_column.controls.append(
            ft.Text(f"Поколение {generation}, Лучшая приспособленность: {current_best}", size=14, color="#000000")
        )
        debug_column.update()
        page.mst_graphs_by_gen = mst_graphs_by_gen
        page.mst_weights_by_gen = mst_weights_by_gen
        page.mst_weights_history = fitness_history[:]
        if hasattr(page, 'graphs_container'):
            page.graphs_container.content = graphs(
                page,
                page.current_graph,
                mst_matrix,
                page.mst_weights_history
            )
            page.graphs_container.update()
        slider.max = len(page.mst_graphs_by_gen) - 1
        slider.divisions = max(1, len(page.mst_graphs_by_gen) - 1)
        slider.value = slider.max
        slider.label = str(int(slider.value))
        slider.update()
        update_slider_info(slider)
        update_nav_buttons()
        if generation + 1 >= ga.generations:
            page.ga_step_state['done'] = True
            if best_individual is not None:
                mst_matrix = [[0 for _ in range(num_nodes)] for _ in range(num_nodes)]
                for edge in [edge for edge, bit in zip(ga.edges, best_individual) if bit]:
                    i, j = edge
                    weight = ga.graph[edge]
                    mst_matrix[i][j] = weight
                    mst_matrix[j][i] = weight
                unique_edges = set()
                total_weight = 0
                result_lines = ["Минимальное остовное дерево:"]
                for i in range(num_nodes):
                    for j in range(i+1, num_nodes):
                        if mst_matrix[i][j]:
                            unique_edges.add((i, j))
                            result_lines.append(f"{i} -- {j} (вес: {mst_matrix[i][j]})")
                            total_weight += mst_matrix[i][j]
                if len(unique_edges) != num_nodes - 1:
                    result_lines = ["Остовное дерево не найдено"]
                else:
                    result_lines.append(f"Суммарный вес: {total_weight}")
                result_text.value = "\n".join(result_lines)
                result_text.color = "#000000"
                result_text.update()
        page.ga_step_state['population'] = ga._selection(population, fitnesses)
        next_generation = []
        selected = page.ga_step_state['population']
        for i in range(0, len(selected), 2):
            if i+1 < len(selected):
                child1, child2 = ga._crossover(selected[i], selected[i+1])
                next_generation.extend([child1, child2])
            else:
                next_generation.append(selected[i])
        next_generation = [ga._mutation(ind) for ind in next_generation]
        if best_individual not in next_generation:
            next_generation[0] = best_individual[:]
        page.ga_step_state['population'] = next_generation
        page.ga_step_state['generation'] = generation + 1
        page.ga_step_state['fitness_history'] = fitness_history
        page.ga_step_state['best_individual'] = best_individual
        page.ga_step_state['best_fitness'] = best_fitness
        page.ga_step_state['best_edges'] = best_edges
        page.ga_step_state['mst_graphs_by_gen'] = mst_graphs_by_gen
        page.ga_step_state['mst_weights_by_gen'] = mst_weights_by_gen

    def update_slider_info(slider):
        gen = int(slider.value)
        slider_value_text.value = f"Поколение: {gen}"
        if 0 <= gen < len(page.mst_weights_by_gen):
            mst_weight_text.value = f"Вес МОД: {page.mst_weights_by_gen[gen]}"
        else:
            mst_weight_text.value = "Вес МОД: -"
        slider_value_text.update()
        mst_weight_text.update()
        if hasattr(page, 'graphs_container'):
            mst_graph = page.mst_graphs_by_gen[gen] if 0 <= gen < len(page.mst_graphs_by_gen) else None
            page.graphs_container.content = graphs(
                page,
                page.current_graph,
                mst_graph,
                page.mst_weights_history
            )
            page.graphs_container.update()

    slider.on_change = lambda e: (update_slider_info(slider), update_nav_buttons())

    run_algo_button = button(page, "Запустить алгоритм", width=180)
    run_algo_button.on_click = run_algorithm
    step_algo_button = button(page, "Шаг", width=180)
    step_algo_button.on_click = step_algorithm

    finish_algo_button = button(page, "До конца", width=180)
    def finish_algorithm(e):
        ga = page.ga_step_state['ga']
        if not ga:
            step_algorithm(None)
            ga = page.ga_step_state['ga']
        while not page.ga_step_state['done'] and page.ga_step_state['generation'] < ga.generations:
            step_algorithm(None)
    finish_algo_button.on_click = finish_algorithm

    return ft.Container(
        content=ft.ResponsiveRow(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            run_algo_button,
                            step_algo_button,
                            finish_algo_button,
                            slider,
                            ft.Row([left_btn, right_btn], alignment=ft.MainAxisAlignment.CENTER),
                            slider_value_text,
                            mst_weight_text,
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
                                    color="#000000"
                                ),
                                alignment=ft.alignment.center,
                                padding=ft.padding.only(bottom=10),
                            ),
                            ft.Container(
                                content=debug_column,
                                expand=True,
                            )
                        ],
                        expand=True,
                    ),
                    col={"sm":4},
                    expand=True,
                    bgcolor="#F1F1F1",
                    border_radius=30,
                    padding=20,
                ),
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Container(
                                content=result_text,
                                padding=ft.padding.only(top=10, left=5, right=5, bottom=5),
                                bgcolor="#F1F1F1",
                                border_radius=10,
                                alignment=ft.alignment.center,
                                expand=False
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        expand=True
                    ),
                    col={"sm":4},
                    expand=True,
                    bgcolor=ft.Colors.TRANSPARENT,
                    padding=10
                ),
            ],
            expand=True
        ),
        expand=1,
        alignment=ft.alignment.center,
        padding=10
    )