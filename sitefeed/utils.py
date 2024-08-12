from collections.abc import Mapping
from typing import Any, Type, TypedDict, TypeVar, cast

Options = TypeVar("Options", bound=TypedDict)


def extract_options(
    prefix: str, mapping: Mapping[str, Any], type_: Type[Options]
) -> Options:
    options = {}
    for key in type_.__required_keys__:
        options[key] = mapping[f"{prefix}{key}"]
    for key in type_.__optional_keys__:
        prefixed_key = f"{prefix}{key}"
        if prefixed_key in mapping:
            options[key] = mapping[prefixed_key]
    return cast(type_, options)
