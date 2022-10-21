from math import sqrt

m = 0

lists = []


def mediana(a, b, c):
    global m
    if m == 2:
        print(f"x={lists[-3]}, y={lists[-2]}, z={lists[-1]}")
        return ""
    else:
        x = sqrt(2 * b * b + 2 * c * c - a * a) / 2
        y = sqrt(2 * a * a + 2 * c * c - b * b) / 2
        z = sqrt(2 * b * b + 2 * a * a - c * c) / 2
        lists.append(x)
        lists.append(y)
        lists.append(z)
        if x + y > z and y + z > x and x + z > y:
            m += 1
            return mediana(x, y, z)
        else:
            m += 1
            print("Bla bla bar go")


print(mediana(5, 12, 13))
