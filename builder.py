from jinja2 import Environment, FileSystemLoader
from decouple import config

file_loader = FileSystemLoader("templates")
environment = Environment(loader=file_loader)

head = environment.get_template("head.pine")

TITLE = "FOMO DRIVEN DEVELOPMENT OPTIONS RETICLE"
SHORT_TITLE = "[FDD] OPTIONS RETICLE"

head_arguments = {"title": TITLE, "short_title": SHORT_TITLE}
output = head.render(**head_arguments)
print()
print(output)
print()

vars = environment.get_template("variables.pine")
output = vars.render()

print(output)
print()
