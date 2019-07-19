from __future__ import unicode_literals


def update_dict(first, second):
    """Recursivly update the first dict inplace with the items from second.

    Throw a ValueError if any of the keys are already in first.
    """
    second = to_unicode_recurse(second)
    invalid = []
    for key, value in second.items():
        if key in first:
            invalid.append(key)
        else:
            first[key] = value

    if invalid:
        raise ValueError("Keys already exist: {}".format(invalid))


def to_unicode_recurse(value):
    if isinstance(value, list):
        return [to_unicode_recurse(v) for v in value]
    elif isinstance(value, dict):
        return {
            to_unicode(key): to_unicode_recurse(value)
            for key, value in value.items()
        }
    else:
        return to_unicode(value)


def to_unicode(value):
    if isinstance(value, str):
        value = value.decode('utf-8')
    return value
