from downloader import download
from copy import copy, deepcopy
from itertools import product
from math import ceil
import operator
import re
from string import ascii_uppercase as ABC

download(2021, 24)
with open('aoc2021_24input.txt') as inputfile:
    data = inputfile.read()
#print(data)
#for i, line in enumerate(data.splitlines()):
    #print(i, line)

def div(a, b):
    if a // b >= 0:
        return a // b
    return ceil(a / b)

variables = {'w': 0, 'x': 1, 'y': 2, 'z': 3}
ops = {'add': operator.add, 'mul': operator.mul, 'div': operator.floordiv, 'mod': operator.mod, 'eql': operator.eq}


class Variable:
    
    def __init__(self, var, factor=1):
        self.var = var
        self.factor = factor
    
    def __bool__(self):
        return bool(self.factor)
    
    def __eq__(self, other):
        try:
            return (self.var, self.factor) == (other.var, other.factor)
        except AttributeError:
            return False
    
    def __mul__(self, other):
        if isinstance(other, int):
            self.factor *= other
        else:
            print('mul by var')
            self.factor *= other.factor
            self.var += f'*{other.var}'
        if not self.factor:
            return Expression()
        return self
    
    def __floordiv__(self, other):
        """if isinstance(other, int):
            self.factor = div(self.factor, other)
        else:
            print('div by var')
            raise NotImplementedError
            self.factor = div(self.factor, other.factor)
            if self.var == other.var:
                return Expression(self.factor)
            self.var = f'div({self}, {other}'
        return self"""
        if self == other:
            return Expression(1)
        if self.factor == other.factor:
            if self.max() < other.min():
                return Expression()
            return Variable(f'div({self.var!s}, {other.var!s}')
        if self.var == other.var:
            return Expression(div(self.factor, other.factor))
        raise NotImplementedError
        return Variable(f'div({self!s}, {other!s}')
    
    def __mod__(self, other):
        if isinstance(other, int):
            self.factor %= other
            if not self.factor:
                return Expression()
        if self.max() < other.min():
            return 
        print('mod by var')
        raise NotImplementedError
        self.var = f'({self.factor}*{self.var})%{other}'
        self.factor = 1
        return self
    
    def __repr__(self):
        if not isinstance(self.var, str):
            raise TypeError
        return f'Variable({self.var}, {self.factor})'
        return str(self)
    
    def __str__(self):
        return f'{self.factor}*{self.var}' if self.factor != 1 else str(self.var)
    
    def __copy__(self):
        return Variable(self.var, self.factor)
    
    def max(self):
        if 'div' in self.var or '%' in self.var:
            raise NotImplementedError
        return eval(re.sub('[A-N]', '9', str(self)))

    def min(self):
        if 'div' in self.var or '%' in self.var:
            raise NotImplementedError
        return eval(re.sub('[A-N]', '1', str(self)))


class Expression:
    
    def __init__(self, const=0, vars=None):
        self.const = const
        if vars is None:
            vars = []
        self.vars = vars
    
    def __bool__(self):
        return bool(self.const or self.vars)
    
    def __eq__(self, other):
        if not self.vars and not other.vars:
            return Expression(int(self.const == other.const))
        elif (self.const, self.vars) == (other.const, other.vars):
            return Expression(1)
        if not self.vars and other.has_simple_vars():
            comparator = (self.const - other.const) / other.vars[0].factor
            if not (0 < comparator < 10) or not comparator.is_integer():
                return Expression()
        if not self.vars and other.positive_vars() and (self.const - other.const) < 0:
            return Expression()
        if not other.vars and self.has_simple_vars():
            comparator = (other.const - self.const) / self.vars[0].factor
            if not (0 < comparator < 10) or not comparator.is_integer():
                return Expression()
        if not other.vars and self.positive_vars() and (other.const - self.const) < 0:
            return Expression()
        if self.has_simple_vars() and other.positive_vars() and (other.const - self.const) / self.vars[0].factor > 9:
            return Expression()
        if other.has_simple_vars() and self.positive_vars() and (self.const - other.const) / other.vars[0].factor > 9:
            return Expression()
        if self.max() < other.min() or self.min() > other.max():
            return Expression()
        if self.has_simple_vars() and other.has_simple_vars():
            return variable_equality_test(self, other)
        print(f'{self}=={other}')
        raise NotImplementedError
        operand1 = f'({self!s})' if '+' in str(self) else str(self)
        operand2 = f'({other!s})' if '+' in str(other) else str(other)
        return Expression(vars=[Variable(f'{operand1}=={operand2}')])
    
    def __add__(self, other):
        const = self.const + other.const
        vars = {var.var: var.factor for var in self.vars}
        for other_var in other.vars:
            if other_var.var in vars:
                vars[other_var.var] += other_var.factor
            else:
                vars[other_var.var] = other_var.factor
        vars = [Variable(var, factor) for var, factor in vars.items() if factor]
        return Expression(const, vars)
    
    def __sub__(self, other):
        const = self.const - other.const
        vars = {var.var: var.factor for var in self.vars}
        for other_var in other.vars:
            if other_var.var in vars:
                vars[other_var.var] -= other_var.factor
            else:
                vars[other_var.var] = -other_var.factor
        vars = [Variable(var, factor) for var, factor in vars.items() if factor]
        return Expression(const, vars)
    
    def __mul__(self, other):
        if Expression() in (self, other):
            return Expression()
        elif Expression(1) in (self, other):
            operands = [self, other]
            operands.remove(Expression(1))
            return operands.pop()
        const = self.const * other.const
        if not self.vars and not other.vars:
            return Expression(const)
        elif not self.vars and other.vars:
            return Expression(const, [Variable(var.var, var.factor * self.const) for var in other.vars])
        elif self.vars and not other.vars:
            return Expression(const, [Variable(var.var, var.factor * other.const) for var in self.vars])
        print(f'{self}*{other}')
        raise NotImplementedError
        expression = Expression()
        for a, b in product(self.vars + [self.const], other.vars + [other.const]):
            if a == self.const and b == other.const:
                expression.const = const
            elif a == self.const:
                expression.vars.append(Variable(b, a))
            elif b == other.const:
                expression.vars.append(Variable(a, b))
            else: 
                expression.vars.append(Variable(f'{a}*{b}'))
        return expression
    
    def __floordiv__(self, other):
        if other == Expression():
            raise ZeroDivisionError
        if self == Expression() or other == Expression(1):
            return deepcopy(self)
        if not self.vars and not other.vars:
            return Expression(div(self.const, other.const))
        if self.min() >= 0 and not other.vars:
            expression = self - (self % other)
            const = expression.const / other.const
            if not const.is_integer():
                raise ValueError
            vars = []
            for var in expression.vars:
                factor = var.factor / other.const
                if not factor.is_integer():
                    raise ValueError
                vars.append(Variable(var.var, int(factor)))
            return Expression(int(const), vars)
        print(f'{self}//{other}')
        raise NotImplementedError
        denominator = str(other)
        numerators = self.vars
        if self.const:
            numerators.append(self.const)
        vars = [Variable(f'div({numerator}, {denominator})') for numerator in numerators]
        return Expression(vars=vars)
    
    def __mod__(self, other):
        if other.max() <= 0 or self.max() < 0:
            raise ZeroDivisionError
        if other == Expression(1):
            return Expression()
        if self == Expression():
            return Expression()
        if not self.vars and not other.vars:
            return Expression(self.const % other.const)
        if not other.vars and self.has_simple_vars():
            if self.const + 9 * self.vars[0].factor < other.const:
                return deepcopy(self)
            if not self.const:
                return Expression(vars=[self.vars[0] % other.const])
        if self.max() < other.min():
            return deepcopy(self)
        #print(f'{self}%{other}')
        if not other.vars and self.vars:
            new_const = self.const % other.const
            changed = self.const != new_const
            new_vars = [] 
            for var in self.vars:
                new_var = (Expression(vars=[copy(var)]) % other).vars[0]
                changed = changed or var != new_var
                if new_var != Expression():
                    new_vars.append(new_var)
            if changed:
                expression = Expression(new_const, new_vars)
                return expression % other
        raise NotImplementedError
        operand1 = f'({self!s})' if '+' in str(self) else str(self)
        operand2 = f'({other!s})' if '+' in str(other) else str(other)
        return Expression(vars=[f'{operand1}%{operand2}'])
    
    def __repr__(self):
        return f'Expression({self.const}, {self.vars})'
        return str(self)
    
    def __str__(self):
        if not self.vars:
            expression = str(self.const)
        else:
            expression = f'{"+".join(str(var) for var in self.vars)}'
            if self.const:
                expression += f'+{self.const}'
        return expression
    
    def __deepcopy__(self, memodict):
        return Expression(self.const, [deepcopy(var) for var in self.vars])
    
    def has_simple_vars(self):
        return len(self.vars) == 1 and len(self.vars[0].var) == 1
    
    def positive_vars(self):
        return not any(('-' in var.var or var.factor < 0) for var in self.vars)
    
    def max(self):
        return self.const + sum(var.max() for var in self.vars)

    def min(self):
        return self.const + sum(var.min() for var in self.vars)
    
#def variable_equality_test(a, b):
    #print('*****\nTESTING True\n*****')
    #return Expression(1)
    #return Expression(int(input(f'{a}=={b}?')))

def alu():
    inputs = iter(ABC)
    state = [Expression() for var in range(4)]
    for i, command in enumerate(data.splitlines()):
        #print(f'{i}. {command}')
        parts = command.split()
        if parts[0] == 'inp':
            result = Expression(vars=[Variable(next(inputs))])
        else:
            a = state[variables[parts[1]]]
            try:
                b = state[variables[parts[2]]]
            except KeyError:
                b = Expression(int(parts[2]))
            op = ops[parts[0]]
            result = op(a, b)
        state[variables[parts[1]]] = result
        #print(state)
        #print()
    return state[-1]
#alu()

for order in product((1, 0), repeat=7):
    order = iter(order)
    tests = []
    def variable_equality_test(a, b):
        result = next(order)
        #print(result)
        signs = ('!=', '==')
        tests.append(f'{a}{signs[result]}{b}')
        return Expression(result)
    z = alu()
    if not z:
        print(tests)


'''0 inp w  # A 0 0 0
1 mul x 0  # A 0 0 0
2 add x z  # A 0 0 0
3 mod x 26  # A 0 0 0
4 div z 1  # A 0 0 0
5 add x 10  # A 10 0 0
6 eql x w  # A 0 0 0
7 eql x 0  # A 1 0 0
8 mul y 0  # A 1 0 0
9 add y 25  # A 1 25 0
10 mul y x  # A 1 25 0
11 add y 1  # A 1 26 0
12 mul z y  # A 1 26 0
13 mul y 0  # A 1 0 0
14 add y w  # A 1 A 0
15 add y 10  # A 1 A+10 0
16 mul y x  # A 1 A+10 0
17 add z y  # A 1 A+10 A+10
18 inp w  # B 1 A+10 A+10
19 mul x 0  # B 0 A+10 A+10
20 add x z  # B A+10 A+10 A+10
21 mod x 26  # B A+10 A+10 A+10
22 div z 1  # B A+10 A+10 A+10
23 add x 13  # B A+23 A+10 A+10
24 eql x w  # B 0 A+10 A+10
25 eql x 0  # B 1 A+10 A+10
26 mul y 0  # B 1 0 A+10
27 add y 25  # B 1 25 A+10
28 mul y x  # B 1 25 A+10
29 add y 1  # B 1 26 A+10
30 mul z y  # B 1 26 26A+260
31 mul y 0  # B 1 0 26A+260
32 add y w  # B 1 B 26A+260
33 add y 5  # B 1 B+5 26A+260
34 mul y x  # B 1 B+5 26A+260
35 add z y  # B 1 B+5 26A+B+265
36 inp w  # C 1 B+5 26A+B+265
37 mul x 0  # C 0 B+5 26A+B+265
38 add x z  # C 26A+B+265 B+5 26A+B+265
39 mod x 26  # C B+5 B+5 26A+B+265
40 div z 1  # C B+5 B+5 26A+B+265
41 add x 15  # C B+20 B+5 26A+B+265
42 eql x w  # C 0 B+5 26A+B+265
43 eql x 0  # C 1 B+5 26A+B+265
44 mul y 0  # C 1 0 26A+B+265
45 add y 25  # C 1 25 26A+B+265
46 mul y x  # C 1 25 26A+B+265
47 add y 1
48 mul z y
49 mul y 0
50 add y w
51 add y 12
52 mul y x
53 add z y
54 inp w
55 mul x 0
56 add x z
57 mod x 26
58 div z 26
59 add x -12
60 eql x w  # C==D
61 eql x 0
62 mul y 0
63 add y 25
64 mul y x
65 add y 1
66 mul z y
67 mul y 0
68 add y w
69 add y 12
70 mul y x
71 add z y
72 inp w
73 mul x 0
74 add x z
75 mod x 26
76 div z 1
77 add x 14
78 eql x w
79 eql x 0
80 mul y 0
81 add y 25
82 mul y x
83 add y 1
84 mul z y
85 mul y 0
86 add y w
87 add y 6
88 mul y x
89 add z y
90 inp w
91 mul x 0
92 add x z
93 mod x 26
94 div z 26
95 add x -2
96 eql x w  # E+4==F
97 eql x 0
98 mul y 0
99 add y 25
100 mul y x
101 add y 1
102 mul z y
103 mul y 0
104 add y w
105 add y 4
106 mul y x
107 add z y
108 inp w
109 mul x 0
110 add x z
111 mod x 26
112 div z 1
113 add x 13
114 eql x w
115 eql x 0
116 mul y 0
117 add y 25
118 mul y x
119 add y 1
120 mul z y
121 mul y 0
122 add y w
123 add y 15
124 mul y x
125 add z y
126 inp w
127 mul x 0
128 add x z
129 mod x 26
130 div z 26
131 add x -12
132 eql x w
133 eql x 0
134 mul y 0
135 add y 25
136 mul y x
137 add y 1
138 mul z y
139 mul y 0
140 add y w
141 add y 3
142 mul y x
143 add z y
144 inp w
145 mul x 0
146 add x z
147 mod x 26
148 div z 1
149 add x 15
150 eql x w
151 eql x 0
152 mul y 0
153 add y 25
154 mul y x
155 add y 1
156 mul z y
157 mul y 0
158 add y w
159 add y 7
160 mul y x
161 add z y
162 inp w
163 mul x 0
164 add x z
165 mod x 26
166 div z 1
167 add x 11
168 eql x w
169 eql x 0
170 mul y 0
171 add y 25
172 mul y x
173 add y 1
174 mul z y
175 mul y 0
176 add y w
177 add y 11
178 mul y x
179 add z y
180 inp w
181 mul x 0
182 add x z
183 mod x 26
184 div z 26
185 add x -3
186 eql x w
187 eql x 0
188 mul y 0
189 add y 25
190 mul y x
191 add y 1
192 mul z y
193 mul y 0
194 add y w
195 add y 2
196 mul y x
197 add z y
198 inp w
199 mul x 0
200 add x z
201 mod x 26
202 div z 26
203 add x -13
204 eql x w
205 eql x 0
206 mul y 0
207 add y 25
208 mul y x
209 add y 1
210 mul z y
211 mul y 0
212 add y w
213 add y 12
214 mul y x
215 add z y
216 inp w
217 mul x 0
218 add x z
219 mod x 26
220 div z 26
221 add x -12
222 eql x w
223 eql x 0
224 mul y 0
225 add y 25
226 mul y x
227 add y 1
228 mul z y
229 mul y 0
230 add y w
231 add y 4
232 mul y x
233 add z y
234 inp w
235 mul x 0
236 add x z
237 mod x 26
238 div z 26
239 add x -13
240 eql x w
241 eql x 0
242 mul y 0
243 add y 25
244 mul y x
245 add y 1
246 mul z y
247 mul y 0
248 add y w
249 add y 11
250 mul y x
251 add z y'''
