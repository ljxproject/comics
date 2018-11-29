import string


def hump_to_attr(hump):
    key_l = ["IP", "ID"]
    key_u = string.ascii_uppercase
    for key in key_l:
        position = hump.find(key)
        if position > -1:
            hump = hump.replace(key, "_%s_" % key.lower())
    for i in key_u:
        position = hump.find(i)
        if position > -1:
            hump = hump.replace(i, "_%s" % i.lower())
    hump = hump.replace("__", "_").strip("_")
    return hump


def attr_to_hump(string):
    s_l = string.split("_")
    key_l = ["ip", "id"]
    n_i = ""
    for i in range(len(s_l)):
        if i == 0:
            n_i += s_l[i]
        else:
            if s_l[i] in key_l:
                n_i += s_l[i].upper()
            else:
                n_i += s_l[i].title()
    return n_i
