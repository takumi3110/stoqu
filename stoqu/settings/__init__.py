from .production import *

try:
	from .local import *
except Exception as e:
	pass
