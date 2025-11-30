from argos import __version__
from argos.cli import ArgosInfo, build_parser, format_greeting, format_info, handle_args


def test_format_greeting_defaults_to_general_audience():
    assert format_greeting() == "Hello, there! Welcome to Argos."


def test_format_greeting_with_name():
    assert format_greeting("Ada") == "Hello, Ada! Welcome to Argos."


def test_format_info_uses_default_metadata():
    info_output = format_info()
    assert "Argos" in info_output
    assert __version__ in info_output


def test_handle_args_invokes_hello_command():
    parser = build_parser()
    args = parser.parse_args(["hello", "--name", "Ada"])
    assert handle_args(args) == "Hello, Ada! Welcome to Argos."


def test_handle_args_invokes_info_command():
    parser = build_parser()
    args = parser.parse_args(["info"])
    expected = format_info(ArgosInfo(name="Argos", version=__version__, description="Argos is a lightweight toolkit starter."))
    assert handle_args(args) == expected
