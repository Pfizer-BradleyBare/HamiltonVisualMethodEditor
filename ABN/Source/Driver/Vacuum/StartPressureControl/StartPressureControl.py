from ...Tools.Command.Command import Command
from .StartPressureControlOptions import StartPressureControlOptions


class StartPressureControlCommand(Command):
    def __init__(self, Name: str, OptionsInstance: StartPressureControlOptions):
        Command.__init__(self)
        self.Name: str = Name
        self.OptionsInstance: StartPressureControlOptions = OptionsInstance

    def GetName(self) -> str:
        return self.Name

    def GetModuleName(self) -> str:
        return "Vacuum"

    def GetCommandName(self) -> str:
        return "Start Pressure Control"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)