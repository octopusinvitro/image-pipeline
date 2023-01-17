import os


class Configuration:
    OUTPUT_FOLDER = './output'
    MAXIMUM_ASSET_SIZE = 2000
    MAXIMUM_THUMB_SIZE = 500

    def __init__(self, red_band_path, green_band_path):
        self._red_band_path = red_band_path
        self._green_band_path = green_band_path

    def blue_band_path(self):
        bluename = self._output_path(self._red_band_path, '')
        bluename = bluename.replace('-vv-', '-vh-vv-')
        return bluename.replace('-001', '-003')

    def red_cog_path(self):
        return self._output_path(self._red_band_path, '-red')

    def green_cog_path(self):
        return self._output_path(self._green_band_path, '-green')

    def blue_cog_path(self):
        return self._output_path(self.blue_band_path(), '-blue')

    def asset_path(self, fullpath):
        filename, extension = self._splitext(fullpath)
        assetname = f'{filename}.webp'
        return self._normalized_path(assetname)

    def thumbnail_path(self, fullpath):
        filename, extension = self._splitext(fullpath)
        thumbname = f'{filename}-thumbnail{extension}'
        return self._normalized_path(thumbname)

    def rgb_path(self):
        rgbname = self.red_cog_path().replace('-vv-', '-')
        return rgbname.replace('-001-red.tiff', '-123-rgb.webp')

    def _output_path(self, input_path, modifier):
        filename, extension = self._splitext(input_path)
        outname = f'{filename}{modifier}{extension}'
        return self._normalized_path(outname)

    def _splitext(self, filename):
        basename = os.path.basename(filename)
        return os.path.splitext(basename)

    def _normalized_path(self, filename):
        return os.path.normpath(os.path.join(self.OUTPUT_FOLDER, filename))
