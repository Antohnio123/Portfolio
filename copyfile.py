import os

def copyfile (source, destination):
    """A custom fuction to copy a file"""
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
        print('Файл назначения уже существует, менять его мы не уполномочены, программа закрывается')
        exit()

    with open(source, "rb") as Sfile:
        r = Sfile.readlines()
        with open(destination, "wb") as Dfile:
            Dfile.writelines(r)

