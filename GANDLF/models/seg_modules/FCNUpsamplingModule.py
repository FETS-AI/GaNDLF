import torch
import torch.nn as nn
import torch.nn.functional as F
from GANDLF.models.seg_modules.Interpolate import Interpolate


class FCNUpsamplingModule(nn.Module):
    def __init__(
        self,
        input_channels,
        output_channels,
        conv=nn.Conv2d,
        conv_kwargs=None,
        scale_factor=2,
    ):
        nn.Module.__init__(self)
        if conv_kwargs is None:
            conv_kwargs = {"kernel_size": 1, "stride": 1, "padding": 0, "bias": True}

        if conv == nn.Conv2d:
            mode = "bilinear"
        else:
            mode = "trilinear"
        self.interp_kwargs = {
            "size": None,
            "scale_factor": 2 ** (scale_factor - 1),
            "mode": mode,
            "align_corners": True,
        }
        self.interpolate = Interpolate(interp_kwargs=self.interp_kwargs)

        self.conv0 = conv(input_channels, output_channels, **conv_kwargs)

    def forward(self, x):
        """[summary]

        [description]

        Extends:
        """
        x = self.interpolate(self.conv0(x))
        return x
