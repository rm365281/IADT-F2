import asyncio
import copy
import itertools
import time
from typing import Callable, Awaitable
from typing import Callable, Awaitable, Optional
from domain.solution import Solution
from genetic_algorithm.selection import parents_selection
from vrp.vrp_builder import VrpFactory


class GeneticAlgorithmRunner:
    def __init__(self, vrp_factory: VrpFactory, population_size: int, on_new_best_solution: Callable[[dict], Awaitable[None]] = None) -> None:
        self.vrp = vrp_factory.create_vrp()
        self.population_size = population_size
        self.population: list[Solution] = self.vrp.generate_initial_population()

        self.best_solution: Optional[Solution] = None
        self.generation_counter = itertools.count(start=1)

        self.running = False
        self.paused = False
        self.on_new_best_solution = on_new_best_solution


    async def loop(self):
        start_time = time.time()
        while self.running:
            if self.paused:
                await asyncio.sleep(0.1)
                continue

            generation_start = time.time()
            generation = next(self.generation_counter)

            for individual in self.population:
                self.vrp.fitness(individual)

            self.population = self.vrp.sort_population(population=self.population)

            generation_time = time.time() - generation_start
            total_time = time.time() - start_time

            if self.best_solution is None or self.best_solution.fitness > self.population[0].fitness:
                self.best_solution = self.population[0]
                if self.on_new_best_solution:
                    await self.on_new_best_solution({
                        "event": "new_best_solution",
                        "generation": generation,
                        "best_distance": round(self.best_solution.total_distance(), 2),
                        "best_fitness": round(self.best_solution.fitness, 2),
                        "generation_time": round(generation_time, 2),
                        "total_time": round(total_time, 2)
                    })

            new_population = [copy.deepcopy(self.population[0])]
            while len(new_population) < self.population_size:
                parent1, parent2 = parents_selection(self.population)
                child1, child2 = self.vrp.crossover(parent1, parent2)
                mutated_child1 = self.vrp.mutate(child1)
                mutated_child2 = self.vrp.mutate(child2)
                new_population.extend([mutated_child1, mutated_child2])

            self.population = new_population
            await asyncio.sleep(0)

    async def start(self):
        if not self.running:
            self.running = True
            self.paused = False
            asyncio.create_task(self.loop())

    async def pause(self):
        self.paused = True

    async def resume(self):
        self.paused = False

    async def stop(self):
        self.running = False

    def status(self):
        return {
            "running": self.running,
            "paused": self.paused,
            "best_solution": self.best_solution.to_dict() if self.best_solution else None
        }