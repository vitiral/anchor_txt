"""

```yaml @
a:
    - b
    - c
```

```yaml @
a:
    d: 2
    e: 3
```

"""

SINGLES = '__singles__'


def update_dict(first, second):
    """Recursivly update the first dict inplace with the items from second.

    Throw a ValueError if any of the keys are already in first.
    """
    invalid = []
    for key, value in second.items():
        if key in first:
            invalid.append(key)
        else:
            first[key] = value

    if invalid:
        raise ValueError("Keys already exist: {}".format(invalid))
