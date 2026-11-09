"""Stand-in for the arrow package, which inform imports at the top but uses
only to time-stamp a log file (inform.get_datetime). The NestedText loader
never calls it, so this stub only has to make the import succeed."""


def now():
    raise NotImplementedError("arrow is not vendored")
