import sys
import os

def resource_path(relative_path: str) -> str:
    """
    Get the absolute path to a resource, 
    whether running in a bundled exe or from source.
    """
    bundle_root = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
    return os.path.join(bundle_root, relative_path)