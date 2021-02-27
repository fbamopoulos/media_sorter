import os
import PIL
from PIL import Image
from hachoir.parser import createParser
from hachoir.metadata import extractMetadata

DATE_TIME_ORIG_TAG = 36867

imgFormats = ['png', 'jpg', 'jpeg']
videoFormats = ['m4v', 'mov', 'mp4']


def get_exif(image_file_path):
    loaded_image = Image.open(image_file_path)
    exif_data = loaded_image.getexif()
    loaded_image.close()
    return exif_data


file_list = [f for f in os.listdir() if os.path.isfile(f)]
for afile in file_list:
    filename = os.fsdecode(afile)
    filename_no_ext = filename.split('.')[0]
    extension = filename.split('.')[1].lower()
    if os.path.isfile(filename):
        if extension in imgFormats:
            print(f"Processing {filename}")
            try:
                exif = get_exif(afile)
                if DATE_TIME_ORIG_TAG in exif:
                    print(f"File has DateTimeOriginal EXIF tag: {exif[DATE_TIME_ORIG_TAG]}")
                    date_time_prefix = exif[DATE_TIME_ORIG_TAG].replace(':', '').replace(' ', '_')+'_'
                    if not filename.startswith(date_time_prefix):
                        print(f'Prefix: {date_time_prefix}')
                        print('Renaming...')
                        os.rename(filename, date_time_prefix+filename)
                print()
            except FileNotFoundError:
                print('File could not be found')
            except PIL.UnidentifiedImageError:
                print('File could not be opened and identified')
            except ValueError as e:
                print(e)
            except TypeError as e:
                print(e)
        elif extension in videoFormats:
            print(f"Processing {filename}")
            parser = createParser(filename)
            if not parser:
                print("Unable to parse file %s" % filename)
                continue
            with parser:
                try:
                    metadata = extractMetadata(parser)
                except Exception as err:
                    print("Metadata extraction error: %s" % err)
                    metadata = None
            if not metadata:
                print("Unable to extract metadata")
                continue
            for line in metadata.exportPlaintext():
                creation_date_line_prefix = '- Creation date: '
                if line.startswith(creation_date_line_prefix):
                    line = line[len(creation_date_line_prefix):]
                    date_time_prefix = line.replace('-', '').replace(':', '').replace(' ', '_') + '_'
                    if not filename.startswith(date_time_prefix):
                        print(f'Prefix: {date_time_prefix}')
                        print('Renaming...')
                        os.rename(filename, date_time_prefix+filename)
                    break
