import os
import random
import re

root_dir = "data"
files = os.listdir(root_dir)
for file in files:
    with open(os.path.join(root_dir, file), "r") as f:
        lines = f.read().split("\n")
        print(f"{file}: {len(lines)}")


def get_random_value(file: str, n: int = 1, allow_duplicates: bool = False) -> str:
    with open(os.path.join(root_dir, file), "r") as f:
        lines = f.read().split("\n")
        if allow_duplicates:
            results = random.sample(lines, n)
        else:
            assert len(lines) >= n, f"Cannot generate {n} unique values from list of {len(lines)}"
            results = set()
            while len(results) < n:
                results.add(random.sample(lines, 1)[0])
    if n == 1:
        return list(results)[0]
    else:
        return list(results)


def get_templated_string(text: str, n: int = 1, allow_duplicates: bool = False) -> str:
    if allow_duplicates:
        results = []
    else:
        results = set()
    tags = re.findall("\{(.+?)\}", text)
    # TODO check permutation count vs n
    while len(results) < n:
        working_text = text
        for tag in tags:
            try:
                value = get_random_value(f"{tag}.txt")
            except FileNotFoundError:
                # make plural if singular
                value = get_random_value(f"{tag}s.txt")
            working_text = working_text.replace("{" + f"{tag}" + "}", value, 1)
        if allow_duplicates:
            results.append(working_text)
        else:
            results.add(working_text)
    if n == 1:
        return list(results)[0]
    else:
        return list(results)


if __name__ == "__main__":
    get_templated_string("{actions}-{adjectives}-{animals}-{colors}-{nouns}-{sportsgames}-{transportwords}-{verbs}")

    get_templated_string("e-{verb}-{noun}", 10)
