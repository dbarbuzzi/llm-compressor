import pytest

from collections import OrderedDict
import tempfile
import torch
from torch.nn import Sequential, Linear

from neuralmagicML.pytorch.utils import ModuleExporter


EXPORT_MODEL = Sequential(
    OrderedDict(
        [
            ("fc1", Linear(8, 16, bias=True)),
            ("fc2", Linear(16, 32, bias=True)),
            (
                "block1",
                Sequential(
                    OrderedDict(
                        [
                            ("fc1", Linear(32, 16, bias=True)),
                            ("fc2", Linear(16, 8, bias=True)),
                        ]
                    )
                ),
            ),
        ]
    )
)


def test_exporter_onnx():
    sample_batch = torch.randn(1, 8)
    exporter = ModuleExporter(EXPORT_MODEL, tempfile.gettempdir())
    exporter.export_onnx(sample_batch)


@pytest.mark.parametrize("batch_size", [1, 64])
def test_export_batches(batch_size):
    sample_batch = torch.randn(batch_size, 8)
    exporter = ModuleExporter(EXPORT_MODEL, tempfile.gettempdir())
    exporter.export_samples([sample_batch])
