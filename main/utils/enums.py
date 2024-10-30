import enum


class NewEnumMeta(type):

    def __new__(cls, name, bases, attrs):
        mappings = dict()
        values = list()
        for k, v in attrs.items():
            if k.startswith("__") and k.endswith("__"):
                continue
            mappings[k] = v
            values.append(v)
        for k in mappings.keys():
            attrs.pop(k)
        attrs["__values__"] = values
        attrs["__mappings__"] = mappings
        return type.__new__(cls, name, bases, attrs)

    def __contains__(cls, val):
        if val in cls.__values__:
            return True
        return False

    def __getattr__(cls, item):
        return cls.__mappings__[item]

    def __iter__(cls):
        for val in cls.__values__:
            yield val

    def help_text(self):
        items = []
        for key, val in self.__mappings__.items():
            items.append(f"{key}: {val}")
        return ", ".join(items)


class NewEnum(object, metaclass=NewEnumMeta):
    pass


class ParagraphStatus(NewEnum):
    UNKNOWN = 0
    POSITIVE = 1
    NEGTIVE = -1
