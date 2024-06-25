import random

from src.job import Job
from src.machine import Machine
from src.queue import MachineQueue
from .base import BaseShopJobScheduler


class GeneticShopJobScheduler(BaseShopJobScheduler):

    MUTATION_RATE = 0.1
    
    def get_job_order(self) -> list[Job]:
        return self._geentic_algorithm()

    def __initial_poplutation(self, size=10):
        population = []
        for _ in range(size):
            individual = self.jobs[:]
            random.shuffle(individual)
            population.append(individual)
        return population

    def __crossover(self, parent1: list[Job], parent2: list[Job]):
        size = len(parent1)
        start, end = sorted(random.sample(range(size), 2))
        child = [None] * size
        
        child[start:end+1] = parent1[start:end+1]
        
        fill_pos = 0
        for gene in parent2:
            if gene not in child:
                while child[fill_pos] is not None:
                    fill_pos += 1
                child[fill_pos] = gene

        return child

    def __selection(self, population, tournaments_size=5):
        tournaments_size = min(tournaments_size, len(population) - 1)
        selected = random.sample(population, tournaments_size)
        fittest_population = min(selected, key=self.__fitness)
        return fittest_population
    
    def __mutate(self, individual):
        for i in range(len(individual)):
            if random.random() < self.MUTATION_RATE:
                swap_idx = random.randint(0, len(individual) - 1)
                individual[i], individual[swap_idx] = individual[swap_idx], individual[i]
        

    def __fitness(self, job: list[Job]):
        self._schedule(job)
        makespan = max(self.queues.values(), key=lambda q: q.last_task_due()).last_task_due()
        self._reset_machine_queues()
        return makespan

    def _reset_machine_queues(self):
        self.queues: dict[Machine: MachineQueue] = {m: MachineQueue(m) for m in self.machines}

    def __get_best_solution(self, population):
        return min(population, key=self.__fitness)

    def _geentic_algorithm(self, round=120):
        population = self.__initial_poplutation()
        best_solution = self.__get_best_solution(population)
        for _ in range(round):
            new_population = list()
            for _ in range(len(population) // 2):
                parent1 = self.__selection(population)
                parent2 = self.__selection(population)

                child1 = self.__crossover(parent1, parent2)
                child2 = self.__crossover(parent2, parent1)

                self.__mutate(child1)
                self.__mutate(child2)

                new_population.extend([child1, child2])
            population = new_population
            current_best = self.__get_best_solution(population)
            best_solution = min(best_solution, current_best, key=self.__fitness)
            # print(f'Generation {best_solution}: Best Fitness = {self.__fitness(best_solution)}')
        return best_solution

    def get_machine_order(self) -> list[Machine]:
        return self.machines
