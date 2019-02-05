# coding=utf-8
from urllib.parse import urljoin

from pulp_smash.constants import PULP_FIXTURES_BASE_URL
from pulp_smash.pulp3.constants import (
    BASE_PUBLISHER_PATH,
    BASE_REMOTE_PATH,
    CONTENT_PATH
)

# FIXME: list any download policies supported by your plugin type here.
# If your plugin supports all download policies, you can import this
# from pulp_smash.pulp3.constants instead.
# DOWNLOAD_POLICIES = ['immediate', 'streamed', 'on_demand']
DOWNLOAD_POLICIES = ['immediate']

# FIXME: replace 'unit' with your own content type names, and duplicate as necessary for each type
SHELTER_CONTENT_NAME = 'shelter.unit'

# FIXME: replace 'unit' with your own content type names, and duplicate as necessary for each type
SHELTER_CONTENT_PATH = urljoin(CONTENT_PATH, 'shelter/units/')

SHELTER_REMOTE_PATH = urljoin(BASE_REMOTE_PATH, 'shelter/shelter/')

SHELTER_PUBLISHER_PATH = urljoin(BASE_PUBLISHER_PATH, 'shelter/shelter/')


# FIXME: replace this with your own fixture repository URL and metadata
SHELTER_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, 'shelter/')

# FIXME: replace this with the actual number of content units in your test fixture
SHELTER_FIXTURE_COUNT = 3

SHELTER_FIXTURE_SUMMARY = {
    SHELTER_CONTENT_NAME: SHELTER_FIXTURE_COUNT
}

# FIXME: replace this with the location of one specific content unit of your choosing
SHELTER_URL = urljoin(SHELTER_FIXTURE_URL, '')

# FIXME: replace this iwth your own fixture repository URL and metadata
SHELTER_LARGE_FIXTURE_URL = urljoin(PULP_FIXTURES_BASE_URL, 'shelter_large/')

# FIXME: replace this with the actual number of content units in your test fixture
SHELTER_LARGE_FIXTURE_COUNT = 25
