# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------

"""
Converters for operators necessary for supporting scikit-learn Pipelines.
"""

from distutils.version import LooseVersion
import numpy as np
from onnxconverter_common.registration import register_converter
import torch

from ._base_operator import BaseOperator


class Concat(BaseOperator, torch.nn.Module):
    def __init__(self):
        super(Concat, self).__init__(transformer=True)

    def forward(self, *x):
        if len(x[0].shape) > 1:
            if LooseVersion(torch.__version__) < LooseVersion("1.6.0"):
                # Concat for pytorch < 1.6.0 has problems when types don't match. We need to explictly cast the tensors.
                dtypes = {t.dtype for t in x}
                if len(dtypes) > 1:
                    if torch.float64 in dtypes:
                        x = [t.double() for t in x]
                    else:
                        raise RuntimeError(
                            "Combination of data types for Concat input tensors not supported. Please fill an issue at https://github.com/microsoft/hummingbird."
                        )
            return torch.cat(x, dim=1)
        else:
            return torch.stack(x, dim=1)
