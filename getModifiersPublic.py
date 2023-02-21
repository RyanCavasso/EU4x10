import re
import urllib.request
from os import listdir
from os.path import isfile, join


#gets the modifier name for all non-constant modifiers (not yes/no and not min autonomy)
rawRegex = "<tr>\n<td>(.*)\n<\/td>\n<td><code>.*\n.*\n.*\n.*\n.*\n?.*\n?<td>[AM]"

#gets the variable and constant text (as separate groups) for modifiers with variable names
#example of variable name: <tech>_cost_modifier
variableRegex = "&lt;(.*)&gt;(.*)"

#gets the factions from factions files
factionsRegex = "(.+) =[ \n]{"

#gets the estates from estates files
estatesRegex = "estate_(.*) = {"

directory = "...\\steamapps\\common\\Europa Universalis IV" #Set this to your EU4 directory, e.g. C:\\...\\steamapps\\common\\Europa Universalis IV
if directory == "...\\steamapps\\common\\Europa Universalis IV":
    print("Insert path to your EU4 directory: ")
    directory = input()
commonDir = directory + "\\common"

cleanFile = "modifiers.txt"

#get all modifiers from raw html from the wiki
modifiersHtml = urllib.request.urlopen("https://eu4.paradoxwikis.com/Modifier_list")
modifiers = re.findall(rawRegex, modifiersHtml.read().decode("utf8"))
modifiersHtml.close()

#get name of all factions
factions = []
for file in [f for f in listdir(commonDir + "\\factions") if isfile(join(commonDir + "\\factions", f))]:
    fin = open(commonDir + "\\factions\\" + file, "r")
    for match in re.findall(factionsRegex, fin.read()):
        if match != "\tmodifier" and match != "\tallow":
            factions += [match]
    fin.close()

#get name of all estates
estates = []
for file in [f for f in listdir(commonDir + "\\estates") if isfile(join(commonDir + "\\estates", f))]:
    fin = open(commonDir + "\\estates\\" + file, "r")
    estates += re.findall(estatesRegex, fin.read())
    fin.close()


#prints list of modifier names
fout = open(cleanFile, "w")

for modifier in modifiers:
    variable = re.search(variableRegex, modifier)
    if(variable != None):   # If the modifier name has a variable in it, change that variable to a constant
        if(variable.group(1) == "tech"):    # If the variable was <tech> add adm_tech, mil_tech, and dip_tech as separate modifiers
            fout.write("adm_tech" + variable.group(2) + '\n')
            fout.write("dip_tech" + variable.group(2) + '\n')
            fout.write("mil_tech" + variable.group(2) + '\n')
        if(variable.group(1) == "faction"): # If the variable was <faction> add all faction variants, pulled from the factions directory
            for faction in factions:
                fout.write(faction + variable.group(2) + '\n')
        if(variable.group(1) == "estate"):  # If the variable was <estate> add all estate variants, pulled from the estates directory
            for estate in estates:
                fout.write(estate + variable.group(2) + '\n')
    else:
        fout.write(modifier + '\n')

fout.close()
