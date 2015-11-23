# -*- coding: utf-8 -*-


class Electron:
    mass = 0.002  # moll. Габриелян 8класс 21стр.
    speed = 300000  # km/sec. близка к скорости света. Меньшее ее, что соответствует наличию массы
    electric_charge = -1

    def __init__(self):
        pass


class Proton:
    mass = 1
    symbol = 'p'
    electric_charge = 1

    def __init__(self):
        pass


class Neutron:
    mass = 1
    symbol = 'n'
    electric_charge = 0

    def __init__(self):
        pass


class Atom(object):
    symbol = None
    mass = None

    electron_count = None
    proton_count = None  # изменение количества протонов изменяет само вещество. Например водород в азот

    neutron_count = None  # изменение количества нейтронов не сильно влиеяет на физ.качества вещества.

    def __new__(cls, element_list=None):
        if cls is not Atom:
            return super(Atom, cls).__new__(cls)

        proton_count = 0
        for element in element_list:
            if isinstance(element, Proton):
                proton_count += 1

        if proton_count == 1:
            return Hydrogen(element_list)
        elif proton_count == 8:
            return Oxygen(element_list)

        raise NotImplemented

    def __init__(self, element_list=None):
        self.neutron_count = 0

        for element in element_list:
            if isinstance(element, Neutron):
                self.neutron_count += 1

    def get_mass(self):
        """ Является приблеженной, так как отображает и соотношение разных изотопов в природе
        """
        return self.mass

    def get_real_mass(self):
        return self.proton_count + self.neutron_count

    def is_isotope(self, atom_for_compare):
        """
        :type atom_for_compare: Atom
        """
        if self.proton_count == atom_for_compare.proton_count:
            if self.neutron_count != atom_for_compare.neutron_count:
                return True

        return False


class AtomFactory():

    def __init__(self):
        pass

    def create_by_elements(self, elements_list):
        pass


class Nitrogen(Atom):
    proton_count = 7
    symbol = 'N'
    mass = 14.00674


class Hydrogen(Atom):
    proton_count = 1
    symbol = 'H'
    mass = 1.00794


class Oxygen(Atom):
    proton_count = 8
    symbol = 'O'
    mass = 15.9994


if __name__ == '__main__':

    # Создание атома через список протонов, нейтронов,
    list_element = [Proton()]
    atom_hydrogen = Atom(list_element)
    print repr(atom_hydrogen.symbol)

    # Проверка на изотоп
    list_element = [Proton(), Neutron()]
    atom_deuterium = Atom(list_element)
    print 'hydrogen and deuterium is isotopes: ' + str(atom_hydrogen.is_isotope(atom_deuterium))  # True
    print 'hydrogen and hydrogen is isotopes: ' + str(atom_hydrogen.is_isotope(atom_hydrogen))  # False

    atom_oxygen = Atom([Proton(), Proton(), Proton(), Proton(), Proton(), Proton(), Proton(), Proton()])
    print 'hydrogen and oxygen is isotopes: ' + str(atom_hydrogen.is_isotope(atom_hydrogen))  # False
