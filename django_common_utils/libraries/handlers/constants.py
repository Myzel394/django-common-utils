from ..typings import Kwargs
from ..utils import EnsureIterationDictType

__all__ = [
    "HandleOn", "TextOptimizerDefault", "HTMLOptimizerDefault",
    "AddAttributesDict", "UnwrapDict"
]

AddAttributesDict = EnsureIterationDictType[
    str, EnsureIterationDictType[str, str]
]

UnwrapDict = EnsureIterationDictType[str, str]


class HandleOn:
    SAVE = "SAVE"
    CREATION = "CREATION"
    DELETION = "DELETION"


class TextOptimizerDefault:
    space_after: str = r".,!?:;)+*&§%|\/\\"
    space_before: str = r"\(+*&%#$|\/\\"
    no_space_before: str = "?!.,`':;-"
    no_space_after: str = "-#"
    ignore_for_digits: str = ".,"


class HTMLOptimizerDefault:
    unwrap: UnwrapDict = {
        ("p",): {"img", "table"}
    }
    add_attributes: AddAttributesDict = {
        "img": {
            "loading": "lazy"
        },
        "a": {
            "rel": "noopener noreferrer"
        }
    }
