from ...Workbook.Block import Block, ClassDecorator_AvailableBlock
from ....Tools import Excel
from ...Workbook import Workbook
from ....HAL import Hal
from ...Tools.Container import Container
from ...Tools.Context import Context


@ClassDecorator_AvailableBlock
class Plate(Block):
    def __init__(self, ExcelInstance: Excel, Row: int, Col: int):
        Block.__init__(self, ExcelInstance, Row, Col)

    def GetName(self) -> str:
        return "Plate" + str((self.Row, self.Col))

    def GetPlateName(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 2, self.Col + 2, self.Row + 2, self.Col + 2
        )

    def GetPlateType(self) -> str:
        return self.ExcelInstance.ReadMethodSheetArea(
            self.Row + 3, self.Col + 2, self.Row + 3, self.Col + 2
        )

    def Preprocess(self, WorkbookInstance: Workbook, HalInstance: Hal):
        pass

    def Process(self, WorkbookInstance: Workbook, HalInstance: Hal):
        PlateName = self.GetPlateName()
        PlateFilter = self.GetPlateType()

        # Do parameter validation here

        ContextTrackerInstance = WorkbookInstance.GetContextTracker()
        InactiveContextTrackerInstance = WorkbookInstance.GetInactiveContextTracker()

        OldContextInstance = WorkbookInstance.GetExecutingContext()
        NewContextInstance = Context(
            OldContextInstance.GetName() + ":" + PlateName,
            OldContextInstance.GetAspirateWellSequencesTracker(),
            OldContextInstance.GetDispenseWellSequencesTracker,
            OldContextInstance.GetWellFactorTracker(),
        )
        InactiveContextTrackerInstance.ManualLoad(OldContextInstance)
        ContextTrackerInstance.ManualLoad(NewContextInstance)
        WorkbookInstance.SetExecutingContext(NewContextInstance)
        # Deactivate the previous context and active this new context

        ContainerTracker = WorkbookInstance.GetContainerTracker()

        PlateContainerInstance = Container(PlateName, PlateFilter)
        if ContainerTracker.IsTracked(PlateContainerInstance) is False:
            ContainerTracker.ManualLoad(PlateContainerInstance)
        # Create the container if it does not already exists
