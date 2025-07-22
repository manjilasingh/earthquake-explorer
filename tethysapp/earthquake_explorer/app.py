from tethys_sdk.base import TethysAppBase


class App(TethysAppBase):
    """
    Tethys app class for Earthquake Explorer.
    """
    name = 'Earthquake Explorer'
    description = ''
    package = 'earthquake_explorer'  # WARNING: Do not change this value
    index = 'home'
    icon = f'{package}/images/icon.gif'
    root_url = 'earthquake-explorer'
    color = '#718093'
    tags = ''
    enable_feedback = False
    feedback_emails = []
