# curl -X GET http://localhost:65535/Command/Request

import web

from ....Server.Globals.HandlerRegistry import HandlerRegistry
from ....Server.Tools.Parser import Parser

urls = ("/Driver/IsReady", "ABN.Source.Driver.Handler.Endpoints.IsReady.IsReady")


class IsReady:
    def GET(self):
        ParserObject = Parser("Driver IsReady", web.data())

        if not ParserObject.IsValid([]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        CommandTrackerInstance = HandlerRegistry.GetObjectByName(
            "Driver Handler"
        ).CommandTrackerInstance  # type:ignore

        CommandReady = False
        if CommandTrackerInstance.GetNumObjects() != 0:
            if CommandTrackerInstance.GetObjectsAsList()[0].ResponseInstance is None:
                CommandReady = True

        ParserObject.SetAPIState(True)
        ParserObject.SetAPIReturn("Message", "Returned Command IsReady status")
        ParserObject.SetAPIReturn("IsReady", CommandReady)
        Response = ParserObject.GetHTTPResponse()
        return Response
