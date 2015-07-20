# ODKArchForms
Open Data Kit forms and conversion scripts used in archaeology.  Including New Mexico LA Forms, photologs, etc.

A series of <a href="https://opendatakit.org/">Open Data Kit</a> XLSForms and Python scripts to convert from XML to Acrobat PDF format.

These digital forms are used for recording information on archaeological sites, including photo logs and forms specific to archaeology in New Mexico (LA Forms).

Process:
- 1) Field names and data types are defined in an XLS file which is converted for use by ODK with <a href="https://opendatakit.org/use/xlsform/">XLSForm</a>.
- 2) Field data is collected on tablets
- 3) Resulting XML file is converted by Python scripts (thanks to <a href="https://github.com/ccnmtl/fdfgen/">FDFGen</a> and <a href="https://github.com/stchris/untangle">Untangle</a>) to pre-defined PDF forms.

Usage: 
python "...ODK_to_PDF.py" "ODK_instance.xml"

Example: 
python LAForm_ODK_to_PDF.py LA_Site_Form_2015-05-28_13-45-49.xml

Dependencies:
 - Android tablet with the ODK app
 - Python 3+
 - <a href="https://www.pdflabs.com/tools/pdftk-server/">PDFtk Server</a>

 
