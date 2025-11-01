from .file import File
from .datafile import DataFile
class Folder(DataFile, File): pass
class WebSiteFolder(Folder): pass