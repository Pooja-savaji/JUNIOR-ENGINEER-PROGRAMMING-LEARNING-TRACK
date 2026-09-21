"""Visual Pattern Generation in Python (Beginner Friendly).

Demonstrates nested loops (outer loop for rows, inner loop for columns)
to create classic geometric and numeric patterns.
"""


def star_right_triangle(rows: int = 5):
    """Prints a right-angled star triangle:
    *
    **
    ***
    ****
    *****
    """
    print(f"\n1. Right-Angled Star Triangle ({rows} rows):")
    for i in range(1, rows + 1):
        print("*" * i)


def number_triangle(rows: int = 5):
    """Prints a triangle with increasing numbers per row:
    1
    2 2
    3 3 3
    4 4 4 4
    5 5 5 5 5
    """
    print(f"\n2. Repeating Number Triangle ({rows} rows):")
    for i in range(1, rows + 1):
        print(f"{i} " * i)


def counting_triangle(rows: int = 5):
    """Prints counting numbers per row:
    1
    1 2
    1 2 3
    1 2 3 4
    1 2 3 4 5
    """
    print(f"\n3. Counting Number Triangle ({rows} rows):")
    for i in range(1, rows + 1):
        for j in range(1, i + 1):
            print(j, end=" ")
        print()  # Newline after each row


def inverted_triangle(rows: int = 5):
    """Prints an inverted star triangle:
    *****
    ****
    ***
    **
    *
    """
    print(f"\n4. Inverted Triangle ({rows} rows):")
    for i in range(rows, 0, -1):
        print("*" * i)


def star_pyramid(rows: int = 5):
    """Prints a centered star pyramid:
        *
       ***
      *****
     *******
    *********
    """
    print(f"\n5. Centered Star Pyramid ({rows} rows):")
    for i in range(1, rows + 1):
        spaces = " " * (rows - i)
        stars = "*" * (2 * i - 1)
        print(spaces + stars)


def diamond_pattern(rows: int = 5):
    """Prints a diamond star pattern."""
    print(f"\n6. Diamond Pattern (size {rows}):")
    # Top half
    for i in range(1, rows + 1):
        spaces = " " * (rows - i)
        stars = "*" * (2 * i - 1)
        print(spaces + stars)
    # Bottom half
    for i in range(rows - 1, 0, -1):
        spaces = " " * (rows - i)
        stars = "*" * (2 * i - 1)
        print(spaces + stars)


def floyds_triangle(rows: int = 4):
    """Prints Floyd's continuous counting triangle:
    1
    2 3
    4 5 6
    7 8 9 10
    """
    print(f"\n7. Floyd's Triangle ({rows} rows):")
    num = 1
    for i in range(1, rows + 1):
        for _ in range(i):
            print(f"{num:2d}", end=" ")
            num += 1
        print()


def hollow_square(size: int = 5):
    """Prints a hollow square border:
    * * * * *
    *       *
    *       *
    *       *
    * * * * *
    """
    print(f"\n8. Hollow Square ({size}x{size}):")
    for row in range(size):
        for col in range(size):
            if row == 0 or row == size - 1 or col == 0 or col == size - 1:
                print("*", end=" ")
            else:
                print(" ", end=" ")
        print()


def run_all_patterns():
    print("=" * 50)
    print("         ✨ PATTERN GENERATION DEMO            ")
    print("=" * 50)

    star_right_triangle(5)
    number_triangle(5)
    counting_triangle(5)
    inverted_triangle(5)
    star_pyramid(5)
    diamond_pattern(4)
    floyds_triangle(4)
    hollow_square(5)


if __name__ == "__main__":
    run_all_patterns()
