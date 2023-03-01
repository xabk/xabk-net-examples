import polib
import argparse
from pathlib import Path

# --- DEFAULTS ---
ENC = "utf-8-sig"
# Default encoding for PO files.
# Set to your default PO encoding to use the script with less parameters

DEF_FN = 'Game.po'
# Default PO file name.
# Change to your default file name to use the script with less parameters

BACKUP_DIRECTORY = 'backup-sort-po'

WRAP = 0  # Wrap width for saving PO files

def main():
  parser = argparse.ArgumentParser(
    description='''
    Sort PO files by source reference 
    to fix Unreal Engine randomized string order
    By default, creates backups in 'backup` directory
    
    Usage: sort-po.py filename
    
    You can also drag and drop one or more PO files
    on the sort-po.py file
    '''
  )

  parser.add_argument(
    'filenames',
    type=str,
    nargs='*',
    default=[DEF_FN],
    help='Filename(s)',
  )

  parser.add_argument(
    '-encoding',
    '-e',
    type=str,
    nargs='?',
    default=ENC,
    help='Encoding of the PO file ',
  )

  args = parser.parse_args()

  if not args.filenames:
    print('Specify the filename in script parameters.')
    parser.print_help()
    input('Press Enter to close...')
    return 1
  
  files_to_sort = [Path(f).absolute().resolve() for f in args.filenames]

  processed_files = []
  
  for file in files_to_sort:
    print(f'Sorting {file}')
    if not file.exists() or not file.is_file():
      print(f' - Error: {file} not found or is not a file')
      continue

    pofile = polib.pofile(file, encoding=args.encoding, wrapwidth=WRAP)
    if len(pofile) == 0:
      print(f' - Error: no entries loaded for {file}')
      continue

    if BACKUP_DIRECTORY:
      backup_file = file.parent / BACKUP_DIRECTORY / file.name
      if not backup_file.parent.exists():
        backup_file.parent.mkdir()
      print(f' - Saving backup {backup_file}')
      pofile.save(backup_file)

    pofile.sort()

    try:
      pofile.save(file)
    except:
      print(f' - Error while saving sorted {file}')
      continue

    print(f' - Sorted and saved {file}')
    
    processed_files.append(file)

  print(' --- --- --- --- --- ')
  if len(processed_files) != len(files_to_sort):
    if len(processed_files) == 0:
      print(f'No files have been sorted. Check input parameters:')
      for file in files_to_sort:
        print(file)
      input('Press Enter to close...')
      return 2
      
    print(f'Sorted files ({len(processed_files)}/{len(files_to_sort)}):')
    for file in processed_files:
      print(' -', file)
    failed_files = [f for f in files_to_sort if f not in processed_files]
    print(f'Failed to sort ({len(failed_files)}):')
    for file in failed_files:
      print(' -', file)
    input('Press Enter to close...')
    return 3
  
  print(f'Processed all files ({len(processed_files)}):')
  for file in processed_files:
    print(' -', file)

  input('Press Enter to close...')

  return 0

if __name__ == "__main__":
  main()