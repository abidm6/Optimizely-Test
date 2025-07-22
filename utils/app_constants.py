"""
Provides paths for various resource under resource folder.
"""
from os.path import dirname, join


class AppConstant:
    """
    Used for storing constants.
    """
    PROJECT_ROOT = dirname(dirname(__file__))
    RESOURCE_FOLDER = join(PROJECT_ROOT, 'resources')
    SYSTEM_CONFIG = join(RESOURCE_FOLDER, 'system.properties')