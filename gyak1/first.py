a = [1, 2, 3, 8, 3]
print(sorted(a, reverse=True))


def is_leap_year(num):
    return (num % 4 == 0) and not (num % 100 == 0 and num % 400 != 0)


print(list(map(is_leap_year, [1986, 2000, 2003])))
