"""This module cleans the data about how the subway stations are connected."""
import csv


def clean_metro_lines(metro_lines_file: str) -> None:
    """Cleans the metro_line file"""
    with open(metro_lines_file) as file:
        a = csv.reader(file)
        new_data = []
        for row in a:
            new_data.append([int(row[0]), int(row[1]), int(row[2])])

    with open(metro_lines_file, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(new_data)


if __name__ == "__main__":
    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['csv'],  # the names (strs) of imported modules
        'allowed-io': ['clean_metro_lines'],
        'max-line-length': 100,
        'disable': ['E1136']
    })

    import python_ta.contracts
    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()
