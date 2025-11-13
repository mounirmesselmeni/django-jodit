import importlib.metadata

__author__ = """Mounir Messelmeni"""
__email__ = "messelmeni.mounir@gmail.com"

try:
    __version__ = importlib.metadata.version("django_jodit")
except importlib.metadata.PackageNotFoundError:
    __version__ = "0.1.0"
