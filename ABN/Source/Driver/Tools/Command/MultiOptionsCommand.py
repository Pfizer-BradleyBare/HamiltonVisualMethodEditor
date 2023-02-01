from collections import defaultdict
from typing import Generic, TypeVar

from ....Tools.AbstractClasses import NonUniqueItemTrackerABC
from .BaseCommand import Command

T = TypeVar("T", bound="NonUniqueItemTrackerABC")


class MultiOptionsCommand(Command, Generic[T]):
    def __init__(self, Name: str, OptionsTrackerInstance: T, CustomErrorHandling: bool):
        Command.__init__(self, Name, CustomErrorHandling)
        self.OptionTrackerInstance: T = OptionsTrackerInstance

    def GetCommandParameters(self) -> dict[str, any]:  # type:ignore
        OutputDict = defaultdict(list)

        for Options in self.OptionTrackerInstance.GetObjectsAsList():
            OptionsDict = vars(Options)

            for key, value in OptionsDict.items():
                OutputDict[key].append(value)

        return OutputDict
