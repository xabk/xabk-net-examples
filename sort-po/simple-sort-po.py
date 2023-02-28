import polib

file_path = "c:/paste/path/to/your/po"

pofile = polib.pofile(
  file_path,
  wrapwidth=0,
  encoding='utf-8-sig'
)
pofile.sort()
pofile.save()
