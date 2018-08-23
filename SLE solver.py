array = [
    [2, 3, 1, 13],
    [8, 0, -2, -10],
    [0, 18, -3, 9]
]


class Number():
    """@author tecosaur"""

    def __init__(self, *args):
        # Sanitise the input
        if len(args) == 0:
            value = '0/1'
        elif len(args) == 1:
            value = args[0]
            if isinstance(value, Number):
                self.type = value.type
                if self.type == 'fraction':
                    self.numerator = value.numerator
                    self.denominator = value.denominator
                elif self.type == 'decimal':
                    self.value = value.value
                return
            elif type(value) in [str, int, float]:
                value = str(value).replace(' ', '')
                # If it's an integer
                if not '.' in value and not '/' in value:
                    value = value+'/1'
                # If it's a float with <= 3 decimal places convert to frac
                elif '.' in value and len(value.split('.')[1]) <= 3:
                    value = value.replace('.', '') + '/' + str(10**len(value.split('.')[1]))
            else:
                raise ValueError('Number class only accepts str/int/float types for initialisation')
        elif len(args) == 2:
            if type(args[0]) in [str, int, float] and type(args[1]) in [str, int, float]:
                value = str(args[0]).replace(' ', '') + '/' + str(args[1]).replace(' ', '')
            else:
                raise ValueError('Number class only accepts str/int/float types for initialisation')
        else:
            raise TypeError('Too many parameters passed!')
        # Now to actually process the imput
        self.type = 'fraction' if '/' in value else 'decimal'
        if self.type == 'fraction':
            self.numerator = int(value.split('/')[0])
            self.denominator = int(value.split('/')[1])
        elif self.type == 'decimal':
            self.value = float(value)
        self.simplify()

    def info(self):
        return "<Number type='{0}' value='{1}'>".format(self.type, str(self.numerator)+'/'+str(self.denominator) if self.type == 'fraction' else self.value)

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.type == 'decimal':
            return str(self.value)
        elif self.type == 'fraction':
            if self.denominator == 1:
                return str(self.numerator)
            else:
                return str(self.numerator) + '/' + str(self.denominator)

    def __float__(self):
        if self.type == 'decimal':
            return self.value
        elif self.type == 'fraction':
            return (self.numerator / self.denominator)

    def __int__(self):
        return int(float(self))

    def simplify(self):
        '''Reduces fractions. n is the numerator and d the denominator.'''
        def gcd(n, d):
            while d != 0:
                t = d
                d = n % d
                n = t
            return n
        assert self.denominator != 0, "integer division by zero"
        assert isinstance(self.denominator, int), "must be int"
        assert isinstance(self.numerator, int), "must be int"
        greatest = gcd(self.numerator, self.denominator)
        self.numerator = int(self.numerator / greatest)
        self.denominator = int(self.denominator / greatest)

    def __add__(self, other):
        other = other if isinstance(other, Number) else Number(other)
        result = Number(str(self.numerator*other.denominator + other.numerator *
                            self.denominator) + '/' + str(self.denominator*other.denominator))
        result.simplify()
        return result

    def __radd__(self, other):
        self.__add__(other)

    def __sub__(self, other):
        other = other if isinstance(other, Number) else Number(other)
        return self+(other*Number(-1))

    def __rsub__(self, other):
        return self.__sub__(other)

    def __mul__(self, other):
        other = other if isinstance(other, Number) else Number(other)
        if self.type == 'fraction':
            if other.type == 'fraction':
                result = Number(self.numerator * other.numerator, self.denominator * other.denominator)
            elif other.type == 'decimal':
                result = Number(float(self)*other.value)
        elif self.type == 'decimal':
            result = Number(self.value*float(other))
        result.simplify()
        return result

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        other = other if isinstance(other, Number) else Number(other)
        return self * (other**-1)

    def __rtruediv__(self, other):
        return self.__truediv__(other)

    def __pow__(self, power):
        if self.type == 'number':
            return self.value**power
        elif self.type == 'fraction':
            if power < 0:
                return Number(self.denominator, self.numerator)**(-power)
            elif power == 0:
                return Number(1)
            else:
                return Number(self.numerator**power, self.denominator**power)


class Matrix():
    "@author tecosaur"

    def __init__(self, *args, barLocation=None):
        # Sanitise matrix
        if len(args) == 0:
            matrix = []
        elif len(args) == 1:
            if type(args[0]) == list:
                matrix = args[0]
            elif type(args[0]) == int:
                matrix = [[0]*args[0]]*args[0]
            else:
                raise TypeError('Matrix can be initialised only with a list or int')
        elif len(args) == 2:
            if type(args[0]) == int and type(args[1]) == int:
                matrix = [[0]*args[1]]*args[0]
            else:
                raise TypeError('Matrix can be initialised only with a list or int')
        else:
            raise TypeError('Matrix initialisation takes at most 2 arguments')
        self.matrix = matrix
        self.MaxElementLength = 7
        self.barLocation = barLocation

    def toNumbers(self):
        for r in range(len(self.matrix)):
            for c in range(len(self.matrix[r])):
                self.matrix[r][c] = Number(self.matrix[r][c])

    def __getitem__(self, i):
        return self.matrix

    # TODO: read/set row/col functions

    def __str__(self):
        rowString = ''
        for row in range(len(self.matrix)):
            # Adds square bracket start
            rowString += '⎡' if row == 0 else ('⎣' if row == (len(self.matrix)-1) else '⎢')
            if self.barLocation != None:
                # Adds all but last element of row
                for elem in self.matrix[row][:self.barLocation]:
                    rowString += ('{:>' + str(self.MaxElementLength) + '.' + str(self.MaxElementLength+1) +
                                  '}').format(' ' + str(elem).replace(' -', '-'))
                rowString += ' ⎢ '
                for elem in self.matrix[row][self.barLocation:]:
                    rowString += ('{:>' + str(self.MaxElementLength) + '.' + str(self.MaxElementLength+1) +
                                  '}').format(' ' + str(elem).replace(' -', '-'))
            else:
                for elem in self.matrix[row]:
                    rowString += ('{:>' + str(self.MaxElementLength) + '.' + str(self.MaxElementLength+1) +
                                  '}').format(' ' + str(elem).replace(' -', '-'))
            # Adds square bracket end
            rowString += ' ' + ('⎤' if row == 0 else ('⎦' if row == len(self.matrix)-1 else '⎥'))
            # If not last line add new line
            rowString += '\n' if row < len(self.matrix) else ''
        return rowString


# FIXME: need to class-ify some global variables? Anyway, funny stuff is happening
class GaussJordanSLE(Matrix):
    "@author DAdams2"

    def __init__(self, augmented_matrix):
        Matrix.__init__(self, augmented_matrix, -1)

    def check_leading(self, point1, point2):
        if array[point1][point2] != 1 and array[point1][point2] != 0:
            # print("processing")
            leading = array[point1][point2]
            for i in range(0, len(array[point1])):
                array[point1][i] /= leading

    def print_array(self):
        for row in self.matrix:
            print(row)

    def check_zeros(self, row):
        for i in range(len(self.matrix)):
            if(self.matrix[row][i] != 0):
                return(False)
        return(True)

    def move_row(self, row):
        temp = self.matrix[len(self.matrix)-1]
        self.matrix[len(self.matrix)-1] = self.matrix[row]
        self.matrix[row] = temp

    def clear_collum(self, row, pos):
        # going up
        rotpos = row
        while(rotpos-1 >= 0):
            if self.matrix[rotpos-1][pos] != 0:
                multiple = self.matrix[rotpos-1][pos]
                for i in range(len(self.matrix[row])):
                    self.matrix[rotpos-1][i] -= multiple*self.matrix[row][i]
                # subtract thigns
            rotpos -= 1
        rotpos = row
        # print_array()
        while(rotpos+1 < len(self.matrix)):
            if self.matrix[rotpos+1][pos] != 0:
                multiple = self.matrix[rotpos+1][pos]
                for i in range(len(self.matrix[row])):
                    # print(str(self.matrix[rotpos+1][i]) + " - " + str(multiple) + " x "+  str(self.matrix[row][i]) + " = ")
                    self.matrix[rotpos+1][i] -= multiple*self.matrix[row][i]
                    # print(self.matrix[rotpos+1][i])
                    # print_array()
                    # print()
            rotpos += 1

    def solve(self):
        start1, start2 = 0, 0
        while(start1 < len(self.matrix[0]) and start2 < len(self.matrix)):
            if(self.check_zeros(start1)):
                self.move_row(start1)
            self.check_leading(start1, start2)
            self.clear_collum(start2, start2)
            start1 += 1
            start2 += 1
        # # currently undefined:
        # # check_solutions()
        # print()
        # print_array()
        # pretty_print_result(array)
        # gj_cli()

# Example prety_print_result(1, 2, 4) -> "x₁ = 1, x₂ = 2, x₃ = 4"
# x₁ = 0, x₂ = 1, x₃ = 2, x₄ = 3, x₅ = 4, x₆ = 5, x₇ = 6, x₈ = 7, x₉ = 8, x₁₀ = 9, x₁₁ = 10, x₁₂ = 11, x₁₃ = 12, x₁₄ = 13, x₁₅ = 14, x₁₆ = 15, x₁₇ = 16, x₁₈ = 17, x₁₉ = 18, x₂₀ = 19, x₂₁ = 20, x₂₂ = 21, x₂₃ = 22, x₂₄ = 23, x₂₅ = 24, x₂₆ = 25, x₂₇ = 26, x₂₈ = 27, x₂₉ = 28, x₃₀ = 29, x₃₁ = 30, x₃₂ = 31, x₃₃ = 32, x₃₄ = 33, x₃₅ = 34, x₃₆ = 35, x₃₇ = 36, x₃₈ = 37, x₃₉ = 38, x₄₀ = 39, x₄₁ = 40, x₄₂ = 41, x₄₃ = 42, x₄₄ = 43, x₄₅ = 44, x₄₆ = 45, x₄₇ = 46, x₄₈ = 47, x₄₉ = 48, x₅₀ = 49


# gj_cli()

def gj_cli():
    global gj_cli_run_yet
    if not 'gj_cli_run_yet' in globals() or gj_cli_run_yet == False:
        gj_cli_run_yet = True
        print('''
    Welcome to the CLI of a Gauss-Jordan SLE solver.
    You're about to be prompted for the augmented matrix of your equation
    line by line. Just enter the coeeficients separated by a comma
    and then use a comma instead of a vertical bar.
    e.g. '1  2  3 | 4' → '1, 2, 3, 4'

    Have fun solving your equation :)
        ''')
    matrix = []
    line = input("\ncomma separated coefficients and result: ")
    while line:
        matrix.append(list(map(
            lambda flt_str: Number(flt_str),
            line.replace(' ', '').split(','))
        ))
        line = input("comma separated coefficients and result: ")

    matrix_as_string = '\n'.join(
        list(map(
            lambda line: ''.join(list(map(
                lambda coeff: ('{:>7.8}'.format(
                    ' ' + str(coeff).replace(' -', '-'))),
                line
            ))),
            matrix
        ))
    )

    if input('\nConfirm that \n{0}\n Is the correct augmented matrix (y/n) '.format(matrix_as_string)).lower() == 'y':
        global array
        array = GaussJordanSLE(matrix)
        array.solve()


def pretty_print_result(array_of_values, multiline=False):
    '''Turns array of form [x_1_val, x_2_val, ... x_n_val] into a pretty

    Arguments:
        array_of_values {array} -- Array with the the value of x_(i+1) at the ith index
        multiline {boolein} do you want the result to be multiline?
    '''

    subscript = {'0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄', '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉'}
    for i in range(len(array_of_values)):
        print('x' + (
            ''.join(list(map(lambda i: subscript[i], list(str(i+1)))))) + ' = ' + str(array_of_values[i][len(array_of_values[i])-1]),
            end=('\n' if multiline else (', ' if i < len(array_of_values) - 1 else ' ')))
