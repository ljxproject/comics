from api.helpers import r
from api.helpers.code.en import *
from api.helpers.code.zh import *
from api.helpers.code.vi import *
from api.helpers.code.ms import *

EnumBase.set_d()
lang = ["en", "vi", "zh", "ms"]
r.set("lang", lang)
