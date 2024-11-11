class Filter:
    def execute(self, input_lines: list[str]) -> list[str]:
        pass


class ReadFilter(Filter):
    def execute(self, input_lines: list[str]) -> list[str]:
        return [line.strip() for line in input_lines]


class CircularShiftFilter(Filter):
    def execute(self, input_lines: list[str]) -> list[str]:
        for line in input_lines:
            words = line.split()
            for index in range(len(words)):
                yield ' '.join(words[index:] + words[:index])


class AlphabetizerFilter(Filter):
    def execute(self, input_lines: list[str]) -> list[str]:
        return sorted(input_lines)


class OutputFilter(Filter):
    def execute(self, input_lines: list[str]) -> list[str]:
        return input_lines


class Pipe:
    def __init__(self):
        self.filters: list[Filter] = []

    def add(self, new_filter: Filter):
        self.filters.append(new_filter)
        return self

    def execute(self, input_lines: list[str]) -> list[str]:
        for executable_filter in self.filters:
            input_lines = executable_filter.execute(input_lines)

        return input_lines


def main():
    pipe = Pipe()
    pipe.add(ReadFilter()).add(CircularShiftFilter()).add(AlphabetizerFilter()).add(OutputFilter())

    lines = user_input()
    lines = pipe.execute(lines)
    user_output(lines)


def user_input() -> list[str]:
    while True:
        input_line = input("Enter text (empty line to stop): ").strip()

        if input_line == '':
            break

        yield input_line


def user_output(lines: list[str]):
    for line in lines:
        print(line)


if __name__ == '__main__':
    main()
