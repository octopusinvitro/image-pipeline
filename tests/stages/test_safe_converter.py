from io import StringIO
from pathlib import Path
import sys

from unittest import skip, TestCase
from unittest.mock import patch

from pipeline.diagnostics import Diagnostics
from pipeline.status import Status
from pipeline.stages.safe_converter import (
    InvalidCOGError, InvalidInputError, SAFEConverter
)

from tests.paths import clear_files, fixtures_path, output_path


class TestSAFEConverter(TestCase):
    def setUp(self):
        sys.stdout = StringIO()

        self.invalid = (False, ['error1', 'error2'], ['warn1', 'warn2'])

        self.input = fixtures_path('sentinel.tiff')
        self.output = output_path('sentinel-cog.tiff')
        self.converter = SAFEConverter(self.input, self.output, Diagnostics())

    def tearDown(self):
        sys.stdout = sys.__stdout__
        clear_files()

    @skip
    def test_converts_tiff_to_cog_successfully(self):
        self.converter.run()
        self.assertTrue(Path(self.output).is_file())

    @skip
    @patch.object(Diagnostics, 'log')
    def test_logs_diagnostics_if_conversion_is_successful(self, log_spy):
        self.converter.run()
        log_spy.assert_called_with(self.output, Status.COG_CREATED)

    @skip
    def test_raises_error_if_file_is_missing(self):
        with self.assertRaises(InvalidInputError) as error:
            SAFEConverter('inextistent.tiff', 'irrelevant', Diagnostics()).run()
        self.assertEqual(str(error.exception), 'Invalid path: inextistent.tiff')

    @skip
    @patch.object(Diagnostics, 'log')
    def test_logs_diagnostics_if_file_is_missing(self, log_spy):
        with self.assertRaises(InvalidInputError):
            SAFEConverter('inextistent.tiff', 'irrelevant', Diagnostics()).run()
        log_spy.assert_called_with('irrelevant', Status.INVALID_PATH)

    @skip
    @patch('rio_cogeo.cogeo.cog_validate')
    def test_raises_error_if_cog_is_invalid(self, cog_validate_mock):
        cog_validate_mock.return_value = self.invalid

        with self.assertRaises(InvalidCOGError) as error:
            self.converter.run()

        message = 'Invalid COG: output. Errors: error1, error2. Warnings: warn1, warn2'
        self.assertEqual(str(error.exception), message)

    @skip
    @patch('rio_cogeo.cogeo.cog_validate')
    @patch.object(Diagnostics, 'log')
    def test_logs_diagnostics_if_cog_is_invalid(self, log_spy, cog_validate_mock):
        cog_validate_mock.return_value = self.invalid

        with self.assertRaises(InvalidInputError):
            self.converter.run()

        log_spy.assert_called_with(self.output, Status.INVALID_COG)
