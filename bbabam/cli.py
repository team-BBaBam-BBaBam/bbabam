import argparse

import bbabam.bbabam as bbabam


def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--user_input", type=str, default=None)
    args = argparser.parse_args()

    user_input = args.user_input
    if user_input is None:
        user_input = input("검색어를 입력하세요: ")

    bbabam.run_bbabam(user_input)
