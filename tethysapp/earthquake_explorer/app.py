from tethys_sdk.components import ComponentBase


class App(ComponentBase):
    """
    Tethys app class for Earthquake Explorer.
    """

    name = "Earthquake Explorer"
    description = "a web app that shows recent earthquakes on an interactive map"
    package = "earthquake_explorer"  # WARNING: Do not change this value
    index = "home"
    icon = f"{package}/images/icon.png"
    root_url = "earthquake-explorer"
    color = "#16a085"
    tags = ""
    enable_feedback = False
    feedback_emails = []
    exit_url = "/apps/"
    default_layout = "NavHeader"
    nav_links = "auto"


@App.page
def home(lib):
    return lib.tethys.Display(
        lib.tethys.Map()
    )