import os


def get_root_path():
    """Trả về đường dẫn đến thư mục chứa project."""
    root_path = os.path.dirname(os.path.realpath(__file__))
    return root_path


def get_parent_root_path():
    """Trả về đường dẫn đến thư mục cha của thư mục chứa project."""
    root_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    return root_path
