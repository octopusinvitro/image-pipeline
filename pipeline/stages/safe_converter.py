from pathlib import Path

from osgeo import gdal
from rio_cogeo.cogeo import cog_validate

from ..status import Status


class InvalidCOGError(Exception):
    def __init__(self, output_path, errors, warnings):
        message = f'Invalid COG: {output_path}'
        message += '. Errors: ' + ', '.join(errors)
        message += '. Warnings: ' + ', '.join(warnings)
        super().__init__(message)


class InvalidInputError(Exception):
    def __init__(self, input_path):
        super().__init__(f'Invalid path: {input_path}')


class SAFEConverter:
    FILE_FORMAT = 'COG'

    def __init__(self, input_path, output_path, diagnostics):
        self._input_path = input_path
        self._output_path = output_path
        self._diagnostics = diagnostics

    def run(self):
        dataset = self._dataset()

        self._convert(dataset)
        self._validate()
        self._log_success()

        dataset = None

    def _dataset(self):
        path = Path(self._input_path)
        if not path.is_file():
            self._diagnostics.log(self._output_path, Status.INVALID_PATH)
            raise InvalidInputError(self._input_path)

        return gdal.Open(self._input_path, gdal.GA_ReadOnly)

    def _convert(self, dataset):
        driver = gdal.GetDriverByName(self.FILE_FORMAT)

        output = driver.CreateCopy(
            self._output_path, dataset, strict=0,
            options=['COMPRESS=LZW', 'PREDICTOR=NO', 'SPARSE_OK=FALSE']
        )

        output = None  # noqa: F841

    def _validate(self):
        valid, errors, warnings = cog_validate(self._output_path)
        if not valid:
            self._diagnostics.log(self._output_path, Status.INVALID_COG)
            raise InvalidCOGError(self._output_path, errors, warnings)

    def _log_success(self):
        self._diagnostics.log(self._output_path, Status.COG_CREATED)
