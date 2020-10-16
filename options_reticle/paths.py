from pathlib import Path
from appdirs import user_data_dir

SOURCE_ROOT_PATH = Path(__file__).parent

PROJECT_ROOT_PATH = SOURCE_ROOT_PATH.parent

USER_DIRECTORY = Path(user_data_dir("options_reticle", "dgnsrket"))
