import web
from ..Tools.Parser import Parser
import xlwings

urls = (
    "/Method/Open",
    "ABN.Source.Server.Method.Open.Open",
)


class Open:
    def POST(self):
        ParserObject = Parser("Method Open", web.data())

        if not ParserObject.IsValid(["Method File Path"]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        MethodFilePath = ParserObject.GetAPIData()["Method File Path"]

        BookHandle: xlwings.Book | None = None
        if xlwings.apps.count != 0:
            for Book in xlwings.books:
                if Book.fullname == MethodFilePath:
                    BookHandle = Book

        if BookHandle is None:
            BookHandle = xlwings.Book(MethodFilePath)

        ParserObject.SetAPIState(True)
        ParserObject.SetAPIReturn("Message", "Excel Workbook Opened")

        Response = ParserObject.GetHTTPResponse()
        return Response
