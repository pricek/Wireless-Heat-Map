import re

class Regex_Helper:
    abbrRE = re.compile('\((.*)\)$')
    buildRE = re.compile('(?P<abbr>.*?)(?:-b(?P<building>[0-9]{4}))?(?:-f(?P<floor>[0-9]+))?(?:-r(?P<room>.*))?$')
    floorRE = re.compile('.*-f([0-9]{4}[-$].*)')
    roomRE  = re.compile('.*-r([0-9]{4}[-$].*)')
