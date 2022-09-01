# curl -X POST http://localhost:8080/Comm/GetCommand

from ..Tools.Parsing import ParseHTTPResponse

urls = ("/Comm/GetCommand", "ABN.Source.Server.Comm.GetCommand.GetCommand")

ExpectedJsonKeys = ("MethodID",)


class GetCommand:
    def GET(self):
        print()  # Readability
        print("GetCommand handling started!")

        # Do something here

        Response = ParseHTTPResponse(
            {"MethodID": 12345, "Out": "Test"}, ExpectedJsonKeys
        )

        if Response is None:
            print("Error detected so no processing will occur.")
            return None

        print()  # Readability
        return Response
