import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.UI import *
from pyrevit import script
from pyrevit import forms

output = script.get_output()
doc = __revit__.ActiveUIDocument.Document
uidoc = __revit__.ActiveUIDocument

# Function to safely retrieve parameter values
def get_parameter_value(element, built_in_param):
    param = element.get_Parameter(built_in_param)
    if param is not None and param.HasValue:
        return str(param.AsString())
    return "N/A"

# Options for user to select output columns
ops = ['ID',
       'Sheet Name',
       'Sheet Number',
       'View Name',
       'Revision Name',
       'Revision Number',
       'Mark',
       'Comments']
print(','.join(ops))
# Show form to select columns for output
res = forms.SelectFromList.show(ops,
                                title='Output Column Selection',
                                multiselect=True,
                                button_name='Select Columns for output')

if res:        
    collector = FilteredElementCollector(doc)
    sheets = collector.OfCategory(BuiltInCategory.OST_Sheets).ToElements()
    sheet_list = []

    for sheet in sheets:
        sheet_list.append(sheet.get_Parameter(BuiltInParameter.SHEET_NUMBER).AsString())
        viewports = sheet.GetAllViewports()
        if viewports:
            for vp_id in viewports:
                viewport = doc.GetElement(vp_id)
                view = doc.GetElement(viewport.ViewId)
                collector = FilteredElementCollector(doc, view.Id)
                rev_cloud = collector.OfClass(RevisionCloud).ToElements()
                rev_clouds_on_sheet = FilteredElementCollector(doc, sheet.Id).OfClass(RevisionCloud).ToElements()
                if rev_clouds_on_sheet:
                    for revision in rev_clouds_on_sheet:
                        output_strings = []
                        if 'ID' in res:
                            output_strings.append(str(revision.Id))
                        if 'Sheet Name' in res:
                            output_strings.append(sheet.Name.replace(',', ''))
                        if 'Sheet Number' in res:
                            output_strings.append(get_parameter_value(sheet, BuiltInParameter.SHEET_NUMBER))
                        if 'View Name' in res:
                            output_strings.append("N/A")  # No view for sheet-based revision clouds
                        if 'Revision Name' in res:
                            revision_id = revision.RevisionId  # Single associated revision
                            if revision_id.IntegerValue != -1:  # Check that there is an associated revision
                                associated_revision = doc.GetElement(revision_id)
                                revision_name = associated_revision.Name
                            else:
                                revision_name = "N/A - - On Sheet"
                            output_strings.append(revision_name.replace(',', ''))
                        if 'Revision Number' in res:
                            output_strings.append(get_parameter_value(revision, BuiltInParameter.REVISION_CLOUD_REVISION_NUM))
                        if 'Mark' in res:
                            output_strings.append(get_parameter_value(revision, BuiltInParameter.ALL_MODEL_MARK).replace(',', ''))
                        if 'Comments' in res:
                            output_strings.append(get_parameter_value(revision, BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS).replace(',', ''))
                        print(','.join(output_strings))
                if rev_cloud:
                    for revision in rev_cloud:
                        output_strings = []
                        if 'ID' in res:
                            output_strings.append(str(revision.Id))
                        if 'Sheet Name' in res:
                            output_strings.append(doc.GetElement(sheet.Id).Name.replace(',',''))
                        if 'Sheet Number' in res:
                            output_strings.append(get_parameter_value(sheet, BuiltInParameter.SHEET_NUMBER))
                        if 'View Name' in res:
                            output_strings.append(view.Name.replace(',',''))
                        if 'Revision Name' in res:
                            output_strings.append(revision.Name.replace(',',''))
                        if 'Revision Number' in res:
                            output_strings.append(get_parameter_value(revision, BuiltInParameter.REVISION_CLOUD_REVISION_NUM))
                        if 'Mark' in res:
                            output_strings.append(get_parameter_value(revision, BuiltInParameter.ALL_MODEL_MARK).replace(',',''))
                        if 'Comments' in res:
                            output_strings.append(get_parameter_value(revision, BuiltInParameter.ALL_MODEL_INSTANCE_COMMENTS).replace(',',''))
                        # Print the selected columns, joined by a comma
                        print(','.join(output_strings))
                else:
                    continue
        else:
            continue
else:
    print('No columns selected. TRY AGAIN')
