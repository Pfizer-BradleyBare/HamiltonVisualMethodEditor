import os
from ...AbstractClasses import ObjectABC
from .Block import BlockTracker
from .Worklist import Worklist
from .Solution import SolutionTracker
from enum import Enum
import threading
from ...API.Tools.Container import ContainerTracker
from ...Server.Globals.HalInstance import HalInstance
from ...Server.Globals.AliveStateFlag import AliveStateFlag


class WorkbookStates(Enum):
    Queued = "Queued"
    PreRun = "PreRun"  # This state is where we will do a mock runthrough and *try to* generate the deck loading
    Running = "Running"
    Paused = "Paused"  # The user paused this method manually
    Waiting = "Waiting"  # Something occured so the method is waiting on the user
    Stopped = "Stopped"  # The user stopped the method but it is still in the list. This allows
    # the user to remove plates and all that jazz
    # Killed = "Killed" #The method has been removed from the tracker. It no longer exists


class WorkbookRunTypes(Enum):
    Test = "Test"  # This is a single programmatic test to check method is compatible with system
    Prep = "Prep"  # This will test with all samples added then generate a preparation list for the user
    Run = "Run"  # This will queue to run on the system


# NOTE
#   Workbook contain information about the block pathways, worklist, and solutions
#   A workbook should, ideally, handle the starting and stopping of block pathways
#   Workbook execution should occur as a thread that relies on a thread lock to execute.
#   The workbook thread lock is used to pause workbook execution entirely?
#   The workbook should determine which pathway should be currently executed.
#   How the heck am I going to do this????
#
# ok so this is my plan:
# Thw thread will only read steps. It will not modify the block tracker list at all.
# All modification must occur by the workbook somehow


class Workbook(ObjectABC):
    def __init__(
        self,
        RunType: WorkbookRunTypes,
        MethodPath: str,
        BlockTrackerInstances: list[BlockTracker],
        WorklistInstance: Worklist,
        SolutionTrackerInstance: SolutionTracker,
    ):

        # Thread
        self.WorkbookProcessorThread: threading.Thread = threading.Thread(
            target=WorkbookProcessor,
            args=(self,),  # args must be tuple hence the empty second argument
        )
        self.ProcessingLock: threading.Lock = threading.Lock()
        self.ProcessingLock.acquire()

        # Variables
        self.RunType: WorkbookRunTypes = RunType
        self.MethodPath: str = MethodPath
        self.MethodName: str = os.path.basename(MethodPath)
        self.State: WorkbookStates = WorkbookStates.Queued

        # Trackers
        self.BlockTrackerInstances: list[BlockTracker] = BlockTrackerInstances
        self.WorklistInstance: Worklist = WorklistInstance
        self.SolutionTrackerInstance: SolutionTracker = SolutionTrackerInstance
        self.ContainerTrackerInstance: ContainerTracker = ContainerTracker()

        # Contexts
        self.ActiveContexts: list[str] = list()
        self.InactiveContexts: list[str] = list()

    def GetName(self) -> str:
        return self.MethodName

    def GetPath(self) -> str:
        return self.MethodPath

    def GetState(self) -> WorkbookStates:
        return self.State

    def GetBlockTrackers(self) -> list[BlockTracker]:
        return self.BlockTrackerInstances

    def GetWorklist(self) -> Worklist:
        return self.WorklistInstance

    def GetSolutionTracker(self) -> SolutionTracker:
        return self.SolutionTrackerInstance

    def GetContainerTracker(self) -> ContainerTracker:
        return self.ContainerTrackerInstance

    def GetActiveContexts(self) -> list[str]:
        return self.ActiveContexts

    def GetInactiveContexts(self) -> list[str]:
        return self.InactiveContexts


def WorkbookProcessor(WorkbookInstance: Workbook):
    HalInstance
    while True:

        WorkbookInstance.ProcessingLock.acquire()
        WorkbookInstance.ProcessingLock.release()
        # The processing lock is used as a pause button to control which workbook executes.
        # During acquire we wait for the thread to be unpaused.
        # We immediately release so we do not stall the main process

        if AliveStateFlag is False:
            break

        # do processing here
