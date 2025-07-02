import random
import itertools
from collections import defaultdict



class GeneticAlgorithmMST:
    def __init__(self, graph=None, num_nodes=None, edge_probability=0.5, max_weight=10, 
                 population_size=50, generations=100, crossover_rate=0.8, mutation_rate=0.1, penalty=1e6, selection_type='Турнир'):
        if graph is None:
            if num_nodes is None:
                num_nodes = random.randint(5, 10)
            self.graph = self.generate_random_graph(num_nodes, edge_probability, max_weight)
        else:
            self.graph = graph
        self.edges = list(self.graph.keys())
        self.weights = list(self.graph.values())
        self.population_size = population_size
        self.generations = generations
        self.crossover_rate = crossover_rate
        self.mutation_rate = mutation_rate
        self.penalty = penalty
        self.nodes = self._get_nodes()
        self.selection_type = selection_type



    @staticmethod
    def generate_random_graph(num_nodes, edge_probability=0.5, max_weight=10):
        nodes = list(range(num_nodes))
        graph = {}
        for i in range(1, num_nodes):
            u = nodes[0] if random.random() < 0.5 else nodes[random.randint(0, i-1)]
            v = nodes[i]
            weight = random.randint(1, max_weight)
            graph[(u, v)] = weight
            graph[(v, u)] = weight
        for u, v in itertools.combinations(nodes, 2):
            if (u, v) not in graph and random.random() < edge_probability:
                weight = random.randint(1, max_weight)
                graph[(u, v)] = weight
                graph[(v, u)] = weight
        return graph



    def _get_nodes(self):
        nodes = set()
        for (u, v) in self.graph.keys():
            nodes.add(u)
            nodes.add(v)
        return sorted(nodes)



    def _is_spanning_tree(self, individual):
        selected_edges = [edge for edge, bit in zip(self.edges, individual) if bit]
        if len(selected_edges) != len(self.nodes) - 1:
            return False
        adj = defaultdict(list)
        for u, v in selected_edges:
            adj[u].append(v)
            adj[v].append(u)
        visited = set()
        stack = [self.nodes[0]]
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                stack.extend(neighbor for neighbor in adj[node] if neighbor not in visited)
        return len(visited) == len(self.nodes)



    def _fitness(self, individual):
        total_weight = sum(weight for edge, weight, bit in zip(self.edges, self.weights, individual) if bit)
        if not self._is_spanning_tree(individual):
            return self.penalty + total_weight
        return total_weight



    def _random_spanning_tree(self):
        parent = {node: node for node in self.nodes}
        def find(u):
            while parent[u] != u:
                parent[u] = parent[parent[u]]
                u = parent[u]
            return u
        edges = self.edges[::]
        random.shuffle(edges)
        tree_edges = []
        for edge in edges:
            u, v = edge
            ru, rv = find(u), find(v)
            if ru != rv:
                parent[ru] = rv
                tree_edges.append(edge)
            if len(tree_edges) == len(self.nodes) - 1:
                break
        individual = [1 if edge in tree_edges else 0 for edge in self.edges]
        return individual



    def _initialize_population(self):
        population = []
        for _ in range(self.population_size):
            individual = self._random_spanning_tree()
            population.append(individual)
        return population



    def _selection(self, population, fitnesses):
        if self.selection_type == 'Рулетка':
            if len(set(fitnesses)) == 1:
                return [random.choice(population) for _ in range(len(population))]
            max_fit = max(fitnesses)
            adj_fitnesses = [max_fit - f + 1e-6 for f in fitnesses]
            total = sum(adj_fitnesses)
            selected = []
            for _ in range(len(population)):
                pick = random.uniform(0, total)
                current = 0
                for ind, fit in zip(population, adj_fitnesses):
                    current += fit
                    if current >= pick:
                        selected.append(ind)
                        break
            return selected
        selected = []
        for _ in range(len(population)):
            tournament = random.sample(list(zip(population, fitnesses)), k=3)
            winner = min(tournament, key=lambda x: x[1])[0]
            selected.append(winner)
        return selected



    def _crossover(self, parent1, parent2):
        if random.random() < self.crossover_rate:
            point = random.randint(1, len(parent1) - 2)
            child1 = parent1[:point] + parent2[point:]
            child2 = parent2[:point] + parent1[point:]
            if not self._is_spanning_tree(child1):
                child1 = self._random_spanning_tree()
            if not self._is_spanning_tree(child2):
                child2 = self._random_spanning_tree()
            return child1, child2
        return parent1, parent2



    def _mutation(self, individual):
        mutated = individual[:]
        for i in range(len(mutated)):
            if random.random() < self.mutation_rate:
                mutated[i] = 1 - mutated[i]
        if not self._is_spanning_tree(mutated):
            mutated = self._random_spanning_tree()
        return mutated



    def run(self, debug_callback=None):
        population = self._initialize_population()
        best_individual = None
        best_fitness = float('inf')
        best_fitness_history = []
        best_individual_snapshot = None
        for generation in range(self.generations):
            fitnesses = [self._fitness(ind) for ind in population]
            current_best = min(fitnesses)
            idx_best = fitnesses.index(current_best)
            if current_best < best_fitness:
                best_fitness = current_best
                best_individual = population[idx_best][:]
            best_fitness_history.append(best_fitness)
            best_edges_gen = [edge for edge, bit in zip(self.edges, population[idx_best]) if bit]
            selected = self._selection(population, fitnesses)
            next_generation = []
            for i in range(0, len(selected), 2):
                if i+1 < len(selected):
                    child1, child2 = self._crossover(selected[i], selected[i+1])
                    next_generation.extend([child1, child2])
                else:
                    next_generation.append(selected[i])
            next_generation = [self._mutation(ind) for ind in next_generation]
            if best_individual not in next_generation:
                next_generation[0] = best_individual[:]
            population = next_generation
            if debug_callback:
                debug_callback(generation, best_fitness, best_edges_gen, best_fitness_history[:])
        best_edges = [edge for edge, bit in zip(self.edges, best_individual) if bit]
        return best_edges, best_fitness, best_fitness_history
