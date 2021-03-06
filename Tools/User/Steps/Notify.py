from ..Steps import Steps as STEPS
from ...Hamilton.Commands import Notify as NOTIFY
from ...General import Log as LOG
from ...General import HamiltonIO as HAMILTONIO
from ...Hamilton.Commands import StatusUpdate as STATUS_UPDATE

TITLE = "Notify"
WAIT_ON_USER = "Wait On User"
SUBJECT = "Subject"
MESSAGE = "Message"

IsUsedFlag = True

def IsUsed():
	return IsUsedFlag

def DoesStatusUpdates():
	return True

def Init():
	pass

def Step(step):
	
	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Starting Notify Block. Block Coordinates: " + str(step.GetCoordinates())}),False,True)
	HAMILTONIO.SendCommands()

	Parameters = step.GetParameters()
	Subject = Parameters[SUBJECT]
	Body = Parameters[MESSAGE]
	Wait = Parameters[WAIT_ON_USER]

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################
	MethodComments = []
	
	#Testing subject and body?
	if not (type(Subject) is str):
		MethodComments.append("The Subject parameter must contain letters. Please Correct.")

	if not (type(Body) is str):
		MethodComments.append("The Body parameter must contain letters. Please Correct.")

	if len(MethodComments) != 0:
		LOG.LogMethodComment(step,MethodComments)
		if HAMILTONIO.IsSimulated() == True:
			quit()
		else:
			STEPS.UpdateStepParams(step)
			Step(step)
			return

	#########################
	#########################
	#########################
	#### INPUT VALIDATION ###
	#########################
	#########################
	#########################

	if Wait == "Yes":
		NotifyString = " and waiting for user to proceed"
	else:
		NotifyString = ""

	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Sending notification to the provided contact info" + NotifyString}),False,True)
	HAMILTONIO.AddCommand(NOTIFY.NotifyContacts({"Subject":Subject,"Body":Body,"Wait":Wait}))
	HAMILTONIO.SendCommands()
	#No need to deal with response. Should always succeed

	HAMILTONIO.AddCommand(STATUS_UPDATE.AddProgressDetail({"DetailMessage": "Starting Notify Block. Block Coordinates: " + str(step.GetCoordinates())}),False,True)
	HAMILTONIO.SendCommands()