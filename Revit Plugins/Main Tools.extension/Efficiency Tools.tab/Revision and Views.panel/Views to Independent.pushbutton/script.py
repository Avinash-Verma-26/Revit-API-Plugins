import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *

doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

el = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Views).WhereElementIsNotElementType().ToElements()

t = Transaction(doc,'To Independent')
t.Start()
for one in el:
    dependency_param = one.LookupParameter('Dependency')
    if 'Dependent on' in dependency_param.AsString():
        one.ConvertToIndependent()
    else:
        continue
t.Commit()
    # dependency = one.LookUpParameter('Dependency')
    # print(dependency)


# OST_Views