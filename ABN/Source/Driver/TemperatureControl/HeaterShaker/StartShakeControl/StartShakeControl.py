from ....Tools.Command.Command import Command
from .StartShakeControlOptions import StartShakeControlOptions


class StartShakeControlCommand(Command):
    def __init__(self, Name: str, OptionsInstance: StartShakeControlOptions):
        Command.__init__(self)
        self.Name: str = Name
        self.OptionsInstance: StartShakeControlOptions = OptionsInstance

    def GetName(self) -> str:
        return self.Name

    def GetModuleName(self) -> str:
        return "Temperature Control HeaterShaker"

    def GetCommandName(self) -> str:
        return "Start Shake Control"

    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        return vars(self.OptionsInstance)