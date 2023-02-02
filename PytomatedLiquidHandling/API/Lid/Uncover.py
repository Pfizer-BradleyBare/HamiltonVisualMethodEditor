from ...HAL.Lid import Lid
from ..Handler import GetHandler
from ..Tools.Container.BaseContainer import Container
from ..Tools.LoadedLabware.LoadedLabwareTracker import LoadedLabwareTracker
from ..Transport.Transport import Transport


def Uncover(ContainerInstance: Container, LidInstance: Lid, Simulate: bool):

    HandlerInstance = GetHandler()
    LoadedLabwareTrackerInstance = HandlerInstance.LoadedLabwareTrackerInstance

    LoadedLabwareAssignmentInstances = (
        LoadedLabwareTrackerInstance.GetLabwareAssignments(ContainerInstance)
    )

    LoadedLabwareInstance = LoadedLabwareAssignmentInstances.GetObjectsAsList()[0]
    SourceLayoutItemInstance = (
        LoadedLabwareInstance.LayoutItemGroupingInstance.LidLayoutItemInstance
    )

    DestinationLayoutItemInstance = LidInstance.LidLayoutItem

    Transport(
        SourceLayoutItemInstance, DestinationLayoutItemInstance, Simulate  # type:ignore
    )
    # Do the transfer