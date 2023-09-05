from archicad import ACConnection
from pprint import pprint #prints the data prettier

conn = ACConnection.connect()
assert conn

acc = conn.commands
act = conn.types
acu = conn.utilities

elements = acc.GetElementsByType('Zone')
propArray = []
pIdsNetArea = acu.GetBuiltInPropertyId('Zone_NetArea')
pIdUnitNames = acu.GetUserDefinedPropertyId('Area', 'box_Einheitennummer')

propArray.append(pIdUnitNames)
propArray.append(pIdsNetArea)

value =acc.GetPropertyValuesOfElements(elements,propArray)

# arrUnitName = []
# arrFloorArea = []
units = {"unitName": [], "floorArea": []}

for index,element in enumerate(value):
    check = str(element.propertyValues[0].propertyValue.value)
    if check == '':
        continue
    unitName = element.propertyValues[0].propertyValue.value
    floorArea = element.propertyValues[1].propertyValue.value
    units["unitName"].append(unitName)
    units["floorArea"].append(floorArea)

    # arrUnitName.append(unitName)
    # arrFloorArea.append(floorArea)

for key,value  in units.items():
    xstr = str(value.propertyValues[0].propertyValue.value)
    units[xstr].propertyValues[1].propertyValue.value = 0


print(units)





# pIdsNetArea = acu.GetBuiltInPropertyId('Zone_NetArea')
# zoneArea = acc.GetPropertyValuesOfElements(elements, [pIdsNetArea])
# areaValues = []
# totalArea = 0
# for item in zoneArea:
#     value = item.propertyValues[0].propertyValue.value
#     areaValues.append(value)
# #     totalArea = totalArea + value
# # print(totalArea)
# print(areaValues)

# pIdUnitNames = acu.GetUserDefinedPropertyId('Area', 'box_Einheitennummer')
# unitNames = acc.GetPropertyValuesOfElements(elements, [pIdUnitNames])
# arrUnitName = []
# for item in unitNames:
#     unitName = item.propertyValues[0].propertyValue.value
#     arrUnitName.append(unitName)
# # arrUnitName = list(set(arrUnitName))
# print(arrUnitName)
# z = zip(arrUnitName, areaValues)
# print(list(z))
# # class Unit:
# #     def __init__(self, name):
# #         self.name = name
# #     def __init__(self, area):
# #         self.area = area
# # ??? = Unit(name=???)


# # print(type(value))
# # print(dir(value))
