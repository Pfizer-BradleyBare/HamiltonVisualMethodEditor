from ...Tools.Command.Command import Command
from .StopPressureControlOptions import StopPressureControlOptions


class StopPressureControlCommand(Command):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        OptionsInstance: StopPressureControlOptions,
    ):
        Command.__init__(self, Name, CustomErrorHandling)
        self.OptionsInstance: StopPressureControlOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Vacuum"

    def GetCommandName(self) -> str:
        return "Stop Pressure Control"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)
        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling
        return OutputDict
