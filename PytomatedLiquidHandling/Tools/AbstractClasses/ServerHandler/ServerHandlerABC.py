import os
from abc import ABC, abstractmethod
from typing import Self

import web

from ...Logger import Logger


class ServerHandlerABC(ABC):
    __DerivedInstances: list[Self] = list()
    __ServerStartedState: bool = False

    @classmethod
    def IsAlive(cls):
        return ServerHandlerABC.__ServerStartedState

    @classmethod
    def GetURLS(cls) -> tuple:
        Urls = ()

        for DerivedInstance in ServerHandlerABC.__DerivedInstances:
            Urls += DerivedInstance.GetEndpoints()

        return Urls

    @classmethod
    def StartServer(cls, Port: str = "255"):

        # Add endpoints as addresses we can access over HTTP

        os.environ["PORT"] = Port

        if ServerHandlerABC.__ServerStartedState is not True:
            ServerHandlerABC.__ServerStartedState = True
            web.application(ServerHandlerABC.GetURLS(), globals()).run()

    @classmethod
    def KillServer(cls):
        List = [
            DerivedInstance for DerivedInstance in ServerHandlerABC.__DerivedInstances
        ]

        for DerivedInstance in List:
            ServerHandlerABC.__DerivedInstances.remove(DerivedInstance)
            DerivedInstance.Kill()

        ServerHandlerABC.__ServerStartedState = False

    def __init__(self, LoggerInstance: Logger):
        ServerHandlerABC.__DerivedInstances.append(self)

        self.LoggerInstance: Logger = LoggerInstance

    def GetLogger(self) -> Logger:
        return self.LoggerInstance

    @abstractmethod
    def GetEndpoints(self) -> tuple:
        ...

    @abstractmethod
    def Kill(self):
        ...