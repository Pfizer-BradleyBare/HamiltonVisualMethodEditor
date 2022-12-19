from enum import Enum
from typing import cast

from .BaseSolutionProperty.SolutionProperty import SolutionPropertyValue


class ViscositySolutionProperty(Enum):
    Low = SolutionPropertyValue(1, 0, 0)
    Medium = SolutionPropertyValue(1, 0, 0)
    High = SolutionPropertyValue(1, 0, 0)

    @classmethod
    def GetByNumericKey(cls, NumericKey: int) -> ViscositySolutionProperty:  # type: ignore
        for Item in ViscositySolutionProperty:
            if Item.value.GetNumericValue() == NumericKey:
                return Item