import yaml

from .Tip import TipFTR, TipNTR, TipTypes
from .TipTracker import TipTracker


def LoadYaml(TipTrackerInstance: TipTracker, FilePath: str):
    FileHandle = open(FilePath, "r")
    ConfigFile = yaml.full_load(FileHandle)
    FileHandle.close()
    # Get config file contents

    for TipID in ConfigFile["Tip IDs"]:
        TipItem = ConfigFile["Tip IDs"][TipID]

        PickupSequence = TipItem["Pickup Sequence"]
        MaxVolume = TipItem["Max Pipetting Volume"]

        TipType = TipTypes(TipItem["Tip Type"])

        if TipType == TipTypes.NTR:
            NTRWasteSequence = MaxVolume = TipItem["NTR Waste Sequence"]

            TipTrackerInstance.ManualLoad(
                TipNTR(TipID, PickupSequence, NTRWasteSequence, MaxVolume)
            )

        elif TipType == TipTypes.FTR:
            TipTrackerInstance.ManualLoad(TipFTR(TipID, PickupSequence, MaxVolume))