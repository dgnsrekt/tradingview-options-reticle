"""This module build the emotional status bars."""


def create_emojis():
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
