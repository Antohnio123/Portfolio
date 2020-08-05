#  джуниор программист работает в нетфликс. он сделал массив из фильмов какие посмотрел пользователь "в лоб".
# то есть матрицу 10 тыс на 10 тыс (например)
# 1 - если юзер посмотрел этот фильм. 0 - если не посмотрел.
# задача:
# 1) сделать генератор такой матрицы
# 2) предложить структуру в какой хранить данные эффективно. много нулей в матрице - наверное не хорошо
# 3) скрипт который переводит данные из матрицы которую сделал наш джуниор в ваш формат
# чем короче код тем лучше
# простой скрипт (запускается в юпитере)


from scipy import sparse


films = ['Titanic', 'Avatar', 'Формула Любви', 'Гардемарины', 'American Beauty', 'War and Peace', 'Stranger']
users = {1: ['Titanic', 'Avatar'], 2: ['Формула', 'Avatar'], 3: ['Titanic', 'American Beauty'],
         4: ['Формула Любви', 'Гардемарины'], 5: ['Avatar', 'American Beauty'], 6: ['War and Peace', 'American Beauty'], 7: ['Гардемарины', 'Формула Любви']}



class Gen:
    def __init__(self):
        self.gen = ([1 if f in users[u] else 0 for u in users] for f in films)


compressed = [(i, j) for (i, row) in enumerate(list(Gen().gen)) for (j, x) in enumerate(row) if x == 1]


#  ТОЛЬКО для сравнения, так как sparce выдает координаты и значения, а нам значения не нужны
sparse_compressed = sparse.coo_matrix(list(Gen().gen))


if __name__ == "__main__":
    print(list(Gen().gen))
    print(sparse_compressed)
    print(compressed)





