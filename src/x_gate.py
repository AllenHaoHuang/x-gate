import math

import torch
import torch.nn as nn


class XAT(nn.Module):

    def __init__(self):
        super(XAT, self).__init__()
        self.alpha = nn.Parameter(torch.zeros(1))
        self.half_pi = math.pi / 2
        self.inv_pi = 1 / math.pi

    def forward(self, x):
        gate = torch.arctan(x)
        return gate * (self.inv_pi * (1 + 2 * self.alpha)) + 0.5


class XGE(nn.Module):

    def __init__(self):
        super(XGE, self).__init__()
        self.alpha = nn.Parameter(torch.zeros(1))
        self.inv_sqrt2 = 1 / math.sqrt(2)

    def forward(self, x):
        gate = torch.erf(x * self.inv_sqrt2)
        return gate * (0.5 + self.alpha) + 0.5


class XSig(nn.Module):

    def __init__(self):
        super(XSig, self).__init__()
        self.alpha = nn.Parameter(torch.zeros(1))

    def forward(self, x):
        gate = torch.sigmoid(x)
        return gate * (1 + 2 * self.alpha) - self.alpha


class XATLU(nn.Module):

    def __init__(self):
        super(XATLU, self).__init__()
        self.gate = XAT()

    def forward(self, x):
        return self.gate(x) * x


class XGELU(nn.Module):

    def __init__(self):
        super(XGELU, self).__init__()
        self.gate = XGE()

    def forward(self, x):
        return self.gate(x) * x


class XSiLU(nn.Module):

    def __init__(self):
        super(XSiLU, self).__init__()
        self.gate = XSig()

    def forward(self, x):
        return self.gate(x) * x


class ATGLU(nn.Module):

    def __init__(self, order=2):
        super(ATGLU, self).__init__()
        assert order in [1, 2], "order must be either 1 or 2"
        self.order = order
        self.half_pi = math.pi / 2
        self.inv_pi = 1 / math.pi

    def forward(self, x):
        assert x.shape[-1] % 2 == 0, "dimension must be even"
        x, y = x.chunk(2, dim=-1)
        gate = (torch.arctan(x) + self.half_pi) * self.inv_pi
        if self.order == 1:
            return gate * y
        else:
            return gate * x * y


class XATGLU(nn.Module):

    def __init__(self, order=1):
        super(XATGLU, self).__init__()
        assert order in [1, 2], "order must be either 1 or 2"
        self.order = order
        self.gate = XAT()

    def forward(self, x):
        assert x.shape[-1] % 2 == 0, "dimension must be even"
        x, y = x.chunk(2, dim=-1)
        if self.order == 1:
            return self.gate(x) * y
        else:
            return self.gate(x) * x * y


class XGEGLU(nn.Module):

    def __init__(self, order=1):
        super(XGEGLU, self).__init__()
        assert order in [1, 2], "order must be either 1 or 2"
        self.order = order
        self.gate = XGE()

    def forward(self, x):
        assert x.shape[-1] % 2 == 0, "dimension must be even"
        x, y = x.chunk(2, dim=-1)
        if self.order == 1:
            return self.gate(x) * y
        else:
            return self.gate(x) * x * y


class XSwiGLU(nn.Module):

    def __init__(self, order=1):
        super(XSwiGLU, self).__init__()
        assert order in [1, 2], "order must be either 1 or 2"
        self.order = order
        self.gate = XSig()

    def forward(self, x):
        assert x.shape[-1] % 2 == 0, "dimension must be even"
        x, y = x.chunk(2, dim=-1)
        if self.order == 1:
            return self.gate(x) * y
        else:
            return self.gate(x) * x * y
