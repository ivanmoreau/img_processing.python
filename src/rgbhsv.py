import sys


def usage():
    print("Usage: python3 rgbhsv.py --rgb <r> <g> <b> or python3 rgbhsv.py --hsv <h> <s> <v>")


def to_hsv(r, g, b):
    cmax = max(r, g, b)
    cmin = min(r, g, b)
    chroma = cmax - cmin
    hue_ = None
    if chroma == 0:
        hue_ = 0
    elif cmax == r:
        hue_ = ((g - b) / chroma) % 6
    elif cmax == g:
        hue_ = ((b - r) / chroma) + 2
    elif cmax == b:
        hue_ = ((r - g) / chroma) + 4
    hue_ = hue_ * 60
    value = cmax
    saturation = None
    if value == 0:
        saturation = 0
    else:
        saturation = chroma / value
    return hue_, saturation, value


def to_rgb(h, s, v):
    chroma = s * v
    hue_ = h / 60
    x = chroma * (1 - abs((hue_ % 2) - 1))
    r, g, b = 0, 0, 0
    if 0 <= hue_ <= 1:
        r = chroma
        g = x
    elif 1 <= hue_ <= 2:
        r = x
        g = chroma
    elif 2 <= hue_ <= 3:
        g = chroma
        b = x
    elif 3 <= hue_ <= 4:
        g = x
        b = chroma
    elif 4 <= hue_ <= 5:
        r = x
        b = chroma
    elif 5 <= hue_ <= 6:
        r = chroma
        b = x
    m = v - chroma
    return r + m, g + m, b + m


def main():
    is_rgb = False
    values = []
    len_args = len(sys.argv)
    rgb = "--rgb"
    hsv = "--hsv"
    if len_args != 4:
        usage()
        return
    if sys.argv[1] == rgb:
        is_rgb = True
    elif sys.argv[1] == hsv:
        is_rgb = False
    else:
        usage()
        return
    for i in range(1, len_args):
        # check if the value is a number
        try:
            values.append(float(sys.argv[i]))
        except ValueError:
            usage()
            return
    result = None
    if is_rgb:
        result = to_hsv(values[0], values[1], values[2])
    else:
        result = to_hsv(values[0], values[1], values[2])
    (val1, val2, val3) = result
    print(f"Converted: {val1}, {val2}, {val3}")


if __name__ == "__main__":
    main()
