from ...HAL.Lid import Lid
from ..Handler import GetHandler
from ..Tools.Container.BaseContainer import Container
from ..Tools.LoadedLabware.LoadedLabwareTracker import LoadedLabwareTracker
from ..Transport.Transport import Transport


def Cover(ContainerInstance: Container, LidInstance: Lid, Simulate: bool):

    HandlerInstance = GetHandler()
    LoadedLabwareTrackerInstance = HandlerInstance.LoadedLabwareTrackerInstance

    LoadedLabwareAssignmentInstances = (
        LoadedLabwareTrackerInstance.GetLabwareAssignments(ContainerInstance)
    )

    LoadedLabwareInstance = LoadedLabwareAssignmentInstances.GetObjectsAsList()[0]
    DestinationLayoutItemInstance = (
        LoadedLabwareInstance.LayoutItemGroupingInstance.LidLayoutItemInstance
    )
    if DestinationLayoutItemInstance is None:
        raise Exception(
            "There is not a lid at this location. This is incorrect. Please fix."
        )

    SourceLayoutItemInstance = LidInstance.LidLayoutItem

    Transport(SourceLayoutItemInstance, DestinationLayoutItemInstance, Simulate)
    # Do the transfer