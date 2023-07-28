# python test/chunk_divisor_test.py

if __name__ == "__main__":
    import sys
    import os
    current = os.path.dirname(os.path.realpath(__file__))
    parent = os.path.dirname(current)
    sys.path.append(parent)

from bbabam.modules.chunk_divisor import ChunkDivisor

from termcolor import colored


def main():
    # read text from bloc_content1.txt
    with open('test/blog_content1.txt', 'r', encoding='utf-8') as f:
        blog1 = f.read()

    data = [
        {
            "text": "Hello, I am a sample text for testing the ChunkDivisor class.",
            "link": "https://example.com/sample1"
        },
        {
            "text": blog1,
            "link": "https://blog.naver.com/eun417911/223129682887"
        }
    ]

    chunk_divisor = ChunkDivisor(isGpt3=False)

    divided_texts = chunk_divisor.divide_chunks(data, chunk_size=200)

    for text in divided_texts:
        print("Link: " + colored(f"{text['link']}", 'green'))
        print(
            "Total Token Count: " + colored(f"{text['total_token_count']}", 'blue'))
        print('')
        i = 0
        for chunk in text['chunks']:
            print(colored(
                f"Token Count: {chunk['token_count']}", 'yellow' if i % 2 == 0 else 'magenta'))
            print(colored(f"Text: ", 'yellow' if i %
                  2 == 0 else 'magenta') + chunk['text'])
            i += 1

        print('\n')


if __name__ == "__main__":
    main()
