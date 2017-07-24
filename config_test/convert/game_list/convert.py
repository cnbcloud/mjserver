# -*- coding=utf-8
'''
Created on 2015年7月30日

@author: zhaojiangang
'''

import codecs
import importlib
import json

import gdss


def buildNodes():
    nodes = {}
    mod = importlib.import_module('nodes')
    for name in dir(mod):
        if not name.startswith('__'):
            attr = getattr(mod, name)
            if isinstance(attr, dict):
                nodes[name] = getattr(mod, name)
    return nodes

def initTemplates(nodes):
    mod = importlib.import_module('templates')
    for nodeName in nodes.keys():
        setattr(mod, nodeName, nodeName)
    return mod

def writeTemplateForClientId(clientIdNumber, templateName):
    d = {
         "template" : templateName
    }
    jstr = json.dumps(d, ensure_ascii=False, indent=4)
    f = open('../../game/9999/gamelist/%s.json' % (clientIdNumber), 'w')
    f.write(jstr)
    f.close()
    
if __name__ == '__main__':
    nodes = buildNodes()
    nodeNames = nodes.keys()
    nodeNameLines = []
    for nodeName in nodeNames:
        nodeNameLines.append("%s='%s'" % (nodeName, nodeName))
    nodeNamesString = '\n'.join(nodeNameLines)
    
    f = codecs.open('./templates.txt')
    line = f.readline(2048)
    lines = []
    while (line):
        if line.startswith('${nodeNames}'):
            line = line.replace('${nodeNames}', nodeNamesString)
        lines.append(line)
        line = f.readline(2048)
    f.close()
    
    f1 = open('./templates.py', 'w')
    f1.writelines(lines)
    f1.close()
    
    templatesModel = initTemplates(nodes)
    templates = getattr(templatesModel, 'templates')

    conf = {'templates':templates, 'nodes':nodes}
    jstr = json.dumps(conf, ensure_ascii=False, indent=4)
    f = open('../../game/9999/gamelist/%s.json' % (0), 'w')
    f.write(jstr)
    f.close()

    template2clientIds = getattr(templatesModel, 'template2clientIds')
    clientIdMap = gdss.syncDataFromGdss('getClientIdDict')

    for templateName, template in templates.iteritems():
        clientIds = template2clientIds.get(templateName)
        print 'templateName=', templateName, 'clientIds=', clientIds
        if clientIds:
            for clientId in clientIds:
                clientIdNumber = clientIdMap.get(clientId)
                if clientIdNumber:
                    writeTemplateForClientId(clientIdNumber, templateName)
    
    