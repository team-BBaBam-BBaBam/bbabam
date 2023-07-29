# Example Command
# python test\restriction_information_test.py --gpt3 --user_input "top 5 restaurants in seoul except noodle"


if __name__ == "__main__":
    import sys
    import os
    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    sys.path.append(parent)

from bbabam.settings.openai_lm import CHATGPT_4_MODEL_STABLE, CHATGPT_3_MODEL_STABLE
from bbabam.models.restriction_information_generation import RestrictionInformationGenerator
import time
from yaspin import yaspin
from colorama import Fore, Style


def test_restriction_gen(user_input, gpt3=False):
    if user_input is None:
        user_input = "top 5 restaurants in seoul except noodle"

    res_inform_gen = RestrictionInformationGenerator(use_gpt3=gpt3)

    # Show Loading Spinner
    with yaspin(text="Generating...", spinner="dots") as spinner:
        s_time = time.time()
        restriction = res_inform_gen.generate_restriction(user_input)
        e_time = time.time()
        spinner.ok("✔")

    # Print Result
    print()
    print(Fore.GREEN + "Time Elapsed: " +
          Fore.RESET, e_time - s_time, "seconds")
    print(Fore.BLUE + "User Input:" + Fore.RESET, user_input)
    print(Fore.YELLOW + "Used Model:" + Fore.RESET,
          CHATGPT_3_MODEL_STABLE if gpt3 else CHATGPT_4_MODEL_STABLE)
    print()
    print(Fore.RED + "Generated Output: \n" + Fore.RESET, restriction)
    print(Style.RESET_ALL)


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--user_input", type=str, default=None)
    parser.add_argument("--gpt3", action="store_true")
    args = parser.parse_args()

    test_restriction_gen(args.user_input, args.gpt3)
