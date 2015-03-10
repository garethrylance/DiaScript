#layer  = dia.active_display().diagram.data.active_layer.objects[0]
#import sys,os
#sys.path.append(os.path.abspath("C:\\dev\\src\\DiaScripts\\"))
#import createClasses
#createClasses.go()
#reload(createClasses)
# test = dia.active_display().diagram
#uml = test.data.active_layer.objects[0]

import sys, math, dia, types, string,os


class UmlAttribute:
    def __init__(self, name,type):
        self.name = name
        self.type = type

    def __repr__(self):
        return self.name + ':'+ self.type

class UmlClass:
    
    def __init__(self, name,attributes):
        self.name = name
        self.attributes =[]
        for att in attributes :
            self.attributes.append(UmlAttribute(att[0],att[1]))
    
    def __repr__(self):
        return self.name

def distribute_objects_gjr (objs) :
	width = 0.0
	height = 0.0
	for o in objs :
		if width < o.properties["elem_width"].value :
			width = o.properties["elem_width"].value
		if height < o.properties["elem_height"].value : 
			height = o.properties["elem_height"].value
	# add 20 % 'distance'
	width *= 1.2
	height *= 1.2
	area = len (objs) * width * height
	max_width = math.sqrt (area)
	x = 0.0
	y = 0.0
	dy = 0.0 # used to pack small objects more tightly
	for o in objs :
		if dy + o.properties["elem_height"].value * 1.2 > height :
			x += width
			dy = 0.0
		if x > max_width :
			x = 0.0
			y += height
		o.move (x, y + dy)
		dy += (o.properties["elem_height"].value * 1.2)
		if dy > .75 * height :
			x += width
			dy = 0.0
		if x > max_width :
			x = 0.0
			y += height

def cleanValues(values):
    newValues = []
    for value in values:
        newValues.append(value.strip())
    return newValues

def parseFiles(fileName)  :
    fileName = os.path.abspath(fileName)
    file = open(fileName, "r")

    parsedLines=[]
    for line in file.readlines():
        rawValues = line.split(',')
        cleanedValues = cleanValues(rawValues)
        if(len(cleanedValues[0]) > 0):
            parsedLines.append(cleanedValues)
        
    return parsedLines


def loadClassesFromFile(filename):
    classesToMake = []
    curretAttrubutes = []
    currentName = None
    for item in parseFiles(filename):
        if (len(item) == 1):
            if(currentName != None):
                classesToMake.append(UmlClass(currentName,curretAttrubutes))
                curretAttrubutes = []
            currentName = item[0]
        if(len(item) == 2):
            curretAttrubutes.append(item)

            
    classesToMake.append(UmlClass(currentName,curretAttrubutes))
    return classesToMake
			
def GetClassesToMake():
				return loadClassesFromFile("C:\\dev\\src\\DiaScript\\test.txt")
				
				
def go () :
	diagram = dia.new("classes.dia")
	# passed in data is not necessary valid - we are called from the Toolbox menu
	data = diagram.data
	display = diagram.display()

	layer = data.active_layer
	
	for classToMake in GetClassesToMake():
		oType = dia.get_object_type ("UML - Class")
		o, h1, h2 = oType.create (0,0)  
		o.properties["name"] = classToMake.name
		attributes = []
		for att in classToMake.attributes:
			attributes.append((att.name, att.type, '', '', 3, 0, 0))
			
		o.properties["attributes"] = attributes
		layer.add_object (o)

	distribute_objects_gjr (layer.objects)

	if diagram :
		diagram.update_extents()
		diagram.flush()
	# work with bindings test
	return data