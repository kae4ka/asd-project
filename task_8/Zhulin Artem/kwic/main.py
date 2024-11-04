def main():
    lines = input_filter()
    lines = circular_shit_filter(lines)
    lines = alphabetizer_filter(lines)
    output_filter(lines)


def input_filter() -> list[str]:
    while True:
        input_line = input("Enter text (empty line to stop): ").strip()

        if input_line == '':
            break

        yield input_line.strip()


def circular_shit_filter(input_lines: list[str]) -> list[str]:
    for line in input_lines:
        words = line.split()
        for index in range(len(words)):
            yield ' '.join(words[index:] + words[:index])


def alphabetizer_filter(input_lines: list[str]) -> list[str]:
    return sorted(input_lines)


def output_filter(input_lines: list[str]):
    for line in input_lines:
        print(line)


if __name__ == '__main__':
    main()
