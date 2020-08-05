from typing import List
from operator import itemgetter


def get_top(data: List[dict]) -> dict:
  """Finds the best students in each course.
  :data: a list of dictionaries, that looks like {'name': 'any', 'rate': any, 'course':'any'}. """
  # d = {}
  # for element in sorted(data.copy(), key=itemgetter('course', 'rate')):
  #   if element['course'] not in d.items():
  #     d.update({element['course']: element['name']})
  return {el['course']: el['name'] for el in sorted(data.copy(), key=itemgetter('course', 'rate'))}


marks = [
  {'name':'Alexey', 'rate': 3, 'course': 'Python'},
  {'name': 'Andrew', 'rate': 5, 'course': 'Python'},
  {'name': 'John', 'rate': 2, 'course': 'Russian'},
  {'name': 'Maria', 'rate': 5, 'course': 'Russian'},
  {'name': 'Jimmy', 'rate': 5, 'course': 'C#'},
  {'name': 'Maria', 'rate': 4, 'course': 'C#'},
  {'name': 'Karl', 'rate': 3, 'course': 'Python'}
]
print(sorted(marks.copy(), key=itemgetter('course', 'rate'), reverse=True))
print(get_top(marks))



# В комментах код, который сначала сделал через for.  А потом его уже упаковал по-функциональному )))