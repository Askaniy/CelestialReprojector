from math import sin, cos, tan, atan2, sqrt, hypot, degrees


# Sample implementation of the Bowring algorithm

def bowring(x, y, z, a, b):
    long = atan2(y, x)
    p = hypot(x, y)
    e1_2 = (a*a - b*b) / (a*a)
    e2_2 = (a*a - b*b) / (b*b)

    beta = a / b * z / p
    phi, phi0 = None, 0

    while phi0 != phi:
        phi0 = phi
        phi = atan2(z + b * e2_2 * sin(beta)**3, p - a * e1_2 * cos(beta)**3)
        beta = atan2(b * tan(phi), a)
        print(phi, beta)

    h = p / cos(phi) - a / sqrt(1 - e1_2 * sin(beta) ** 2)
    return long, phi, h


long, lat, hight = bowring(60, 60, 60, 66.854, 71.492) # parameters of Jupiter

print(f'long = {degrees(long)} deg, lat = {degrees(lat)} deg, hight = {hight} km')