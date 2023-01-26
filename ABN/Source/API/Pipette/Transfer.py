from ...HAL.Pipette import TransferOptions as HALTransferOptions
from ...HAL.Pipette import TransferOptionsTracker as HALTransferOptionsTracker
from ...Server.Globals.HandlerRegistry import GetAPIHandler
from ..Tools.LoadedLabware.LoadedLabwareTracker import (
    LoadedLabware,
    LoadedLabwareTracker,
)
from .Options.TransferOptionsTracker import TransferOptionsTracker


def Transfer(TransferOptionsTrackerInstance: TransferOptionsTracker, Simulate: bool):

    SourceLiquidClassCategories = list()
    DestinationLiquidClassCategories = list()

    for TransferOptions in TransferOptionsTrackerInstance.GetObjectsAsList():

        Volume = TransferOptions.TransferVolume
        SourceContainerInstance = TransferOptions.SourceContainerInstance
        SourceWellNumber = TransferOptions.SourceWellPosition
        DestinationContainerInstance = TransferOptions.DestinationContainerInstance
        DestinationWellNumber = TransferOptions.DestinationWellPosition

        SourceLiquidClassCategories.append(
            SourceContainerInstance.GetLiquidClassCategory().GetName()
        )
        # Get the source liquid class before removing liquid. Becuase that is how it works in real life. Aspirate

        DestinationContainerInstance.Dispense(
            DestinationWellNumber,
            SourceContainerInstance.Aspirate(SourceWellNumber, Volume),
        )

        DestinationLiquidClassCategories.append(
            DestinationContainerInstance.GetLiquidClassCategory().GetName()
        )
        # Get the destination liquid class after adding liquid. Becuase that is how it works in real life. DIspense

    # First we do the "programmatic" transfer

    if Simulate is True:
        return

    LoadedLabwareTrackerInstance: LoadedLabwareTracker = (
        GetAPIHandler().LoadedLabwareTrackerInstance  # type:ignore
    )

    SourceContainerInstances = [
        Options.SourceContainerInstance
        for Options in TransferOptionsTrackerInstance.GetObjectsAsList()
    ]
    DestinationContainerInstances = [
        Options.DestinationContainerInstance
        for Options in TransferOptionsTrackerInstance.GetObjectsAsList()
    ]

    DestinationLoadedLabwareTrackerInstances: list[LoadedLabwareTracker] = list()
    SourceLoadedLabwareTrackerInstances: list[LoadedLabwareTracker] = list()

    for SourceContainerInstance, DestinationContainerInstance in zip(
        SourceContainerInstances, DestinationContainerInstances
    ):

        SourceLoadedLabwareTrackerInstances.append(
            LoadedLabwareTrackerInstance.GetLabwareAssignments(SourceContainerInstance)
        )

        DestinationLoadedLabwareTrackerInstances.append(
            LoadedLabwareTrackerInstance.GetLabwareAssignments(
                DestinationContainerInstance
            )
        )
    # Figure out the loadedlabwares for each container

    DestinationLoadedLabwareInstances: list[LoadedLabware] = list()
    SourceLoadedLabwareInstances: list[LoadedLabware] = list()

    for (
        DestinationLoadedLabwareTrackerInstance,
        SourceLoadedLabwareTrackerInstance,
    ) in zip(
        DestinationLoadedLabwareTrackerInstances, SourceLoadedLabwareTrackerInstances
    ):
        if DestinationLoadedLabwareTrackerInstance.GetNumObjects() > 1:
            raise Exception(
                "Destination containers can only be loaded into a single container. Uh oh!"
            )

        DestinationLoadedLabwareInstance = (
            DestinationLoadedLabwareTrackerInstance.GetObjectsAsList()[0]
        )
        DestinationLoadedLabwareInstances.append(DestinationLoadedLabwareInstance)

        SourceLoadedLabwareInstance = (
            SourceLoadedLabwareTrackerInstance.GetObjectsAsList()[0]
        )
        SourceLoadedLabwareTrackerInstance.ManualUnload(SourceLoadedLabwareInstance)
        SourceLoadedLabwareTrackerInstance.ManualLoad(SourceLoadedLabwareInstance)
        # We effectively want to use each container equally so we unload and reload to put the first at the end
        SourceLoadedLabwareInstances.append(SourceLoadedLabwareInstance)

    # Get for both source and destination a single loaded labware

    SourceProgrammaticWells = [
        Options.SourceWellPosition
        for Options in TransferOptionsTrackerInstance.GetObjectsAsList()
    ]
    DestinationProgrammaticWells = [
        Options.DestinationWellPosition
        for Options in TransferOptionsTrackerInstance.GetObjectsAsList()
    ]

    DestinationLoadedLabwarePhysicalWells: list[int] = list()
    SourceLoadedLabwarePhysicalWells: list[int] = list()

    for (
        SourceProgrammaticWell,
        DestinationProgrammaticWell,
        SourceLoadedLabwareInstance,
        DestinationLoadedLabwareInstance,
        SourceContainerInstance,
        DestinationContainerInstance,
    ) in zip(
        SourceProgrammaticWells,
        DestinationProgrammaticWells,
        SourceLoadedLabwareInstances,
        DestinationLoadedLabwareInstances,
        SourceContainerInstances,
        DestinationContainerInstances,
    ):
        for (
            LoadedLabwareWell
        ) in (
            SourceLoadedLabwareInstance.WellAssignmentTrackerInstance.GetObjectsAsList()
        ):
            if (
                LoadedLabwareWell.TestAsignment(
                    SourceContainerInstance, SourceProgrammaticWell
                )
                is True
            ):
                SourceLoadedLabwarePhysicalWells.append(LoadedLabwareWell.GetName())
                break

        for (
            LoadedLabwareWell
        ) in (
            DestinationLoadedLabwareInstance.WellAssignmentTrackerInstance.GetObjectsAsList()
        ):
            if (
                LoadedLabwareWell.TestAsignment(
                    DestinationContainerInstance, DestinationProgrammaticWell
                )
                is True
            ):
                DestinationLoadedLabwarePhysicalWells.append(
                    LoadedLabwareWell.GetName()
                )
    # figure out the wells

    SourceLabwares = [
        LoadedLabwareInstance.LayoutItemGroupingInstance.PlateLayoutItemInstance.LabwareInstance
        for LoadedLabwareInstance in SourceLoadedLabwareInstances
    ]
    DestinationLabwares = [
        LoadedLabwareInstance.LayoutItemGroupingInstance.PlateLayoutItemInstance.LabwareInstance
        for LoadedLabwareInstance in DestinationLoadedLabwareInstances
    ]

    PipettingDeviceTrackerInstance = (
        TransferOptionsTrackerInstance.PipetteTrackerInstance
    )

    SuitablePipettingDevice = None

    for PipettingDeviceInstance in PipettingDeviceTrackerInstance.GetObjectsAsList():
        if PipettingDeviceInstance.LabwaresSupported(SourceLabwares) is False:
            continue
        if PipettingDeviceInstance.LabwaresSupported(DestinationLabwares) is False:
            continue

        SuitablePipettingDevice = PipettingDeviceInstance
        break
    # Decide which pipetting device to use based off the source and destination labwares

    if SuitablePipettingDevice is None:
        raise Exception(
            "Suitable Pipetting device not found. This should never happen..."
        )

    HALTransferOptionsTrackerInstance = HALTransferOptionsTracker(False)

    Count = 0
    for (
        DestinationLoadedLabwarePhysicalWell,
        SourceLoadedLabwarePhysicalWell,
        DestinationLoadedLabwareInstance,
        SourceLoadedLabwareInstance,
        SourceLiquidClassCategory,
        DestinationLiquidClassCategory,
        TransferOptionsInstance,
    ) in zip(
        DestinationLoadedLabwarePhysicalWells,
        SourceLoadedLabwarePhysicalWells,
        DestinationLoadedLabwareInstances,
        SourceLoadedLabwareInstances,
        SourceLiquidClassCategories,
        DestinationLiquidClassCategories,
        TransferOptionsTrackerInstance.GetObjectsAsList(),
    ):
        HALTransferOptionsTrackerInstance.ManualLoad(
            HALTransferOptions(
                "" + str(Count),
                SourceLoadedLabwareInstance.LayoutItemGroupingInstance.PlateLayoutItemInstance,
                SourceLoadedLabwarePhysicalWell,
                SourceLoadedLabwareInstance.GetWellAssignmentTracker()
                .GetObjectByName(SourceLoadedLabwarePhysicalWell)
                .GetMeasuredVolume(),
                TransferOptionsInstance.SourceMixCycles,
                SourceLiquidClassCategory,
                DestinationLoadedLabwareInstance.LayoutItemGroupingInstance.PlateLayoutItemInstance,
                DestinationLoadedLabwarePhysicalWell,
                DestinationLoadedLabwareInstance.GetWellAssignmentTracker()
                .GetObjectByName(DestinationLoadedLabwarePhysicalWell)
                .GetMeasuredVolume(),
                TransferOptionsInstance.DestinationMixCycles,
                DestinationLiquidClassCategory,
                TransferOptionsInstance.TransferVolume,
            )
        )
        Count += 1

    SuitablePipettingDevice.Transfer(HALTransferOptionsTrackerInstance)
    # Set up the transfer and go
