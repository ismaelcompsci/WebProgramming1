people = [
    {"name": "Harry", "house":"griff"},
    {"name": "zen", "house":"Griff"},
    {"name": "her", "house":"slyth"},
    {"name": "john", "house":"raven"}
]

people.sort(key=lambda person: person["name"])
print(people)