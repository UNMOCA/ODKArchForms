#!python

import untangle, sys, os
from fdfgen import forge_fdf
from subprocess import call

fields = []

#parse XML
resource = sys.argv[1]
obj = untangle.parse(resource)

#TODO
#totalComponents = sum of all components
#assemblageOther = yes if assembleOtherSpecify != ''

def parseMonth(code):
	if code == '01':
		return 'JAN'
	elif code == '02':
		return 'FEB'
	elif code == '03':
		return 'MAR'
	elif code == '04':
		return 'APR'
	elif code == '05':
		return 'MAY'
	elif code == '06':
		return 'JUN'
	elif code == '07':
		return 'JUL'
	elif code == '08':
		return 'AUG'
	elif code == '09':
		return 'SEP'
	elif code == '10':
		return 'OCT'
	elif code == '11':
		return 'NOV'
	else:
		return 'DEC'

def parseFeatureType(ftype):
	if ftype == 'featureBinCist':
		return 'Bin/Cist'
	elif ftype == 'featureCavate':
		return 'Cavate Room'
	elif ftype == 'featureDepression':
		return 'Depression'
	elif ftype == 'featureDump':
		return 'Dump'
	elif ftype == 'featureFCR':
		return 'Fire-Cracked Rock Concentration'
	elif ftype == 'featureHearth':
		return 'Hearth'
	elif ftype == 'featureIsolatedRoom':
		return 'Isolated room'
	elif ftype == 'featureKiva':
		return 'Kiva'
	elif ftype == 'featureMidden':
		return 'Midden'
	elif ftype == 'featureMound':
		return 'Mound'
	elif ftype == 'featurePithouse':
		return 'Pithouse'
	elif ftype == 'featureRockAlign':
		return 'Rock Alignment'
	elif ftype == 'featureRoomblock':
		return 'Roomblock'
	elif ftype == 'featureSoilStain':
		return 'Soil Stain, Unspecified'
	elif ftype == 'featureStoneCircle':
		return 'Stone Circle'
	elif ftype == 'featureStructureUnd':
		return 'Structure, Undefined'
	else:
		return 'Other'

def parsePeriod(period):
	if period == 'periodPreClovis':
		return 'Pre-Clovis (> BC9500)'
	elif period == 'periodClovis':
		return 'Clovis (BC 9500-9000)'
	elif period == 'periodFolsom':
		return 'Folsom/Midland (BC 9000-8000)'
	elif period == 'periodLatePaleo':
		return 'Late Paleo-Indian (BC 8000-6600)'
	elif period == 'periodTerminalPaleo':
		return 'Terminal Paleo-Indian (BC 6600-5500)'
	elif period == 'periodUnspecifPaleo':
		return 'Unspecified Paleo-Indian (BC 9500-5500)'
	elif period == 'periodEarlyArchaic':
		return 'Early Archaic (BC 5500-3000)'
	elif period == 'periodMiddleArchaic':
		return 'Middle Archaic (BC 3000-1800)'
	elif period == 'periodLateArchaic':
		return 'Late Archaic (1800BC -AD200)'
	elif period == 'periodUnspecifArchaic':
		return 'Unspecified Archaic (5500BC - AD200)'
	elif period == 'periodBM2':
		return 'Basketmaker I (AD 1-500)'
	elif period == 'periodBM3':
		return 'Basketmaker II (AD 500-700)'
	elif period == 'periodP1':
		return 'Pueblo I (AD 700-900)'
	elif period == 'periodP2':
		return 'Pueblo II (AD 900-1100)'
	elif period == 'periodP3':
		return 'Pueblo III (AD 1100-1300)'
	elif period == 'periodP4':
		return 'Pueblo IV (AD 1300-1600)'
	elif period == 'periodUnspecifPecos':
		return 'Unspecified Anasazi (Pecos) (AD 1-1600)'
	elif period == 'periodDevelopmental':
		return 'Developmental (AD 600-1200)'
	elif period == 'periodCoalition':
		return 'Coalition (AD 1200-1325)'
	elif period == 'periodClassic':
		return 'Classic (AD 1325-1600)'
	elif period == 'periodUnspecifAnasazi':
		return 'Unspecified Anasazi (N. Rio Grande)'
	elif period == 'periodUnspecifHistoric':
		return 'Unspecified Historic (AD 1539-present)'
	elif period == 'periodSpanish':
		return 'Spanish Contact/Colonial (AD 1539-1680)'
	elif period == 'periodRevolt':
		return 'Pueblo Revolt (AD 1680-1692)'
	elif period == 'periodPostRevolt':
		return 'Post Pueblo Revolt (AD 1692-1821)'
	elif period == 'periodMexican':
		return 'Mexican/Santa Fe Trail (AD 1821-1846)'
	elif period == 'periodTerritorial':
		return 'US Territorial (AD 1846-1912)'
	elif period == 'periodStatehood':
		return 'Statehood - WWII (AD 1912-1945)'
	elif period == 'periodRecent':
		return 'Recent (AD 1945-present)'
	elif period == 'periodUnspecifHispanic':
		return 'Unspecified Hispanic, Pueblo, etc. (AD 1539-present)'
	elif period == 'periodUnknownPrehistoric':
		return 'Unspecific Prehistoric (< AD 1550)'
	elif period == 'periodUnknownHistoric':
		return 'Unspecific Historic (AD 1550-present)'
	elif period == 'periodPrehistoricAboriginal':
		return 'Unknown Prehistoric (Aboriginal)'
	elif period == 'periodHistoricAboriginal':
		return 'Unknown Historic (Aboriginal)'
	elif period == 'periodUnknown':
		return 'Unknown'
	elif period == 'periodNavajoPreRevolt':
		return 'Navajo Pre Pueblo Revolt (<1692)'
	elif period == 'periodNavajoPostRevolt':
		return 'Navajo Pueblo Revolt (AD 1692-1753)'
	elif period == 'periodNavajoPreRes':
		return 'Pre-Reservation (AD 1753-1868)'
	elif period == 'periodNavajoEarlyRes':
		return 'Early Reservation, to arrival of RR (AD 1868-1880)'
	elif period == 'periodNavajoMiddleRes':
		return 'Middle Reservation, to WWI (AD 1880-1920)'
	elif period == 'periodNavajoLateRes':
		return 'Late Reservation, to WWII (AD 1920-1945)'
	elif period == 'periodNavajoRecent':
		return 'Recent (AD 1945-present)'
	elif period == 'periodNavajoUnspecif':
		return 'Unspecified Navajo (AD 1500-present)'
	else:
		return 'Other'


index = 0
for item in obj.LA_Site_Form.IDOWN.children:
	if 'repeatOtherNum' in item._name:
		index += 1
		for item in item.children:
			newItemName = item._name + str(index)
			fields.append((newItemName, item.cdata))
	index = 0
	if 'repeatOwner' in item._name:
		index += 1
		for item in item.children:
			newItemName = item._name + str(index)
			fields.append((newItemName, item.cdata))
	else:
		fields.append((item._name, item.cdata))

for item in obj.LA_Site_Form.SITEOCCUPATIONTYPE.children:
	fields.append((item._name, item.cdata))

for item in obj.LA_Site_Form.RECORDINFO1.children:
	if 'recordingDate' in item._name:
		multiDate = item.cdata.split("-")
		recordDay = multiDate[2]
		recordMonth = parseMonth(multiDate[1])
		recordYear = multiDate[0]
		fields.append(('recordDay', recordDay))
		fields.append(('recordMonth', recordMonth))
		fields.append(('recordYear', recordYear))
	else:
		fields.append((item._name, item.cdata))

for item in obj.LA_Site_Form.RECORDINFO2.children:
	fields.append((item._name, item.cdata))

for item in obj.LA_Site_Form.RECORDINFO3.children:
	if 'recordActivities' in item._name:
		multipleItems = item.cdata.split()
		for items in multipleItems:
			fields.append((items, 'yes'))
	else:
		fields.append((item._name, item.cdata))

for item in obj.LA_Site_Form.RECORDINFO4.children:
	if 'recordsInventory' in item._name:
		multipleItems = item.cdata.split()
		for items in multipleItems:
			fields.append((items, 'yes'))
	else:
		fields.append((item._name, item.cdata))

for item in obj.LA_Site_Form.CONDITION.children:
	if 'archaeologicalStatus' in item._name:
		multipleItems = item.cdata.split()
		for items in multipleItems:
			fields.append((items, 'yes'))
	elif 'disturbanceSources' in item._name:
		multipleItems = item.cdata.split()
		for items in multipleItems:
			fields.append((items, 'yes'))
	elif 'vandalismSources' in item._name:
		multipleItems = item.cdata.split()
		for items in multipleItems:
			fields.append((items, 'yes'))
	else:
		fields.append((item._name, item.cdata))

for item in obj.LA_Site_Form.RECOMMENDATION.children:
	if 'NRCriteria' in item._name:
		multipleItems = item.cdata.split()
		for items in multipleItems:
			fields.append((items, 'yes'))
	else:
		fields.append((item._name, item.cdata))

for item in obj.LA_Site_Form.LOCATION.children:
	if 'sourceGraphics' in item._name:
		multipleItems = item.cdata.split()
		for items in multipleItems:
			fields.append((items, 'yes'))
	else:
		fields.append((item._name, item.cdata))

for item in obj.LA_Site_Form.PHYSICALDESCRIPTION1.children:
	if 'siteBoundsBasis' in item._name:
		multipleItems = item.cdata.split()
		for items in multipleItems:
			fields.append((items, 'yes'))
	elif 'depositionalEnviro' in item._name:
		multipleItems = item.cdata.split()
		for items in multipleItems:
			fields.append((items, 'yes'))
	elif 'depthDetermination' in item._name:
		multipleItems = item.cdata.split()
		for items in multipleItems:
			fields.append((items, 'yes'))
	else:
		fields.append((item._name, item.cdata))

for item in obj.LA_Site_Form.PHYSICALDESCRIPTION2.children:
	if 'vegetationCommunity' in item._name:
		multipleItems = item.cdata.split()
		for items in multipleItems:
			fields.append((items, 'yes'))
	elif 'topographicLocation' in item._name:
		multipleItems = item.cdata.split()
		for items in multipleItems:
			fields.append((items, 'yes'))
	else:
		fields.append((item._name, item.cdata))

for item in obj.LA_Site_Form.ASSEMBLAGE1.children:
	if 'assemblageContentLithics' in item._name:
		multipleItems = item.cdata.split()
		for items in multipleItems:
			fields.append((items, 'yes'))
	elif 'assemblageContentCeramics' in item._name:
		multipleItems = item.cdata.split()
		for items in multipleItems:
			fields.append((items, 'yes'))
	elif 'assemblageContentHistorics' in item._name:
		multipleItems = item.cdata.split()
		for items in multipleItems:
			fields.append((items, 'yes'))
	elif 'assemblageContentOthers' in item._name:
		multipleItems = item.cdata.split()
		for items in multipleItems:
			fields.append((items, 'yes'))
	else:
		fields.append((item._name, item.cdata))

for item in obj.LA_Site_Form.ASSEMBLAGE2.children:
	if 'datingPotential' in item._name:
		multipleItems = item.cdata.split()
		for items in multipleItems:
			fields.append((items, 'yes'))
	elif 'assemblageLithicCountSpecify' in item._name:
		if item.cdata == '0':
			fields.append((item._name, ''))
		else:
			fields.append((item._name, item.cdata))
	elif 'assemblageCeramicsCountSpecify' in item._name:
		if item.cdata == '0':
			fields.append((item._name, ''))
		else:
			fields.append((item._name, item.cdata))
	elif 'assemblageHistoricCountSpecify' in item._name:
		if item.cdata == '0':
			fields.append((item._name, ''))
		else:
			fields.append((item._name, item.cdata))
	elif 'assemblageTotalCountSpecify' in item._name:
		if item.cdata == '0':
			fields.append((item._name, ''))
		else:
			fields.append((item._name, item.cdata))
	else:
		fields.append((item._name, item.cdata))

index = 0
for item in obj.LA_Site_Form.COMPONENT.children:
	if 'repeatComponent' in item._name:
		index += 1
		for item in item.children:
			if 'earliestOccupationPeriod' in item._name:
				newItemName = item._name + str(index)
				fields.append((newItemName, parsePeriod(item.cdata)))
			elif 'latestOccupationPeriod' in item._name:
				newItemName = item._name + str(index)
				fields.append((newItemName, parsePeriod(item.cdata)))
			elif 'componentAffiliation' in item._name:
				newItemName = item._name + str(index)
				fields.append((newItemName, item.cdata))
			elif 'componentDatingStatus' in item._name:
				multipleItems = item.cdata.split()
				for items in multipleItems:
					newItemName = items + str(index)
					fields.append((newItemName, 'yes'))
			elif 'componentPhaseNames' in item._name:
				multipleItems = item.cdata.split()
				for items in multipleItems:
					newItemName = items + str(index)
					fields.append((newItemName, 'yes'))
			else:
				newItemName = item._name + str(index)
				fields.append((newItemName, item.cdata))
	else:
			fields.append((item._name, item.cdata))

index = 0
for item in obj.LA_Site_Form.FEATURES.children:
	if 'repeatFeature' in item._name:
		index += 1
		for item in item.children:
			newItemName = item._name + str(index)
			if 'featureType' in item._name:
				fields.append((newItemName, parseFeatureType(item.cdata)))
			else:
				fields.append((newItemName, item.cdata))
	else:
			fields.append((item._name, item.cdata))
	
for item in obj.LA_Site_Form.REFERENCES.children:
	fields.append((item._name, item.cdata))

for item in obj.LA_Site_Form.SITERECORD.children:
	if 'siteRecordAttachments' in item._name:
		multipleItems = item.cdata.split()
		for items in multipleItems:
			fields.append((items, 'yes'))
	else:
		fields.append((item._name, item.cdata))

for item in obj.LA_Site_Form.narrative:
	fields.append((item._name, item.cdata))

#write FDF file
fdf = forge_fdf("",fields,[],[],[])
lanum = str(obj.LA_Site_Form.IDOWN.LANUM.cdata)
filename = "LA" + lanum + ".fdf"
fdf_file = open(filename, "wb")
fdf_file.write(fdf)
fdf_file.close()

#fdf to pdf using pdftk
print ("Creating LA Form PDF for LA" + lanum + "...")
writePDF = "pdftk Blank_LA_Form.pdf fill_form " + filename + " output " + lanum + ".pdf"
call(writePDF)
print ("Removing temp file...")
os.remove(filename)
print ("Done!")
