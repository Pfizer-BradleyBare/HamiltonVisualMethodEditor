from ....Tools.Command.Command import Command
from .GetPlateOptions import GetPlateOptions


class GetPlateCommand(Command):
    def __init__(
        self, Name: str, CustomErrorHandling: bool, OptionsInstance: GetPlateOptions
    ):
        Command.__init__(self, Name, CustomErrorHandling)
        self.OptionsInstance: GetPlateOptions = OptionsInstance

    def GetModuleName(self) -> str:
        return "Transport IPG"

    def GetCommandName(self) -> str:
        return "Get Plate"

    def GetResponseKeys(self) -> list[str]:
        return []

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        OutputDict = vars(self.OptionsInstance)
        OutputDict["CustomErrorHandling"] = self.CustomErrorHandling
        return OutputDict
