import math


def is_prime(n):
    """Verifica si un número es primo."""
    if n <= 1:
        return False
    for i in range(2, int(math.sqrt(n) + 1)):
        if n % i == 0:
            return False
    return True


def main():
    """Tiene toda la lógica principal."""
    for i in range(100):
        if is_prime(i):
            print(i, end=' ')
    print()


def my_func(e):
    """Una función que retorna la longitud del valor."""
    return len(e)


def sort_cars_by_length():
    """Ordena los autos por longitud de nombre en orden descendente."""
    cars = ['Ford', 'Mitsubishi', 'BMW', 'VW']
    cars.sort(reverse=True, key=my_func)
    print(cars)


if __name__ == '__main__':
    main()
    sort_cars_by_length()
