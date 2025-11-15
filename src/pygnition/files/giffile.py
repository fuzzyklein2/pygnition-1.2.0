from .files import File
from .imagefile import ImageFile

@File.register_ext('.gif')
class GIFFile(ImageFile): pass