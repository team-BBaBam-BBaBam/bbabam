import argparse

import bbabam.bbabam as bbabam

def main():
    argparser = argparse.ArgumentParser()
    argparser.add_argument("--user_input", type=str, default=None)
    args = argparser.parse_args()

    result = bbabam.run_bbabam(args.user_input)