# Запускать будучи в папке CeleryApp строкой:
# python -m celery -A HW11Celery worker -P gevent
# и в другом окне терминала запустить периодическую задачу:
# celery -A HW11Celery beat
from celery import Celery
import datetime
from urllib import request as ureq


app = Celery('HW11Celery', broker='amqp://guest@localhost//')
app.conf.CELERY_RESULT_BACKEND='amqp://'
t = 5           # время перепроверки погоды в секундах
web_site = 'https://www.meteoservice.ru/weather/now/nizhniy-novgorod'


@app.task
def weather():
    """Парсер сайта погоды. Считывает погоду с указанного сайта. Можно прееделать под api."""
    req = ureq.Request(web_site)
    response = ureq.urlopen(req)
    web_page = str(response.read().decode('utf-8'))
    Ind1 = web_page.index('<div class="small-6 medium-6 large-4 columns text-center">') + 113
    Ind1_1 = web_page[Ind1:].index('&deg;</span>') + Ind1
    t1 = web_page[Ind1:Ind1_1]
    Ind2 = web_page.index('<p class="margin-bottom-0">') + 27
    Ind2_1 = web_page[Ind2:].index('</p>') + Ind2
    t2 = web_page[Ind2:Ind2_1]
    result = 'В Нижнем Новгороде на ' + str(datetime.datetime.now().ctime()) + \
             ' температура равна: ' + str(t1) + ' по Цельсию. ' + str(t2) + '. (Предоставлено Meteoservice.ru)\n'
    print(result)

    with open('weatherNNlog.txt', 'a', encoding='utf-8') as log:
        log.write(result)
    return result


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """Создает периодическую таску."""
    # Calls weather() every t seconds.
    sender.add_periodic_task(t, weather.s(), name='Get weather.')


if __name__ == '__main__':
    # app.start()
    app.worker_main()