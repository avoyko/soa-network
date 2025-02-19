import pathlib

import pytest

pytest_plugins = ['pytest_userver.plugins.core']

USERVER_CONFIG_HOOKS = ['userver_actions_service']


@pytest.fixture(scope='session')
def service_source_dir():
    """Path to root directory service."""
    return pathlib.Path(__file__).parent.parent


@pytest.fixture(scope='session')
def userver_actions_service(mockserver_info):
    def do_patch(config_yaml, config_vars):
        components = config_yaml['components_manager']['components']
        components['network-users-client']['service-url'] = mockserver_info.url(
            'http://network-users.net',
        )

    return do_patch