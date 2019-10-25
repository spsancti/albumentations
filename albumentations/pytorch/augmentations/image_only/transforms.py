import albumentations as A
from . import functional as F
import kornia as K
import torch

import random


__all__ = ["NormalizeTorch", "CoarseDropoutTorch", "RandomSnowTorch"]


class NormalizeTorch(A.Normalize):
    def __init__(
        self, mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225), max_pixel_value=255.0, always_apply=False, p=1.0
    ):
        super(NormalizeTorch, self).__init__(mean, std, max_pixel_value, always_apply, p)
        self.mean = torch.tensor(self.mean) * self.max_pixel_value
        self.std = torch.tensor(self.std) * self.max_pixel_value

    def apply(self, image, **params):
        return K.normalize(image.type(torch.float32), self.mean, self.std)


class CoarseDropoutTorch(A.CoarseDropout):
    def apply(self, image, fill_value=0, holes=(), **params):
        return F.cutout(image, holes, fill_value)

    def get_params_dependent_on_targets(self, params):
        img = params["image"]
        height, width = img.shape[-2:]

        holes = []
        for _n in range(random.randint(self.min_holes, self.max_holes)):
            hole_height = random.randint(self.min_height, self.max_height)
            hole_width = random.randint(self.min_width, self.max_width)

            y1 = random.randint(0, height - hole_height)
            x1 = random.randint(0, width - hole_width)
            y2 = y1 + hole_height
            x2 = x1 + hole_width
            holes.append((x1, y1, x2, y2))

        return {"holes": holes}


class RandomSnowTorch(A.RandomSnow):
    def apply(self, image, snow_point=0.1, **params):
        return F.add_snow(image, snow_point, self.brightness_coeff)