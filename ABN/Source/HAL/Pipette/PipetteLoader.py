import yaml

from ..Tip.BaseTip import TipTracker
from .Pipette import Pipette8Channel, Pipette96Channel, PipettingDeviceTypes
from .PipetteTip.LiquidClass.LiquidClass import LiquidClass
from .PipetteTip.LiquidClass.LiquidClassCategory import LiquidClassCategory
from .PipetteTip.LiquidClass.LiquidClassCategoryTracker import (
    LiquidClassCategoryTracker,
)
from .PipetteTip.PipetteTip import PipetteTip
from .PipetteTip.PipetteTipTracker import PipetteTipTracker
from .PipetteTracker import PipetteTracker


def LoadYaml(
    PipetteTrackerInstance: PipetteTracker,
    TipTrackerInstance: TipTracker,
    FilePath: str,
):
    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for Device in ConfigFile["Device IDs"]:
        Enabled = ConfigFile["Device IDs"][Device]["Enabled"]

        PipetteTipTrackerInstance = PipetteTipTracker()

        for Tip in ConfigFile["Device IDs"][Device]["Supported Tips"]:

            TipInstance = TipTrackerInstance.GetObjectByName(Tip)
            PickupSequence = ConfigFile["Device IDs"][Device]["Supported Tips"][Tip][
                "Pickup Sequence"
            ]
            DropoffSequence = ConfigFile["Device IDs"][Device]["Supported Tips"][Tip][
                "Drop Off Sequence"
            ]
            WasteSequence = ConfigFile["Device IDs"][Device]["Supported Tips"][Tip][
                "Waste Sequence"
            ]

            LiquidClassCategoryTrackerInstance = LiquidClassCategoryTracker()

            for LiquidClassID in ConfigFile["Device IDs"][Device]["Supported Tips"][
                "Liquid Class IDs"
            ]:
                LiquidClassCategoryInstance = LiquidClassCategory(LiquidClassID)

                for LiquidClassItem in ConfigFile["Device IDs"][Device][
                    "Supported Tips"
                ]["Liquid Class IDs"][LiquidClassID]:

                    MaxVolume = ConfigFile["Device IDs"][Device]["Supported Tips"][
                        "Liquid Class IDs"
                    ][LiquidClassID][LiquidClassItem]["Max Volume"]

                    Name = ConfigFile["Device IDs"][Device]["Supported Tips"][
                        "Liquid Class IDs"
                    ][LiquidClassID][LiquidClassItem]["Max Volume"]

                    LiquidClassCategoryInstance.ManualLoad(LiquidClass(Name, MaxVolume))

                LiquidClassCategoryTrackerInstance.ManualLoad(
                    LiquidClassCategoryInstance
                )

            PipetteTipTrackerInstance.ManualLoad(
                PipetteTip(
                    TipInstance,
                    LiquidClassCategoryTrackerInstance,
                    PickupSequence,
                    DropoffSequence,
                    WasteSequence,
                )
            )

        PipetteDeviceType = PipettingDeviceTypes(Device)

        if PipetteDeviceType == PipettingDeviceTypes.Pipette8Channel:

            PipetteTrackerInstance.ManualLoad(
                Pipette8Channel(
                    Enabled,
                    PipetteTipTrackerInstance,
                    ConfigFile["Device IDs"][Device]["Active Channels"],
                )
            )

        if PipetteDeviceType == PipettingDeviceTypes.Pipette96Channel:
            PipetteTrackerInstance.ManualLoad(
                Pipette96Channel(Enabled, PipetteTipTrackerInstance)
            )
