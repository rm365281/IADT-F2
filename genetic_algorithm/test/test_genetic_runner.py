import unittest
import asyncio
from unittest.mock import AsyncMock
from genetic_algorithm.genetic_runner import GeneticAlgorithmRunner
from domain.solution import Solution

class DummyVRP:
    def __init__(self):
        self._fitness_called = False
        self._sort_called = False
        self._crossover_called = False
        self._mutate_called = False
        self._population = [Solution([])]
    def create_vrp(self):
        return self
    def generate_initial_population(self):
        return [Solution([]) for _ in range(2)]
    def fitness(self, individual):
        self._fitness_called = True
        individual.fitness = 1.0
    def sort_population(self, population):
        self._sort_called = True
        return population
    def crossover(self, p1, p2):
        self._crossover_called = True
        return p1, p2
    def mutate(self, child):
        self._mutate_called = True
        return child

class TestGeneticAlgorithmRunner(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.vrp_factory = DummyVRP()
        self.runner = GeneticAlgorithmRunner(self.vrp_factory, population_size=2)

    def test_initialization(self):
        self.assertEqual(len(self.runner.population), 2)
        self.assertFalse(self.runner.running)
        self.assertFalse(self.runner.paused)
        self.assertIsNone(self.runner.best_solution)

    def test_status(self):
        status = self.runner.status()
        self.assertIn("running", status)
        self.assertIn("paused", status)
        self.assertIn("best_solution", status)

    async def test_start_and_stop(self):
        await self.runner.start()
        self.assertTrue(self.runner.running)
        await self.runner.stop()
        self.assertFalse(self.runner.running)

    async def test_pause_and_resume(self):
        await self.runner.start()
        await self.runner.pause()
        self.assertTrue(self.runner.paused)
        await self.runner.resume()
        self.assertFalse(self.runner.paused)

    async def test_loop_updates_best_solution_and_calls_callback(self):
        callback = AsyncMock()
        runner = GeneticAlgorithmRunner(self.vrp_factory, population_size=2, on_new_best_solution=callback)
        runner.running = True
        runner.paused = False
        # Run the loop in a background task
        task = asyncio.create_task(runner.loop())
        await asyncio.sleep(0.05)  # Let it run briefly
        runner.running = False     # Stop the loop
        await task                # Wait for loop to finish
        self.assertIsNotNone(runner.best_solution)
        callback.assert_called()