from ..Steps import Steps as STEPS
from ..Labware import Plates as PLATES
from ..Labware import Solutions as SOLUTIONS
from ...User import Samples as SAMPLES
from ...Hamilton.Commands import Pipette as PIPETTE
import copy

TITLE = "Liquid Transfer"
NAME = "Name"
TYPE = "Liquid Type"
STORAGE = "Storage Condition"
VOLUME = "Volume (uL)"
MIXING = "Mix?"


def Init():
	pass

def Step(step):
	DestinationPlate = step.GetParentPlate()

	SourceList = SAMPLES.Column(step.GetParameters()[NAME])
	SourceVolumeList = SAMPLES.Column(step.GetParameters()[VOLUME])
	
	for Source in SourceList:
		SOLUTIONS.AddSolution(Source, step.GetParameters()[TYPE], step.GetParameters()[STORAGE])

	Sequences = PLATES.GetPlate(DestinationPlate).CreatePipetteSequence(SourceList, SourceVolumeList)

	_Temp = copy.deepcopy(Sequences)
	for Sequence in _Temp:

		if(Sequence[2] == 0):
			Sequences.remove(Sequence)
			
		else:
			SOLUTIONS.GetSolution(Sequence[1]).AddVolume(Sequence[2])

	if len(Sequences) != 0:
		PIPETTE.Do(DestinationPlate, Sequences)



