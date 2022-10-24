import time
from ....AbstractClasses import ObjectABC
from ...Workbook import Block
from typing import Callable


class Timer(ObjectABC):
    def __init__(
        self,
        WaitTimeSeconds: float,
        WaitReason: str,
        BlockInstance: Block,
        CallbackFunction: Callable[[Block], None],
    ):
        self.WaitTimeSeconds: float = WaitTimeSeconds
        self.WaitTimeEnd: float = time.time() + WaitTimeSeconds
        self.WaitReason: str = WaitReason
        self.BlockInstance: Block = BlockInstance
        self.CallbackFunction: Callable[[Block], None] = CallbackFunction

    def GetName(self) -> str:
        return "Timer: " + self.BlockInstance.GetName()

    def GetWaitTime(self) -> float:
        return self.WaitTimeSeconds

    def GetRemainingWaitTime(self) -> float:
        return self.WaitTimeEnd - time.time()

    def GetWaitReason(self) -> str:
        return self.WaitReason

    def ExecuteCallbackFunction(self) -> None:
        self.CallbackFunction(self.BlockInstance)