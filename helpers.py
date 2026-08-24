from pathlib import Path


def get_float(prompt, default):
    value = input(f"{prompt} [{default}]: ").strip()

    if not value:
        return default

    try:
        return float(value)
    except ValueError:
        print(f"Invalid number. Using default: {default}")
        return default


def get_int(prompt, default):
    value = input(f"{prompt} [{default}]: ").strip()

    if not value:
        return default

    try:
        return int(value)
    except ValueError:
        print(f"Invalid number. Using default: {default}")
        return default


def get_output_path(prompt, default, results_dir, root_dir):
    value = input(f"{prompt} [{default}]: ").strip()

    if not value:
        return Path(default)

    path = Path(value)

    if path.is_absolute():
        return path

    if len(path.parts) == 1:
        return results_dir / path

    return root_dir / path


def get_input_path(prompt, default, root_dir):
    value = input(f"{prompt} [{default}]: ").strip()

    if not value:
        return Path(default)

    path = Path(value)

    if path.is_absolute():
        return path

    return root_dir / path


def print_result(result, csv_columns):
    print("\n" + "=" * 80)
    print("SCRAPING RESULT")
    print("=" * 80)

    for field in csv_columns:
        print(f"{field}: {result.get(field, 'N/A')}")

    print("=" * 80)


def print_royalroad_result(result, csv_columns):
    print("\n" + "=" * 80)
    print("SCRAPING RESULT")
    print("=" * 80)

    for field in csv_columns:
        print(f"{field}: {result.get(field, 'N/A')}")

    print("=" * 80)
