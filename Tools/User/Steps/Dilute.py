from ..Steps import Steps as STEPS
from ..Labware import Plates as PLATES
from ..Labware import Solutions as SOLUTIONS
from ...User import Samples as SAMPLES
from ...Hamilton.Commands import Pipette as PIPETTE
from ...User import Configuration as CONFIGURATION
from ...General import HamiltonIO as HAMILTONIO
import copy

TITLE = "Dilute"
SOURCE = "Source"
DILUENT = "Diluent"
STARTING_CONCENTRATION = "Starting Concentration (mg/mL)"
TARGET_CONCENTRATION = "Target Concentration (mg/mL)"
TARGET_VOLUME = "Target Volume (uL)"

######################################################################### 
#	Description: No itialization required here. Provided for consistency
#	Input Arguments: N/A
#	Returns: N/A
#########################################################################
def Init():
	pass

######################################################################### 
#	Description: Performs a dilution step by doing the following:
#	1. Forms a pipette hamilton command for the diluent solution
#	2. Forms a pipette hamilton command for the source solution
#	Input Arguments: [step: Step class]
#	Returns: N/A
#########################################################################
def Step(step):
	#dilute equation is C1*V1 = C2*V2 Where:
	#C1 is SourceConcentration
	#V1 is Source Volume
	#C2 is Target Concentration
	#V2 is Target Volume
	#We need to solve for Source Volume
	#V1 = (C2*V2)/C1

	DestinationPlate = step.GetParentPlate()

	TargetConcentrationList = SAMPLES.Column(step.GetParameters()[TARGET_CONCENTRATION])
	TargetVolumeList = SAMPLES.Column(step.GetParameters()[TARGET_VOLUME])

	SourceList = SAMPLES.Column(step.GetParameters()[SOURCE])
	DiluentList = SAMPLES.Column(step.GetParameters()[DILUENT])
	SourceConcentrationList = SAMPLES.Column(step.GetParameters()[STARTING_CONCENTRATION])

	for Source in SourceList:
		SOLUTIONS.AddSolution(Source, SOLUTIONS.TYPE_REAGENT, SOLUTIONS.STORAGE_AMBIENT)

	for Diluent in DiluentList:
		SOLUTIONS.AddSolution(Diluent, SOLUTIONS.TYPE_BUFFER, SOLUTIONS.STORAGE_AMBIENT)

	SourceVolumeList = list(map(lambda x,y,z: (z * y) / x if x != None and x != 0 else 0, SourceConcentrationList,TargetVolumeList,TargetConcentrationList))
	DiluentVolumeList = list(map(lambda x,y: y - x, SourceVolumeList,TargetVolumeList))

	Sequences = PLATES.GetPlate(DestinationPlate).CreatePipetteSequence(SourceList, SourceVolumeList)
	#print(Sequences)

	_Temp = copy.deepcopy(Sequences)
	for Sequence in _Temp:

		if(Sequence[2] == 0):
			Sequences.remove(Sequence)
			
		else:
			SOLUTIONS.GetSolution(Sequence[1]).AddVolume(Sequence[2])

	if len(Sequences) != 0:
		PIPETTE.Do(DestinationPlate, Sequences)

	Sequences = PLATES.GetPlate(DestinationPlate).CreatePipetteSequence(DiluentList, DiluentVolumeList)
	#print(Sequences)

	_Temp = copy.deepcopy(Sequences)
	for Sequence in _Temp:

		if(Sequence[2] == 0):
			Sequences.remove(Sequence)
			
		else:
			SOLUTIONS.GetSolution(Sequence[1]).AddVolume(Sequence[2])
	if HAMILTONIO.IsSimulated() == False:
		for sequence in Sequences:
			name = sequence[1]
			SequencePos = CONFIGURATION.GetDeckLoading(name)["Sequence"]
			sequence[1] = SequencePos
		DestinationPlate = CONFIGURATION.GetDeckLoading(DestinationPlate)["Sequence"]

	if len(Sequences) != 0:
		PIPETTE.Do(DestinationPlate, Sequences)
#end


