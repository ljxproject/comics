from django.test import TestCase


class AnimalType(type):
    allow_l = []

    def __new__(cls, name, bases, attrs):
        print(name, bases, attrs)
        update_attrs = {}
        for k, v in attrs.items():
            if k.startswith("__"):
                update_attrs[k] = v

            elif k == "age":
                update_attrs[k] = v

            elif callable(v):
                update_attrs[k] = v
            else:
                cls.allow_l.append(k)
                pass
        update_attrs["allow_l"] = cls.allow_l
        # update_attrs["allow"] = cls.allow()
        return super(AnimalType, cls).__new__(cls, name, bases, update_attrs)


class Animal(metaclass=AnimalType):
    # __metaclass__ = AnimalType
    # def __init__(self):
    #     print(self.__class__)
    # def add(self):
    #     return self.add()
    name = None
    age = None

    def __init__(self, **kwargs):
        print(dir(self))
        for k, v in kwargs.items():
            if k in self.allow_l:
                print(k, v)
                self.name = v
                setattr(self, "%s" % k, self)
        print(dir(self), "af")
        print(self.name)


    def first_name(self):
        name = self.name[0]
        return name

    pass


# class PlantType(type):
#     def __new__(cls, name, bases, attrs):
#         attrs['delete'] = cls.winter(cls)
#
#         super(PlantType, cls).__new__(cls, name, bases, attrs)
#
#     def winter(self):
#         return "变成植物"


# class Plant(metaclass=PlantType):
#     pass


# class WormGrass(object):
#     name = None
#
#     def __init__(self, **kwargs):
#         self.name = kwargs.get("name")


# def behavior(self):
#     print("夏天%s，冬天%s" % (self.summer(), self.winter()))


# wormgrass = WormGrass()
# wormgrass.behavior()

# print(wormgrass.summer())
# a = WormGrass()
a = Animal(name="ABC")
print(a.name.first_name(), "la")
