"""This module build the emotional status indicator."""

from typing import Iterable, Tuple


def create_emojis() -> Tuple[Iterable, Iterable]:
    """Create emotional status indicator."""
    itm = list(
        enumerate(
            ["🙂", "😀", "😃", "😄", "😁", "😆", "🥰", "😍", "🤩", "😛", "😜", "🤑", "😎", "🔥", "🎉", "🍾", "💯"]
        )
    )
    otm = list(
        enumerate(
            ["😐", "😔", "😒", "😞", "😟", "🙁", "😮", "🥺", "😳", "🤢", "🤮", "😵", "😭", "😠", "🤬", "💀", "💩"]
        )
    )
    return itm, otm
