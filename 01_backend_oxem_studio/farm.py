from abc import ABC, abstractmethod
from collections import defaultdict
from typing import Dict, List, Union
import random


class Animal(ABC):
    def __init__(self, animal_id: str):
        self.id = animal_id
    
    @abstractmethod
    def collect_product(self) -> Union[int, float]:
        pass
    
    @abstractmethod
    def get_product_type(self) -> str:
        pass
    
    @abstractmethod
    def get_animal_type(self) -> str:
        pass


class Cow(Animal):
    def collect_product(self) -> int:
        return random.randint(8, 12)
    
    def get_product_type(self) -> str:
        return "milk"
    
    def get_animal_type(self) -> str:
        return "cow"


class Chicken(Animal):
    def collect_product(self) -> int:
        return random.randint(0, 1)
    
    def get_product_type(self) -> str:
        return "eggs"
    
    def get_animal_type(self) -> str:
        return "chicken"


class Farm:
    def __init__(self):
        self._animals: Dict[str, List[Animal]] = defaultdict(list)
        self._animal_counters: Dict[str, int] = defaultdict(int)
    
    def add_animal(self, animal: Animal) -> None:
        animal_type = animal.get_animal_type()
        self._animals[animal_type].append(animal)
        self._animal_counters[animal_type] += 1
    
    def add_animals(self, animals: List[Animal]) -> None:
        for animal in animals:
            self.add_animal(animal)
    
    def get_animal_count(self) -> Dict[str, int]:
        return dict(self._animal_counters)
    
    def collect_products(self) -> Dict[str, Union[int, float]]:
        products = defaultdict(int)
        for animals in self._animals.values():
            for animal in animals:
                products[animal.get_product_type()] += animal.collect_product()
        return dict(products)


def generate_unique_id(animal_type: str, counter: int) -> str:
    return f"{animal_type[0].upper()}{counter:04d}"


def create_initial_animals() -> List[Animal]:
    animals = []
    for i in range(1, 11):
        animals.append(Cow(generate_unique_id("cow", i)))
    for i in range(1, 21):
        animals.append(Chicken(generate_unique_id("chicken", i)))
    return animals