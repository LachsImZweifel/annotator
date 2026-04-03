import pathlib

BASE_DIR = pathlib.Path(__file__).parent.parent.resolve()

#Library Constants
SUPPORTED_FORMATS = {
        '.jpg', '.jpeg', '.jpe',        # JPEG Formate
        '.png',                         # Portable Network Graphics
        '.bmp', '.dib',                 # Windows Bitmaps
        '.webp',                        # Google WebP
        '.tiff', '.tif',                # TIFF Formate
        '.jp2',                         # JPEG 2000
        '.pbm', '.pgm', '.ppm', '.pxm', # Portable Messwerte
        '.sr', '.ras',                  # Sun Rasters
        '.hdr', '.pic'                  # HDR Formate
}