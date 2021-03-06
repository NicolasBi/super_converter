""" A module used to convert a temperature into different bases.

Currently, the supported bases are :
- Binary
- Decimal
- Hexadecimal

Examples:
# Convert 27 from decimal to binary
>>> number1 = NumberWithBase("27", Base.DECIMAL)
>>> print(number1)
0d27
>>> number1.convert(Base.BINARY)
>>> print(number1)
0b11011

# Convert AaF0015424CB from hexadecimal to decimal
>>> number2 = NumberWithBase("AaF0015424CB", Base.HEXADECIMAL)
>>> print(number2)
0xAAF0015424CB
>>> number2.convert(Base.DECIMAL)
>>> print(number2)
0d187947791164619
"""

from enum import Enum

from super_converter.sconv.lib.tools.switchcase import switch


class NotANumberOrWrongBase(Exception):
    pass


class Base(Enum):
    NONE = 0
    BINARY = 2
    DECIMAL = 10
    HEXADECIMAL = 16


class NumberWithBase():
    """A number associated with a base.

    Attributes:
        base         An enum representing the current base of the number.
        number       A string representation of the number.
        IS_INVALID   A boolean flag set to True if the string representation
                     of the number makes no sense with the current base.
    """

    def __init__(self, number: str, base: Base):
        self.number = number.upper()
        self.base = base
        self.IS_INVALID = not self.is_a_number()

    def __str__(self):
        if self.IS_INVALID:
            return "{}\n{}\n{}".format(_("Not a number"),
                                       _("or"),
                                       _("wrong base"))

        prefix = None
        for case in switch(self.base):
            if case(Base.BINARY):
                prefix = 'b'
                break
            if case(Base.DECIMAL):
                prefix = 'd'
                break
            if case(Base.HEXADECIMAL):
                prefix = 'x'
                break
            if case():
                prefix = '?'
                break
        return "0{}{}".format(prefix, self.number)

    def is_a_number(self) -> bool:
        """ Dirty method to check if a number is correctly written in his corresponding
            base.
        """
        try:
            int(self.number, base=self.base.value)
            return True
        except Exception:
            return False

    def convert(self, new_base: Base) -> None:
        # Set the flag value if the number match his current base
        if not self.is_a_number():
            self.IS_INVALID = True
            return
        else:
            self.IS_INVALID = False

        # Set the flag if the number is negative
        # TODO: Support two-complement
        if int(self.number, base=self.base.value) < 0:
            self.IS_INVALID = True
            return

        # Convert the number into a new base
        if self.base == Base.BINARY:
            if new_base == Base.DECIMAL:
                self.base = Base.DECIMAL
                self.number = binary_to_decimal(self.number)
            elif new_base == Base.HEXADECIMAL:
                self.base = Base.HEXADECIMAL
                self.number = binary_to_hexadecimal(self.number)

        elif self.base == Base.DECIMAL:
            if new_base == Base.BINARY:
                self.base = Base.BINARY
                self.number = decimal_to_binary(self.number)
            elif new_base == Base.HEXADECIMAL:
                self.base = Base.HEXADECIMAL
                self.number = decimal_to_hexadecimal(self.number)

        elif self.base == Base.HEXADECIMAL:
            if new_base == Base.BINARY:
                self.base = Base.BINARY
                self.number = hexadecimal_to_binary(self.number)
            elif new_base == Base.DECIMAL:
                self.base = Base.DECIMAL
                self.number = hexadecimal_to_decimal(self.number)


def int_to_base(integer: int) -> Base:
    for case in switch(integer):
        if case(2):
            return Base.BINARY
            break
        if case(10):
            return Base.DECIMAL
            break
        if case(16):
            return Base.HEXADECIMAL
            break


def binary_to_decimal(number: str) -> str:
    return str(int(number, base=2))


def binary_to_hexadecimal(number: str) -> str:
    return str(hex(int(number, base=2))).upper()[2:]


def decimal_to_binary(number: str) -> str:
    return str(bin(int(number)))[2:]


def decimal_to_hexadecimal(number: str) -> str:
    return str(hex(int(number))).upper()[2:]


def hexadecimal_to_binary(number: str) -> str:
    return str(bin(int(number, 16)))[2:]


def hexadecimal_to_decimal(number: str) -> str:
    return str(int(number, 16))


if __name__ == '__main__':
    pass
