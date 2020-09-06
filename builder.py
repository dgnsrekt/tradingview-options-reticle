from jinja2 import Environment, FileSystemLoader
from decouple import config
from options_reticle.paths import PROJECT_ROOT_PATH
from options_reticle.ticker import Watchlist
from options_reticle.emoji import create_emojis
from pprint import pprint


# TODO: add quick flip action as a builder option
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

watchlist_output_path = PROJECT_ROOT_PATH / "watchlist.json"
assert watchlist_output_path.exists()  # check and raise
watchlist = Watchlist.parse_file(watchlist_output_path)
# watchlist.watchlist = watchlist.watchlist[:225]

option_function = environment.get_template("option_function.pine")
watchlist.create_return_data()

output = option_function.render(watchlist.dict())
print(output)

reticle = environment.get_template("reticle.pine")
output = reticle.render()
print(output)

fill = environment.get_template("fill.pine")
output = fill.render()
print(output)

itm_emojis, otm_emojis = create_emojis()
emoji = environment.get_template("emoji.pine")
output = emoji.render(itm=itm_emojis, otm=otm_emojis)
print(output)
print()

label = environment.get_template("label.pine")
output = label.render()
print(output)
