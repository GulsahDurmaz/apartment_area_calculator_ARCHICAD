from archicad import ACConnection
import archicad
import sys

# from archicad.releases.ac25.b3000types import ElementPropertyValue
conn = ACConnection.connect()

assert conn

acc = conn.commands
act = conn.types
acu = conn.utilities

elements = acc.GetElementsByType('Zone')
propArray = []
zoneName = acu.GetBuiltInPropertyId('Zone_ZoneName')
zoneArea = acu.GetBuiltInPropertyId('Zone_MeasuredArea')
zoneNumber = acu.GetUserDefinedPropertyId('Raeume','box_Einheitennummer') #acu.GetBuiltInPropertyId('Zone_ZoneNumber')
zoneCategory = acu.GetBuiltInPropertyId('Zone_ZoneCategoryCode')
zoneLayer = acu.GetBuiltInPropertyId('ModelView_LayerName')
totalsId = acu.GetUserDefinedPropertyId('Raeume','box_Einheitensumme') #acu.GetUserDefinedPropertyId('Apartment Totals','Areas') 
showFlag = acu.GetUserDefinedPropertyId('Raeume','box_Einheitensumme_Show')
# typoId = acu.GetUserDefinedPropertyId('Apartment Totals','Typology')
# roomNumId = acu.GetUserDefinedPropertyId('Apartment Totals','Number')

propArray.append(zoneName) #0
propArray.append(zoneNumber) #1
propArray.append(totalsId) #2
propArray.append(zoneLayer) #3
propArray.append(zoneArea) #4
propArray.append(zoneCategory) #5
propArray.append(showFlag) #6
propArray.append

value =acc.GetPropertyValuesOfElements(elements,propArray)

floorZones ={}
floorGuid = {}
roomZones =[]

for index,element in enumerate(value):
    check = str(element.propertyValues[1].propertyValue.value)
    print(element.propertyValues[6].propertyValue.value)
    if check == '':
        continue
    if element.propertyValues[6].propertyValue.value == True: #'a 063   Einheitenfläche': # 'A - Zones - Floor Areas.3D'
        
        floorZones[str(element.propertyValues[1].propertyValue.value)] = element
        floorGuid[str(element.propertyValues[1].propertyValue.value)] = elements[index].elementId
        print(">>>", element.propertyValues[1].propertyValue.value)
        
    if element.propertyValues[3].propertyValue.value == 'a 063   Raumstempel': # 'A - Zones - Room.3D'
        roomZones.append(element)
    else:
        continue

for key,value  in floorZones.items():
     xstr = str(value.propertyValues[1].propertyValue.value) #Zone Number
     floorZones[xstr].propertyValues[2].propertyValue.value = 0
extra = {}
for index,num in enumerate(roomZones):
    xstr = str(num.propertyValues[1].propertyValue.value) #Zone Number
    code = num.propertyValues[5].propertyValue.value
    extra[xstr] = {'code':code,'number': xstr}
    print(">>> xstr:",xstr)
    tot = num.propertyValues[4].propertyValue.value #Zone Area
    floorZones[xstr].propertyValues[2].propertyValue.value += tot

EPVArray = []
for key,value in floorZones.items():
    buffer = value.propertyValues[2].propertyValue.value #Zone Area
    index =  str(value.propertyValues[1].propertyValue.value)
    code = extra[index]['code']
    roomnum =extra[index]['number']
    normalnum = act.NormalStringPropertyValue(roomnum,type='string',status = 'normal')
    normalcode = act.NormalStringPropertyValue(code,type='string',status = 'normal')
    normalArea = act.NormalAreaPropertyValue(buffer,type='area',status = 'normal')
    element = floorGuid[index]
    EPV =act.ElementPropertyValue(element,totalsId, normalArea)
    EPVArray.append(EPV)
    # EPV =act.ElementPropertyValue(element,typoId, normalcode)
    # EPVArray.append(EPV)
    # EPV =act.ElementPropertyValue(element,roomNumId, normalnum)
    # EPVArray.append(EPV)
result = acc.SetPropertyValuesOfElements(EPVArray)
print(result)
