class Matrix(object):

    def __init__(self, matrix_values):
        self.matrix_values = matrix_values

    def __matmul__(self, m2):
        """
            https://docs.python.org/3/reference/datamodel.html#object.__matmul__
        """
        return Matrix(Matrix._multiply(self.matrix_values, m2.matrix_values))

    def __rmatmul__(self, m1):
        """
            https://docs.python.org/3/reference/datamodel.html#object.__rmatmul__
        """
        return Matrix(Matrix._multiply(m1.matrix_values, self.matrix_values))

    def __imatmul__(self, m2):
        """
            https://docs.python.org/3/reference/datamodel.html#object.__imatmul__
        """
        return self.__matmul__(m2)

    def __repr__(self):
        return str(self.matrix_values)

    @staticmethod
    def _multiply(m1, m2):
        return [[sum(m1 * m2
                     for m1, m2 in zip(m1_row, m2_col))
                 for m2_col in zip(*m2)]
                for m1_row in m1]


class M:
    def __init__(self, v):
        self.v = v

    def __matmul__(self, other):
        ls = self.v
        rs = other.v
        return [[sum(ls * rs
                     for ls, rs in zip(lsr, rsr))
                 for rsr in zip(*rs)]
                for lsr in ls]
