import os
import copyfile


def copydir(source, destination):
    """A custom function to copy a folder with subfolders and files inside.
    Uses our custom copyfile function."""
    class NoSourceExeption(Exception):
        pass
    def sourcecheck(source):
        if not os.path.exists(source):
            raise NoSourceExeption()
    class DestExeption(Exception):
        pass
    def destcheck(destination):
        if os.path.exists(destination):
            raise DestExeption()
    try:
        sourcecheck(source)
        destcheck(destination)
    except NoSourceExeption:
        print('Источника не существует, программа закрывается')
        exit()
    except DestExeption:
        print('Папка назначения уже существует, менять её мы не уполномочены, программа закрывается')
        exit()

    L=os.walk(source, topdown=True)
    L=list(L)                               # Очень важно! Превращаем генератор os.walk в итерируемый лист? в самом генераторе нельзя использовать os.chdir, а в листе можно
    os.mkdir(destination)
    FullDest=os.path.abspath(destination)           # получаем абсолютный путь для папки назначения
    FullSource = os.path.abspath(source)
    for d in L:
        print(d[0])
        destD = d[0].split(source)[1]                # Находим подпуть подпапки в source (обрезая source)
        os.chdir(os.path.join(FullDest, destD))            # Находим путь, соответствующий подпапке в source, но в destination
        for i in d[1]:                      # Работает! несколько папок в одной создается
            os.mkdir(i)
        os.chdir(FullSource)                            # Эта строка нужна, так как следущий os.chdir без этого не сработает
        os.chdir(os.path.abspath(destD))
        for k in d[2]:
            destF = os.path.join(d[0], k).split(source)[1]
            copyfile.copyfile(k, os.path.join(FullDest, destF))


s = "Testdir2\\"
d = 'DestDir\\'
copydir(s, d)