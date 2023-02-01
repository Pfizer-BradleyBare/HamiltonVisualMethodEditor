from ....Server.Globals import LOG
from ...Blocks import MergePlates
from ...Workbook import Block, Workbook


def RunProcessor(WorkbookInstance: Workbook):

    WorkbookInstance.ExcelInstance.OpenBook(False)

    ContextTrackerInstance = WorkbookInstance.GetContextTracker()
    InactiveContextTrackerInstance = WorkbookInstance.GetInactiveContextTracker()
    ExecutedBlocksTrackerInstance = WorkbookInstance.GetExecutedBlocksTracker()
    PreprocessingBlocksTrackerInstance = (
        WorkbookInstance.GetPreprocessingBlocksTracker()
    )
    CompletedPreprocessingBlocksTrackerInstance = (
        WorkbookInstance.CompletedPreprocessingBlocksTrackerInstance
    )

    CurrentExecutingBlock: Block = WorkbookInstance.GetMethodTreeRoot()
    CurrentExecutingBlock.Process(WorkbookInstance)
    ExecutedBlocksTrackerInstance.ManualLoad(CurrentExecutingBlock)
    # Do the first step processing here. First step is always a plate step.

    while True:

        while True:
            WorkbookInstance.ProcessingLock.acquire()
            WorkbookInstance.ProcessingLock.release()
            # if AliveStateFlag.AliveStateFlag is False: TODO
            # Do some workbook save state stuff here
            #    return

            # if all(
            #    LoadedLabwareConnection.IsConnected()
            #    for LoadedLabwareConnection in WorkbookInstance.GetLoadedLabwareConnectionTracker().GetObjectsAsList()
            # ):
            break
            # if all are connected then we can start running. Boom!
        # This first thing we need to do is check that all labwares are loaded. If not then we sit here and wait.
        # This could be expanded to wait until a set of labware is loaded before proceeding. How? No idea.

        if all(
            item in ExecutedBlocksTrackerInstance.GetObjectsAsList()
            for item in WorkbookInstance.GetMethodBlocksTracker().GetObjectsAsList()
        ):

            print("HERE")
            return
            WorkbookInstance.LabwareSelectionTrackerInstance = (
                LabwareSelectionLoader.Load(
                    WorkbookInstance.GetContainerTracker(),
                )
            )

            for (
                LabwareSelectionInstance
            ) in WorkbookInstance.LabwareSelectionTrackerInstance.GetObjectsAsList():
                print(
                    LabwareSelectionInstance.GetName(),
                    LabwareSelectionInstance.GetContainer().GetVolume(),
                    str(
                        [
                            lab.GetName()
                            for lab in LabwareSelectionInstance.GetLabwareTracker().GetObjectsAsList()
                        ]
                    ),
                )

            if WorkbookInstance.GetRunType() == WorkbookRunTypes.PreRun:

                WorkbookInstance.SetRunType(WorkbookRunTypes.Run)

                WorkbookInstance.ProcessingLock.acquire()
                WorkbookInstance.ProcessingLock.release()
                # if AliveStateFlag.AliveStateFlag is False: TODO
                # Do some workbook save state stuff here
                #    return
                # Everything is controlled by the server. So we will wait here for the server to tell us we are next to run
                # Then we will reinit the workbook and wait on deck loading

                WorkbookInit(WorkbookInstance)
            # If we are prerun then we need to do this another time to actually run the method
            # else we are done here and can return

            return
        # First thing to do is check if all blocks have been executed.

        WorkbookInstance.ProcessingLock.acquire()
        WorkbookInstance.ProcessingLock.release()
        # if AliveStateFlag.AliveStateFlag is False: TODO
        # Do some workbook save state stuff here
        #    return
        # The processing lock is used as a pause button to control which workbook executes.
        # During acquire we wait for the thread to be unpaused.
        # We immediately release so we do not stall the main process
        # After release we must check that the server still wants to execute. If not, we do some save state stuff then kill the thread.

        ConfirmedPreprocessingBlockInstances: list[Block] = list()
        for (
            PreprocessingBlockInstance
        ) in PreprocessingBlocksTrackerInstance.GetObjectsAsList():

            SearchBlockInstance = PreprocessingBlockInstance

            if CompletedPreprocessingBlocksTrackerInstance.IsTracked(
                SearchBlockInstance.GetName()
            ):
                continue
            # This block has already been preprocessed. Do not do it twice

            if not ContextTrackerInstance.IsTracked(SearchBlockInstance.GetContext()):
                continue
            # If the block context is not yet available then we are not going to try to start preprocessing.
            # I want this to change in the future but it is good enough for now

            while True:
                SearchBlockInstance = SearchBlockInstance.GetParentNode()

                if SearchBlockInstance is None:
                    ConfirmedPreprocessingBlockInstances.append(
                        PreprocessingBlockInstance
                    )
                    break
                # We found the root. This means that this preprocessing block is ready to start

                if ExecutedBlocksTrackerInstance.IsTracked(
                    SearchBlockInstance.GetName()
                ):
                    continue
                # If the block has already been executed then we can skip it.

                if PreprocessingBlocksTrackerInstance.IsTracked(
                    SearchBlockInstance.GetName()
                ):
                    break
                # There is a preceeding block that needs to be preprocessed. So we will skip this block for now
                # NOTE NOTE NOTE NOTE TODO There is a question if we need to only pay attention to blocks of same type or not. I say not for now

                if type(SearchBlockInstance).__name__ == MergePlates.__name__:
                    break
                # We can not start a preprocessing device if an unexecuted merge plates step preceeds it.
            # We are going to walk backward until we find either a merge plates step, a preceeding preprocessing device, or the beginning of the method

        for ConfirmedPreprocessingBlockInstance in ConfirmedPreprocessingBlockInstances:
            StepPreprocessStatus = ConfirmedPreprocessingBlockInstance.Preprocess(
                WorkbookInstance
            )

            if StepPreprocessStatus is True:
                CompletedPreprocessingBlocksTrackerInstance.ManualLoad(
                    ConfirmedPreprocessingBlockInstance
                )
        # Before each round of steps we want to check if we can start heaters / Coolers or other preprocessing devices
        # We can not start a preprocessing device until any preceeding merge steps are completed

        if InactiveContextTrackerInstance.IsTracked(
            WorkbookInstance.GetExecutingContext().GetName()
        ):
            if all(
                item in InactiveContextTrackerInstance.GetObjectsAsList()
                for item in ContextTrackerInstance.GetObjectsAsList()
            ):
                ...
            # If all contexts are inactive then we need to wait on devices to complete. TODO

            for ContextInstance in ContextTrackerInstance.GetObjectsAsList():
                if not InactiveContextTrackerInstance.IsTracked(
                    ContextInstance.GetName()
                ):
                    WorkbookInstance.SetExecutingContext(ContextInstance)
                    break
            # find the context here

            ReversedExecutedBlocks: list[
                Block
            ] = ExecutedBlocksTrackerInstance.GetObjectsAsList()
            ReversedExecutedBlocks.reverse()

            for BlockInstance in ReversedExecutedBlocks:
                if BlockInstance.GetContext() == WorkbookInstance.GetExecutingContext():
                    CurrentExecutingBlock: Block = BlockInstance
                    break
            # Set the tree current node here
        # Find the context we need to process if the current context is exhausted

        CurrentExecutingBlock = CurrentExecutingBlock.GetChildren()[0]

        StepStatus = True
        if (
            sum(
                WellFactor.GetFactor()
                for WellFactor in WorkbookInstance.GetExecutingContext()
                .GetWellFactorTracker()
                .GetObjectsAsList()
            )
            != 0  # If all the factors are zero then technically the pathway is "dead" so it will never execute
            or type(CurrentExecutingBlock).__name__ == MergePlates.__name__
        ):
            # We will only execute the step if the factors are not zero
            # Additionally we must always execute a merge plates step no matter what

            LOG.info("EXECUTING: " + CurrentExecutingBlock.GetName())
            StepStatus = CurrentExecutingBlock.Process(WorkbookInstance)

        else:
            LOG.info("SKIPPING: " + CurrentExecutingBlock.GetName())

        if StepStatus is True:
            ExecutedBlocksTrackerInstance.ManualLoad(CurrentExecutingBlock)

            # need to fix with new stepstatus TODO
            # This should always be a single child. Only a split plate wil have 2 children
            # The two children will be executed in the split plate block
            # We must track all executed blocks even if processing is skipped.

        # NOTE: A skipped block is still executed in the mind of the program

        else:
            CurrentExecutingBlock = CurrentExecutingBlock.GetParentNode()  # type:ignore