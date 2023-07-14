from helga.ring import infer_ring, is_field

class ProjectivePoint:
    def __init__(self, coords, field=None):
        if field is None:
            field = infer_ring(coords)
        assert is_field(field)
        self.field = field

        assert any(coord != field(0) for coord in coords)

        self.coords = tuple(field(coord) for coord in coords)

    @property
    def dim(self):
        return len(self.coords)

    def __eq__(self, rhs):
        if not isinstance(rhs, ProjectivePoint):
            return NotImplemented

        if len(self.coords) != len(rhs.coords):
            return False

        for i, value in enumerate(self.coords):
            if value != self.field(0):
                factor = rhs.coords[i] / value
                break

        return (self * factor).coords == rhs.coords

    def __mul__(self, rhs):
        if type(rhs) != self.field:
            return NotImplemented

        return self.__class__([coord * rhs for coord in self.coords], field=self.field)
    
    def __rmul__(self, lhs):
        if type(lhs) != self.field:
            return NotImplemented

        return self.__class__([lhs * coord for coord in self.coords], field=self.field)
    
    def __truediv__(self, rhs):
        if type(rhs) != self.field:
            return NotImplemented

        return self.__class__([coord / rhs for coord in self.coords], field=self.field)

    def __hash__(self):
        return hash(self.coords)

    def __str__(self):
        return "[" + " : ".join(str(coord) for coord in self.coords) +  "]"

    def __repr__(self):
        return f"{self.__class__.__name__}({self.coords}, {self.field.__name__})"
