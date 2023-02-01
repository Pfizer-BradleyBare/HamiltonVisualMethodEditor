from ...Globals import GetCommunicationServer
from ..Tools.Container.BaseContainer import Container
from ..Transport import GetLayoutItem, Transport


def MoveToStorage(ContainerInstance: Container, Simulate: bool) -> bool:

    CommunicationServerInstance = GetCommunicationServer()
    APIHandlerInstance = CommunicationServerInstance.APIHandlerInstance
    LoadedLabwareTrackerInstance = APIHandlerInstance.LoadedLabwareTrackerInstance
    ResourceLockTrackerInstance = APIHandlerInstance.ResourceLockTrackerInstance
    HALLayerInstance = APIHandlerInstance.HALLayerInstance

    DeckLocationTrackerInstance = HALLayerInstance.DeckLocationTrackerInstance

    LoadedLabwareAssignmentInstances = (
        LoadedLabwareTrackerInstance.GetLabwareAssignments(ContainerInstance)
    )

    for (
        LoadedLabwareAssignmentInstance
    ) in LoadedLabwareAssignmentInstances.GetObjectsAsList():

        if (
            LoadedLabwareAssignmentInstance.LayoutItemGroupingInstance.GetDeckLocation().IsStorageLocation()
        ):
            continue
        # Is it already in the appropriate location?

        PossibleDeckLocationInstances = [
            Location
            for Location in DeckLocationTrackerInstance.GetObjectsAsList()
            if not ResourceLockTrackerInstance.IsTracked(Location.GetName())
            and Location.IsStorageLocation()
        ]
        # Use filtering to get the possible deck locations

        if len(PossibleDeckLocationInstances) == 0:
            return False

        for PossibleDeckLocationInstance in PossibleDeckLocationInstances:
            DestinationLayoutItemGroupingInstance = GetLayoutItem(
                PossibleDeckLocationInstance,
                LoadedLabwareAssignmentInstance.LayoutItemGroupingInstance.PlateLayoutItemInstance.LabwareInstance,
            )
            # Try to get the layout item for this deck location

            if DestinationLayoutItemGroupingInstance is None:
                continue
            # If there isn't a valid item then we will try the next location

            Transport(
                LoadedLabwareAssignmentInstance.LayoutItemGroupingInstance.PlateLayoutItemInstance,
                DestinationLayoutItemGroupingInstance.PlateLayoutItemInstance,
                Simulate,
            )

            break
            # We moved it! Done with this loop!

    return True
