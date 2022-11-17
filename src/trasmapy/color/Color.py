import colorsys


class Color:
    def __init__(self, r: int, g: int, b: int, a: int = 255) -> None:
        self.r = r
        self.g = g
        self.b = b
        self.a = a
        if not all(0 <= x <= 255 for x in self.colorTupleA):
            raise ValueError(f"All RGB values must be in the interval [0, 255].")

    @classmethod
    def grayscale(cls, gray: int, a: int = 255):
        return cls(gray, gray, gray, a)

    @classmethod
    def hsv(cls, h: float, s: float, v: float, a: int = 255):
        return cls(*tuple(round(x * 255) for x in colorsys.hsv_to_rgb(h, s, v)), a=a)

    @classmethod
    def hls(cls, h: float, l: float, s: float, a: int = 255):
        return cls(*tuple(round(x * 255) for x in colorsys.hls_to_rgb(h, l, s)), a=a)

    @classmethod
    def yiq(cls, y: float, i: float, q: float, a: int = 255):
        return cls(*tuple(round(x * 255) for x in colorsys.yiq_to_rgb(y, i, q)), a=a)

    @property
    def colorTuple(self) -> tuple[int, int, int]:
        return (self.r, self.g, self.b)

    @property
    def colorTupleA(self) -> tuple[int, int, int, int]:
        return (self.r, self.g, self.b, self.a)

    def __repr__(self) -> str:
        return self.colorTupleA.__repr__()
