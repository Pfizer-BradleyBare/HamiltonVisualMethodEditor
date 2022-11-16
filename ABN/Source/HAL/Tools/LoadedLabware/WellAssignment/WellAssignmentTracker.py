from .....Tools.AbstractClasses import TrackerABC
from .WellAssignment import WellAssignment


class WellAssignmentTracker(TrackerABC[WellAssignment]):
    def GetObjectByName(self, MethodName: str, SampleName: str) -> WellAssignment:
        return super().GetObjectByName(MethodName + " - " + SampleName)
