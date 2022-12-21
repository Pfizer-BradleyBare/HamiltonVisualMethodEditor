from abc import abstractmethod
from threading import Event
from typing import Callable

from ....Tools.AbstractClasses import ObjectABC
from .Response.Response import Response


class Command(ObjectABC):
    def __init__(
        self,
        Name: str,
        CustomErrorHandling: bool,
        CallbackFunction: Callable[[list], None] | None = None,
        CallbackArgs: list | None = None,
    ):
        self.ResponseInstance: Response | None = None
        self.ResponseEvent: Event = Event()
        self.Name: str = Name
        self.CustomErrorHandling: bool = CustomErrorHandling
        self.CallbackFunction: Callable[[list], None] | None = CallbackFunction
        self.CallbackArgs: list | None = CallbackArgs

    def GetName(self) -> str:
        return self.Name

    def GetResponse(self) -> Response:
        if self.ResponseInstance is None:
            raise Exception("Response not set. Did the command timeout?")

        return self.ResponseInstance

    @abstractmethod
    def GetModuleName(self) -> str:
        ...

    @abstractmethod
    def GetCommandName(self) -> str:
        ...

    @abstractmethod
    def GetResponseKeys(self) -> list[str]:
        ...

    @abstractmethod
    def GetCommandParameters(self) -> dict[str, any]:  # type: ignore
        ...
