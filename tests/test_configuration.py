from unittest import TestCase

from pipeline.configuration import Configuration


class TestConfiguration(TestCase):
    def test_builds_blue_band_path_from_red_path(self):
        red_band_path = 'path/to/image-vv-foo-001.tiff'
        blue_band_path = 'output/image-vh-vv-foo-003.tiff'
        self.assertEqual(Configuration(red_band_path, 'irrelevant').blue_band_path(), blue_band_path)

    def test_builds_red_cog_path(self):
        red_band_path = 'path/to/image.tiff'
        red_cog_path = 'output/image-red.tiff'
        self.assertEqual(Configuration(red_band_path, 'irrelevant').red_cog_path(), red_cog_path)

    def test_builds_green_cog_path(self):
        green_band_path = 'path/to/image.tiff'
        green_cog_path = 'output/image-green.tiff'
        self.assertEqual(Configuration('irrelevant', green_band_path).green_cog_path(), green_cog_path)

    def test_builds_blue_cog_path_from_red_path(self):
        red_band_path = 'path/to/image-vv-foo-001.tiff'
        blue_cog_path = 'output/image-vh-vv-foo-003-blue.tiff'
        self.assertEqual(Configuration(red_band_path, 'irrelevant').blue_cog_path(), blue_cog_path)

    def test_builds_asset_path_from_fullpath(self):
        fullpath = 'path/to/image-vv-foo-001.tiff'
        assetpath = 'output/image-vv-foo-001.webp'
        self.assertEqual(Configuration(fullpath, 'irrelevant').asset_path(fullpath), assetpath)

    def test_builds_thumbnail_path_from_fullpath(self):
        fullpath = 'output/image-vv-foo-001.webp'
        thumbpath = 'output/image-vv-foo-001-thumbnail.webp'
        self.assertEqual(Configuration(fullpath, 'irrelevant').thumbnail_path(fullpath), thumbpath)

    def test_builds_rgb_path_from_red_path(self):
        red_band_path = 'path/to/image-vv-foo-001.tiff'
        rgb_path = 'output/image-foo-123-rgb.webp'
        self.assertEqual(Configuration(red_band_path, 'irrelevant').rgb_path(), rgb_path)
