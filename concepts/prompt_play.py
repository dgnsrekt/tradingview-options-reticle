from bullet import Bullet, SlidePrompt, Check, Input, YesNo, Numbers, ScrollBar, VerticalPrompt
from bullet import styles
from bullet import colors
import pendulum

process_date = pendulum.now(tz="UTC")

ACCEPTABLE_MINIMUM_DAYS = [45, 60, 90, 120]

PROMPT_DEFAULT = {
    "indent": 0,
    "align": 5,
    "margin": 2,
    "shift": 0,
    "pad_right": 5,
    "background_color": colors.foreground["yellow"],
    "word_color": colors.bright(colors.foreground["yellow"]),
    "height": 5,
}


def title():
    print()
    print("[FDD] OPTIONS RETICLE TUNER")
    print()


def get_minimum_expiration():
    print("VERTICAL EXPIRATION ADJUSTMENT")
    print("What are the minimum days until expiration?")
    choices = [str(day) for day in ACCEPTABLE_MINIMUM_DAYS]
    prompt = ScrollBar(prompt="Minimum days: ", choices=choices, **PROMPT_DEFAULT)
    min_days = int(prompt.launch())
    min_expiration_date = process_date.add(days=min_days).date()
    print(f"Only expiration dates after {min_expiration_date} with be allowed.")
    return min_expiration_date


def get_search_method_priority():
    print("HORIZONTAL SEARCH PRIORITY")
    print("The tuner uses two seach methods to find options.")
    print(
        "The [PRICE SEARCH METHOD] looks for strike prices greater than n dollars out of the money."
    )
    print("The [DELTA SEARCH METHOD] looks for strike prices greater than the current ITM option.")
    print(
        "Both methods will be used. If a contract is not found using the primary method. The second method will be used to fallback on."
    )
    m_prompt = ScrollBar(
        prompt="Select priorty of the OTM Option search method: ",
        choices=["PRICE METHOD", "DELTA METHOD"],
        **PROMPT_DEFAULT,
        return_index=True,
    )

    results = m_prompt.launch()
    delta_method = True if int(results[-1]) else False

    if delta_method:
        print("[DELTA SEACH METHOD] has priority")
    else:
        print("[PRICE SEACH METHOD] has priority")
    return DELTA_METHOD_FIRST


title()
get_minimum_expiration()
get_search_method_priority()
exit()
d_prompt = ScrollBar(
    "[PRICE METHOD] Select minimum dollars OTM from the current price:",
    choices=[str(n) for n in range(1, 101)],
    **PROMPT_DEFAULT,
)

i_prompt = ScrollBar(
    "[DELTA METHOD] Select minimum delta OTM from the current ITM strike:",
    choices=[str(n) for n in range(1, 4)],
    **PROMPT_DEFAULT,
)
for p in [e_prompt, m_prompt, d_prompt, i_prompt]:
    p.launch()
