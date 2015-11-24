# -*- coding: utf-8 -*-


class AtomicFactory:
    def __init__(self):
        pass

    @staticmethod
    def get_clone_element(element, count):
        result = []
        for i in range(0, count):
            result.append(element())

        return result

    @classmethod
    def get_electron_list(cls, count):
        return cls.get_clone_element(Electron, count)

    @classmethod
    def get_proton_list(cls, count):
        return cls.get_clone_element(Proton, count)

    @classmethod
    def get_neutron_list(cls, count):
        return cls.get_clone_element(Neutron, count)

    @classmethod
    def get_atom(cls, proton_count, neutron_count=None):
        """
        :rtype: Atom
        """
        atom = MendeleevTable.get_atom_class_by_proton_count(proton_count)()

        if neutron_count is not None:
            atom.set_neutron_list(cls.get_neutron_list(neutron_count))

        return atom

    @classmethod
    def get_energy_level(cls, level, type_dict):

        orbit_list = []
        for orbit_type, count_electron in type_dict.items():
            while count_electron:
                if count_electron == 1:
                    count_electron -= 1
                    orbit_list.append(AtomicOrbital(orbit_type=orbit_type, electron_list=[Electron()]))
                else:
                    count_electron -= 2
                    orbit_list.append(AtomicOrbital(orbit_type=orbit_type, electron_list=[Electron(), Electron()]))

        return AtomicEnergeticLevel(level=level, atomic_orbital_list=orbit_list)


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


class AtomicEnergeticLevel:
    """ Атомный энергетический уровень
    @see https://dr282zn36sxxg.cloudfront.net/datastreams/f-d%3A96a9d2797f6e33d4a10187aeef0abdb52be51b8602c4fda58fa9768d%2BIMAGE_THUMB_POSTCARD%2BIMAGE_THUMB_POSTCARD.1
    # todo: вещества с одинаковым строением внешних энергетических уровней похожи по свойствам.

    # todo: понять, каким образом можно расчитать количество энергетических уровней имея только информацию о протонах и электронах
    # todo: понять, каким образом можно расчитать типы орбиталей для атома
    # todo: понять, каким образом можно расчитать максимальный энергетический уровень для атома
    aufbau principle
    Madelung energy ordering rule
    правила Клечковского и его исключения  # https://ru.wikipedia.org/wiki/Правило_Клечковского
    http://www.thenakedscientists.com/forum/index.php?topic=25337.0
    https://ru.wikipedia.org/wiki/%D0%AD%D0%BB%D0%B5%D0%BA%D1%82%D1%80%D0%BE%D0%BD%D0%BD%D0%B0%D1%8F_%D0%BA%D0%BE%D0%BD%D1%84%D0%B8%D0%B3%D1%83%D1%80%D0%B0%D1%86%D0%B8%D1%8F
    На данный момент, это империческое правило имеющее исключения. Природного алгоритма не известно.
    """

    level = None
    atomic_orbital_list = []  # Каждый энергетический уровень содержит атомные орбитали

    def __init__(self, level, atomic_orbital_list):
        self.level = level

        if not atomic_orbital_list:
            raise Exception('EnergeticLevel must contain some atomic orbitals')

        for atomic_orbital in atomic_orbital_list:
            if not isinstance(atomic_orbital, AtomicOrbital):
                raise Exception('EnergeticLevel may contain only atomic orbitals')

        self.atomic_orbital_list = atomic_orbital_list

    def __iter__(self):
        for atomic_orbital in self.atomic_orbital_list:
            yield atomic_orbital

    def get_energy_formula(self):
        """
        :return: Example for oxygen, level 2:  2s2p2
        """
        result = str(self.level)

        atomic_orbital_by_type = {}
        for atomic_orbital in self.atomic_orbital_list:
            if atomic_orbital.type not in atomic_orbital_by_type:
                atomic_orbital_by_type[atomic_orbital.type] = len(atomic_orbital)
            else:
                atomic_orbital_by_type[atomic_orbital.type] += len(atomic_orbital)

        for type_symbol in AtomicOrbital.allowed_type_list:
            if type_symbol in atomic_orbital_by_type:
                result += type_symbol + str(atomic_orbital_by_type[type_symbol])
        
        return result

    def get_max_electron(self):
        return 2 * self.level ** 2


class AtomicOrbital:
    """ Атомная орбита электронов
    """

    allowed_type_list = ('s', 'p', 'd', 'f')
    max_count_electron = 2  # Все орбитали могут содержать только 2 электрона (разных спинов)

    type = None  # s (sharp) - сфера; p (principal) - гантели ; d (diffuse) -
    electron_list = []

    def __init__(self, orbit_type, electron_list):

        self.type = orbit_type

        if not electron_list:
            raise Exception('AtomicOrbital must contain some electrons')

        for electron in electron_list:
            if not isinstance(electron, Electron):
                raise Exception('AtomicOrbital may contain only electrons')

        self.electron_list = electron_list

    def __iter__(self):
        for electron in self.electron_list:
            yield electron

    def __len__(self):
        return len(self.electron_list)


class Atom(object):
    symbol = None
    mass = None

    electron_count = None
    proton_count = None  # изменение количества протонов изменяет само вещество. Например водород в азот
    neutron_count = None  # изменение количества нейтронов не сильно влиеяет на физ.качества вещества.
    max_energy_level = None

    neutron_list = []
    energy_level_list = []

    def __new__(cls, element_list=None):
        if cls is not Atom:
            return super(Atom, cls).__new__(cls)

        proton_count = 0
        for element in element_list:
            if isinstance(element, Proton):
                proton_count += 1

        atom = MendeleevTable.get_atom_class_by_proton_count(proton_count)
        return atom(element_list)

    def __init__(self, element_list=None):
        self.neutron_count = 0

        if element_list is None:
            return

        for element in element_list:
            if isinstance(element, Neutron):
                self.neutron_count += 1

    def set_neutron_list(self, neutron_list=None):
        if neutron_list is None:
            self.neutron_count = []
            return

        for neutron in neutron_list:
            if not isinstance(neutron, Neutron):
                raise Exception('allowed only neutrons')
        self.neutron_list = neutron_list

    def get_mass(self):
        """ Является приблеженной, так как отображает и соотношение разных изотопов в природе
        """
        return self.mass

    def get_max_energy_level(self):
        """ Соответствует периоду в таб.Менделеева
        """
        return self.max_energy_level

    def get_electron_count(self):
        return self.proton_count

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

    def get_energy_formula(self):
        """
        :return: Example for oxygen: 1s2 2s2p4
        """
        result = ''

        for energy_level in self.energy_level_list:
            result += energy_level.get_energy_formula() + ' '

        return result


class Hydrogen(Atom):
    proton_count = 1
    symbol = 'H'
    mass = 1.00794
    max_energy_level = 1

    def __init__(self, energy_level_list=None):
        super(Hydrogen, self).__init__(energy_level_list)

        self.energy_level_list = [
            AtomicFactory.get_energy_level(level=1, type_dict={'s': 1}),
        ]


class Nitrogen(Atom):
    proton_count = 7
    symbol = 'N'
    mass = 14.00674
    max_energy_level = 2

    def __init__(self, energy_level_list=None):
        super(Nitrogen, self).__init__(energy_level_list)

        self.energy_level_list = [
            AtomicFactory.get_energy_level(level=1, type_dict={'s': 2}),
            AtomicFactory.get_energy_level(level=2, type_dict={'s': 2, 'p': 3})
        ]


class Oxygen(Atom):
    proton_count = 8
    symbol = 'O'
    mass = 15.9994
    max_energy_level = 2

    def __init__(self, energy_level_list=None):
        super(Oxygen, self).__init__(energy_level_list)

        self.energy_level_list = [
            AtomicFactory.get_energy_level(level=1, type_dict={'s': 2}),
            AtomicFactory.get_energy_level(level=2, type_dict={'s': 2, 'p': 4})
        ]


class Gold(Atom):
    proton_count = 79
    symbol = 'Au'
    mass = 196.96655
    max_energy_level = 6

    def __init__(self, energy_level_list=None):
        super(Gold, self).__init__(energy_level_list)

        self.energy_level_list = [
            AtomicFactory.get_energy_level(level=1, type_dict={'s': 2}),
            AtomicFactory.get_energy_level(level=2, type_dict={'s': 2, 'p': 6}),
            AtomicFactory.get_energy_level(level=3, type_dict={'s': 2, 'p': 6, 'd': 10}),
            AtomicFactory.get_energy_level(level=4, type_dict={'s': 2, 'p': 6, 'd': 10, 'f': 14}),
            AtomicFactory.get_energy_level(level=5, type_dict={'s': 2, 'p': 6, 'd': 10}),
            AtomicFactory.get_energy_level(level=6, type_dict={'s': 1})
        ]


class MendeleevTable():
    """ Таблица менделеева. Должно использоваться только для тех вещей которые мы не можем вычеслить, а только знаем.
          Например: символьное отображение атома. Количество энергетических уровней атома и т.д.
    """
    atom_class_by_proton_count = [
        None, Hydrogen, None,  # I
        None, None, None, None, Nitrogen, Oxygen, None, None,  # II
        None, None, None, None, None, None, None, None,  # III
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,  # IV
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,  # V

        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,  # VI
        None, None, None, None, None, None, Gold, None, None, None, None, None, None, None, None, None, None, None,

        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,  # VII
        None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
    ]

    def __init__(self):
        pass

    @classmethod
    def get_atom_class_by_proton_count(cls, proton_count):
        return cls.atom_class_by_proton_count[proton_count]


if __name__ == '__main__':

    # Создание атома через список протонов, нейтронов,
    atom_hydrogen = Atom([Proton()])
    print repr(atom_hydrogen.symbol)

    # Проверка на изотоп
    atom_deuterium = Atom([Proton(), Neutron()])
    print 'hydrogen and deuterium is isotopes: ' + str(atom_hydrogen.is_isotope(atom_deuterium))  # True
    print 'hydrogen and hydrogen is isotopes: ' + str(atom_hydrogen.is_isotope(atom_hydrogen))  # False

    atom_oxygen = Atom([Proton(), Proton(), Proton(), Proton(), Proton(), Proton(), Proton(), Proton()])
    print 'hydrogen and oxygen is isotopes: ' + str(atom_hydrogen.is_isotope(atom_hydrogen))  # False

    # Получение элементов через фабрику
    oxygen = AtomicFactory.get_atom(proton_count=8)
    print 'Oxygen energy formula: ' + oxygen.get_energy_formula()

    gold = AtomicFactory.get_atom(proton_count=79)
    print 'Gold energy formula: ' + gold.get_energy_formula()