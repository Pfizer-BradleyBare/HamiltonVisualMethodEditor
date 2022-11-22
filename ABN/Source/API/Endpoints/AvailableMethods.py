import os

import web

from ...Server.Tools.Parser import Parser

MethodsPath = "C:\\___MethodsTest"
TemplateMethodSuffix = "__Template"
ArchiveFolder = "Archive"
TempFolder = "Temp"

urls = (
    "/Method/AvailableMethods",
    "ABN.Source.Server.Method.AvailableMethods.AvailableMethods",
)


class AvailableMethods:
    def GET(self):
        ParserObject = Parser("Method AvailableMethods", web.data())

        if not ParserObject.IsValid([]):
            Response = ParserObject.GetHTTPResponse()
            return Response

        MethodProjects = dict()

        if os.path.exists(MethodsPath):
            Methods = [
                Item
                for Item in os.listdir(MethodsPath)
                if os.path.isdir(os.path.join(MethodsPath, Item))
            ]
        else:
            Methods = list()

        for Method in Methods:
            MethodProjects[Method] = [
                Dir
                for Dir in os.listdir(os.path.join(MethodsPath, Method))
                if Dir != ArchiveFolder
                and Dir != TempFolder
                and os.path.isdir(os.path.join(MethodsPath, Method, Dir))
                and any(
                    TemplateMethodSuffix + "_" + Method + "_" + Dir + ".xlsm" in item
                    for item in os.listdir(os.path.join(MethodsPath, Method, Dir))
                )
            ]

        for Method in MethodProjects:
            if len(MethodProjects[Method]) == 0:
                Methods.remove(Method)

        ParserObject.SetAPIState(True)
        ParserObject.SetAPIReturn("Methods", Methods)
        ParserObject.SetAPIReturn("Method Projects", MethodProjects)
        ParserObject.SetAPIReturn("Message", "Possible methods returned as dict")

        Response = ParserObject.GetHTTPResponse()
        return Response