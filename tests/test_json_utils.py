import importlib.util
import sys
import types
from pathlib import Path


def load_json_utils():
    base = Path(__file__).resolve().parents[1] / 'voyager' / 'utils'

    if 'voyager' not in sys.modules:
        sys.modules['voyager'] = types.ModuleType('voyager')
    if 'voyager.utils' not in sys.modules:
        utils_pkg = types.ModuleType('voyager.utils')
        sys.modules['voyager.utils'] = utils_pkg
    else:
        utils_pkg = sys.modules['voyager.utils']

    if 'voyager.utils.file_utils' not in sys.modules:
        spec_fu = importlib.util.spec_from_file_location('voyager.utils.file_utils', base / 'file_utils.py')
        file_utils = importlib.util.module_from_spec(spec_fu)
        spec_fu.loader.exec_module(file_utils)
        sys.modules['voyager.utils.file_utils'] = file_utils
        utils_pkg.file_utils = file_utils

    spec_j = importlib.util.spec_from_file_location('voyager.utils.json_utils', base / 'json_utils.py')
    json_utils = importlib.util.module_from_spec(spec_j)
    spec_j.loader.exec_module(json_utils)
    return json_utils


json_utils = load_json_utils()


def test_missing_closing_brace():
    result = json_utils.fix_and_parse_json('{"a": 1')
    assert result == {"a": 1}


def test_unquoted_property_names():
    result = json_utils.fix_and_parse_json('{a: 1, b: 2}')
    assert result == {"a": 1, "b": 2}
