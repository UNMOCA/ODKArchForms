#!python

import untangle, sys, os
from fdfgen import forge_fdf
from subprocess import call

fields = []

#parse XML
resource = sys.argv[1]

#remove confusing group tag before handing to parser
with open(resource, 'r') as infile:
	modResource = infile.read().replace("</PHOTOGROUP>", "").replace("<PHOTOGROUP>", "")

obj = untangle.parse(modResource)

lanum = str(obj.OCA_Photo_Log.LANUM.cdata)

#TODO convert Blade's crazy notation to polar headings
index = 0
for item in obj.OCA_Photo_Log.children:
	if 'photoRepeat' in item._name:
		for item in item.children:
			LAField = 'site' + str(index)
			fields.append((LAField, lanum))
			if 'photo' in item._name:
				newFieldName = 'exp' + str(index)
				fields.append((newFieldName, item.cdata))
			elif 'description' in item._name:
				newFieldName = 'photo' + str(index)
				fields.append((newFieldName, item.cdata))
			elif 'date' in item._name:
				newFieldName = 'date' + str(index)
				fields.append((newFieldName, item.cdata))
			elif 'orientation' in item._name:
				newFieldName = 'view' + str(index)
				fields.append((newFieldName, item.cdata))
			elif 'recorder' in item._name:
				newFieldName = 'rec' + str(index)
				fields.append((newFieldName, item.cdata))
		index += 1
	else:
		fields.append((item._name, item.cdata))


if index <= 33:
	totalPage = 1
	fields.append(('totalPage', totalPage))
elif index >= 34 and index <= 67:
	totalPage = 2
	fields.append(('totalPage', totalPage))
elif index >= 68 and index <= 101:
	totalPage = 3
	fields.append(('totalPage', totalPage))
elif index >= 102 and index <= 135:
	totalPage = 4
	fields.append(('totalPage', totalPage))
elif index >= 136 and index <= 169: 
	totalPage = 5
	fields.append(('totalPage', totalPage))
else:
	print("This is too long...need to build more pages!!")

#write FDF file
fdf = forge_fdf("",fields,[],[],[])
filename = lanum + "_photolog.fdf"
fdf_file = open(filename, "wb")
fdf_file.write(fdf)
fdf_file.close()

#fdf to pdf using pdftk
print ("Creating OCA Photolog PDF for LA" + lanum + "...")
pdfFileName = lanum + "_photologTemp.pdf"
writePDF = "pdftk Blank_OCAPhotoLog.pdf fill_form " + filename + " output " + pdfFileName
call(writePDF)

#remove excess pages
print ("Removing excess pages...")
trimPDF = "pdftk " + pdfFileName + " cat 1-" + str(totalPage) + " output " + lanum + "_photolog.pdf"
call(trimPDF)

#remove temp files
print ("Removing temp files...")
os.remove(filename)
os.remove(pdfFileName)
print ("Done!")
