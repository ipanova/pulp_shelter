from pulpcore.plugin import PulpPluginAppConfig


class PulpShelterPluginAppConfig(PulpPluginAppConfig):
    """Entry point for the shelter plugin."""

    name = 'pulp_shelter.app'
    label = 'shelter'
