import rasterio

from ..status import Status


class BlueBandCreator:
    def __init__(self, red_path, green_path, blue_path, diagnostics):
        self._red_path = red_path
        self._green_path = green_path
        self._blue_path = blue_path
        self._diagnostics = diagnostics

    def run(self):
        blue_bands, profile = self._calculate_blue_channel()
        self._write(blue_bands, profile)
        self._log_success()

    def _calculate_blue_channel(self):
        red = rasterio.open(self._red_path)
        green = rasterio.open(self._green_path)
        blue_bands = green.read() - red.read()

        return (blue_bands, red.profile)

    def _write(self, bands, profile):
        with rasterio.open(self._blue_path, 'w', **profile) as file:
            file.write(bands)

    def _log_success(self):
        self._diagnostics.log(self._blue_path, Status.BLUE_CHANNEL_CREATED)
