import numpy
import rasterio
from rasterio.plot import adjust_band
from rasterio.windows import Window
from wand.image import Image

from ..configuration import Configuration
from ..status import Status


class AssetsCreator:
    def __init__(self, paths, configuration, diagnostics):
        self._paths = paths
        self._configuration = configuration
        self._diagnostics = diagnostics

    def run(self):
        overview_trio, thumbnail_trio = self._save_single_assets()
        self._save_rgb_assets(overview_trio, thumbnail_trio)

    def _save_single_assets(self):
        overview_trio = []
        thumbnail_trio = []

        for pair in self._paths:
            input_path, output_path = pair
            dataset = rasterio.open(input_path)

            overview = self._resize(dataset, Configuration.MAXIMUM_ASSET_SIZE)
            thumbnail = self._resize(dataset, Configuration.MAXIMUM_THUMB_SIZE)

            overview_trio.append(overview)
            thumbnail_trio.append(thumbnail)

            self._save(adjust_band(overview), output_path)
            self._save(adjust_band(thumbnail), self._thumbname(output_path))

            self._diagnostics.log(output_path, Status.ASSETS_CREATED)

        return (overview_trio, thumbnail_trio)

    def _save_rgb_assets(self, overview_trio, thumbnail_trio):
        overview = numpy.array(overview_trio).transpose(1, 2, 0)
        thumbnail = numpy.array(thumbnail_trio).transpose(1, 2, 0)

        rgb_path = self._configuration.rgb_path()
        self._save(overview, rgb_path)
        self._save(thumbnail, self._thumbname(rgb_path))

        self._diagnostics.log(rgb_path, Status.RGB_ASSETS_CREATED)

    def _resize(self, dataset, maximum_size):
        factor = maximum_size / self._largest(dataset.width, dataset.height)
        width, height = (round(factor * dataset.width), round(factor * dataset.height))
        return dataset.read(1, window=Window(0, 0, width, height))

    def _largest(self, width, height):
        return width if width > height else height

    def _save(self, band, filename):
        geotiff = Image.from_array(band)
        webp = geotiff.convert('webp')
        webp.save(filename=filename)

    def _thumbname(self, output_path):
        return self._configuration.thumbnail_path(output_path)
