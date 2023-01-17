from .configuration import Configuration
from .diagnostics import Diagnostics
from .stages.assets_creator import AssetsCreator
from .stages.blue_band_creator import BlueBandCreator
from .stages.safe_converter import SAFEConverter


def main(red_band_path, green_band_path):
    configuration = Configuration(red_band_path, green_band_path)
    blue_band_path = configuration.blue_band_path()

    red_cog_path = configuration.red_cog_path()
    green_cog_path = configuration.green_cog_path()
    blue_cog_path = configuration.blue_cog_path()

    red_asset_path = configuration.asset_path(red_band_path)
    green_asset_path = configuration.asset_path(green_band_path)
    blue_asset_path = configuration.asset_path(blue_band_path)

    diagnostics = Diagnostics()

    BlueBandCreator(red_band_path, green_band_path, blue_band_path, diagnostics).run()

    SAFEConverter(red_band_path, red_cog_path, diagnostics).run()
    SAFEConverter(green_band_path, green_cog_path, diagnostics).run()
    SAFEConverter(blue_band_path, blue_cog_path, diagnostics).run()

    paths = [
        [red_band_path, red_asset_path],
        [green_band_path, green_asset_path],
        [blue_band_path, blue_asset_path]
    ]
    AssetsCreator(paths, configuration, diagnostics).run()
