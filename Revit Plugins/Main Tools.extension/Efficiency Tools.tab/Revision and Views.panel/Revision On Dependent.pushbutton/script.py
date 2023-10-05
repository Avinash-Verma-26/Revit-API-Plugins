import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from pyrevit import script

output = script.get_output()
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

output.indeterminate_progress(True)
views = FilteredElementCollector(doc).OfClass(View).WhereElementIsNotElementType().ToElements()
dependent_views = []

#Find all Dependent Views
for view in views:    
    dep_view = View.GetDependentViewIds(view)
    if dep_view:
        for dep in dep_view:
            dependent_views.append(dep)
if dependent_views:
    #Get all sheet wise views information and create a dictionary with key=view name and value=sheet number
    sheet_View_pair = {}
    collector = FilteredElementCollector(doc)
    sheets = collector.OfCategory(BuiltInCategory.OST_Sheets).ToElements()
    for sheet in sheets:
        viewport = sheet.GetAllViewports()
        for vp_id in viewport:
            viewport = doc.GetElement(vp_id)
            view = doc.GetElement(viewport.ViewId)
            sheet_View_pair[view.Name] = sheet.get_Parameter(BuiltInParameter.SHEET_NUMBER).AsString()

    #Finding Revision Clouds in each Dependent View
    for dep in dependent_views:
        collector = FilteredElementCollector(doc, dep)
        rev_clouds = collector.OfClass(RevisionCloud).ToElements()
        view_element = doc.GetElement(dep)
        view_name = doc.GetElement(dep).Name
        if rev_clouds:
            print(view_name)
            for rev in rev_clouds:
                if view_name in sheet_View_pair:
                    print(str(rev.Id)+" ---- "+str(rev.Name)+" ---- "+sheet_View_pair[doc.GetElement(dep).Name])
                else:
                    print(str(rev.Id) + " ---- " + str(rev.Name) + " ---- " + "View not on any sheet")
else:
    print("No Dependent Views")
output.indeterminate_progress(False)