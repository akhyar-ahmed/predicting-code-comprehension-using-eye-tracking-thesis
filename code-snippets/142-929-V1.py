# https://raw.githubusercontent.com/ansible/ansible/devel/test/lib/ansible_test/_internal/cli/converters.py
def key_value_type(value):  # type: (str) -> t.Tuple[str, str]
    """Wrapper around key_value."""
    return key_value(value)


def key_value(value):  # type: (str) -> t.Tuple[str, str]
    """Type parsing and validation for argparse key/value pairs separated by an '=' character."""
    parts = value.split('=')

    if len(parts) != 2:
        raise argparse.ArgumentTypeError('"%s" must be in the format "key=value"' % value)

    return parts[0], parts[1]
# # # # # delimiter # # # # # # #
print(key_value_type("x=test"))
