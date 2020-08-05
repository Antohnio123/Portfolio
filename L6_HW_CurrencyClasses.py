# from abc import ABC
# from abc import abstractmethod
import functools


@functools.total_ordering
class Currency:
    """1 EUR = 2 USD = 100 RUB.
    В задаче не говорится про вычитание, поэтому оно не реализовано.
    Если вычитание понадобится, стоит перегрузить оператор __sub__ и __rsub__ по аналогии с __add__ и __radd__.
    Абстрактные методы не использовались, так как удлинняют код и не нужны там, где всё решается методами
    родительского класса."""
    name = 'у.е.'
    absolute_course = 1

    def __init__(self, value):
        self.value = value

    def __eq__(self, other) -> bool:
        return self.value*self.absolute_course == other.value*other.absolute_course

    def __lt__(self, other) -> bool:
        return self.value*self.absolute_course < other.value*other.absolute_course

    def __repr__(self):
        return str(self.value) + ' ' + self.name

    @classmethod
    def course(cls, other):
        return str(float(cls.absolute_course/other.absolute_course)) + ' '+other.name + ' for 1 '+ cls.name

    def to(self, other):
        """Возвращает новый объект класса other."""
        new = other((self.absolute_course/other.absolute_course)*self.value)
        return new

    def __add__(self, other):
        """Возвращает новый объект нашего класса с изменённым значением value."""
        if isinstance(other, Currency):
            new = self.__class__(self.value+(other.absolute_course/self.absolute_course)*other.value)
        elif isinstance(other, int) or isinstance(other, float):
            new = self.__class__(self.value + other)
        else:
            raise ValueError("The type "+ other.__class__.__name__ + " is not available for math operations")
        return new

    def __radd__(self, other):
        """Для функции sum нужно было сделать и radd, так как в ней первый элемент списка складывается с нулём справа."""
        return self + other



class Euro(Currency):
    name = 'EUR'
    absolute_course = 100


class Dollar(Currency):
    name = 'USD'
    absolute_course = 50


class Rubble(Currency):
    name = 'RUB'



print(
    f"Euro.course(Rubble)   ==> {Euro.course(Rubble)}\n"
    f"Dollar.course(Rubble) ==> {Dollar.course(Rubble)}\n"
    f"Rubble.course(Euro)   ==> {Rubble.course(Euro)}\n"
)

e = Euro(100)
r = Rubble(100)
d = Dollar(200)

print(
    f"e = {e}\n"
    f"e.to(Dollar) ==> {e.to(Dollar)}\n"
    f"e.to(Rubble) ==> {e.to(Rubble)}\n"
    f"e.to(Euro)   ==> {e.to(Euro)}\n"
)
print(
    f"r = {r}\n"
    f"r.to(Dollar) ==> {r.to(Dollar)}\n"
    f"r.to(Euro)   ==> {r.to(Euro)}\n"
    f"r.to(Rubble) ==> {r.to(Rubble)}\n"
)

print(
    f"e > r  ==> {e > r}\n"
    f"e == d ==> {e == d}\n"
)

print(
    f"e + r  =>  {e + r}\n"
    f"r + d  =>  {r + d}\n"
    f"d + e  =>  {d + e}\n"
    f"d + 20  =>  {d + 20}\n"
    f"d + 20  =>  {d + 20}\n"
)

print(sum([d]))
print([Euro(i) for i in range(5)])
print(sum([Euro(i) for i in range(5)]))

