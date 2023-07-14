from helga.ring import infer_ring, is_field


class ProjectivePoint:
    def __init__(self, coords, field=None):
        if field is None:
            field = infer_ring(coords)
        assert is_field(field)
        self.field = field

        coords = tuple(field(coord) for coord in coords)

        for i in reversed(range(len(coords))):
            factor = coords[i]
            if factor != field(0):
                self.coords = tuple(coord / factor for coord in coords)
                break
        else:
            raise ValueError("all coordinates are zero")

    @property
    def dim(self):
        return len(self.coords)

    def __eq__(self, rhs):
        if not isinstance(rhs, ProjectivePoint):
            return NotImplemented

        return self.coords == rhs.coords

    def __hash__(self):
        return hash(self.coords)

    def __str__(self):
        return "[" + " : ".join(str(coord) for coord in self.coords) +  "]"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.coords}, {self.field.__name__})"
