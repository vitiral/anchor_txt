# anchor_txt: attributes in markdown
#
# Copyright (C) 2019 Rett Berg <github.com/vitiral>
#
# The source code is Licensed under either of
#
# * Apache License, Version 2.0, ([LICENSE-APACHE](LICENSE-APACHE) or
#   http://www.apache.org/licenses/LICENSE-2.0)
# * MIT license ([LICENSE-MIT](LICENSE-MIT) or
#   http://opensource.org/licenses/MIT)
#
# at your option.
#
# Unless you explicitly state otherwise, any contribution intentionally submitted
# for inclusion in the work by you, as defined in the Apache-2.0 license, shall
# be dual licensed as above, without any additional terms or conditions.
"""Utility functions."""
from __future__ import unicode_literals
import six
from six import PY2


def update_dict(first, second):
    """Recursivly update the first dict inplace with the items from second.

    Throw a ValueError if any of the keys are already in first.
    """
    second = to_unicode_recurse(second)
    invalid = []
    for key, value in six.iteritems(second):
        if key in first:
            invalid.append(key)
        else:
            first[key] = value

    if invalid:
        raise ValueError("Keys already exist: {}".format(invalid))


def to_unicode_recurse(value):
    """Ensure that all text values are unicode."""
    if not PY2:
        return value
    if isinstance(value, list):
        return [to_unicode_recurse(v) for v in value]
    if isinstance(value, dict):
        return {
            to_unicode(key): to_unicode_recurse(value)
            for key, value in six.iteritems(value)
        }

    return to_unicode(value)


def to_unicode(value):
    """Ensure that the value, if text, is unicode."""
    if not PY2:
        return value
    if isinstance(value, str):
        value = value.decode('utf-8')
    return value
