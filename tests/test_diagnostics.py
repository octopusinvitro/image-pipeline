from datetime import datetime
from io import StringIO
import sys

from unittest import TestCase
from unittest.mock import Mock, patch

import pipeline
from pipeline.diagnostics import Diagnostics


class TestDiagnostics(TestCase):
    def setUp(self):
        self.output = StringIO()
        sys.stdout = self.output

    def tearDown(self):
        sys.stdout = sys.__stdout__

    @patch.object(pipeline.diagnostics, 'datetime', Mock(wraps=datetime))
    def test_logs_diagnostics(self):
        utcnow = datetime(2000, 1, 31, 2, 3, 4, 567890)
        pipeline.diagnostics.datetime.utcnow.return_value = utcnow

        Diagnostics().log('filename.tiff', 'status')

        message = '2000-01-31 02:03:04.567890: File: filename.tiff, status: status.'
        self.assertIn(message, self.output.getvalue())
