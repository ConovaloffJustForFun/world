# -*- coding: utf-8 -*-


class Substance:

    def __init__(self, atom_list):
        self.atom_list = atom_list

    def is_simple(self):
        """ Если вещество образовано атомами одного химического элемента, то оно простое. Например O2
            В ином случае, это сложное вещество. Пример H20
        """
        first_atom = self.atom_list[0]
        for atom in self.atom_list[1:]:
            if atom != first_atom:
                return False

        return True

    def get_formula(self):
        """
        TODO: катионы записываются первыми, следом идут анионы
                               https://lavelle.chem.ucla.edu/forum/viewtopic.php?f=45&t=3001
        """
        result = ''

        atom_dict = {}
        for atom in self.atom_list:
            if atom.symbol in atom_dict:
                atom_dict[atom.symbol] += 1
            else:
                atom_dict[atom.symbol] = 1

        for symbol, count in atom_dict.iteritems():
            if count == 1:
                result += symbol
            else:
                result += symbol + str(count)

        return result

    def get_mass_formula(self):
        return 'M(' + self.get_formula() + ') = ' + str(self.get_mass()) + ' g/mol'

    def get_mass(self):
        result = 0

        for atom in self.atom_list:
            result += atom.get_mass()

        return result


if __name__ == '__main__':
    import Atom

    # Получаем формулу вещества
    atom_list = [Atom.Hydrogen(), Atom.Hydrogen(), Atom.Oxygen()]
    water = Substance(atom_list)
    print water.get_formula()

    # Получаем молекулярную массу
    print water.get_mass_formula()
    print 'Molar mass: ' + str(water.get_mass())