# Comics works on a plugin principle, allowing easy
# option to add more comics
# To create a new comic entry, create a relevant folder
# under the plugins directory. In there, create a main.py module
# that has a few methods (see an existing example)
# In the run() method, you can do ***** whatever ***** you want
# (though you probably shouldn't!)


import imp
import os
import alfred
import sys

PluginFolder = "./plugins"
MainModule = "main"

def getPlugins():
    plugins = []
    possibleplugins = os.listdir(PluginFolder)
    for i in possibleplugins:
        location = os.path.join(PluginFolder, i)
        if not os.path.isdir(location) or not MainModule + ".py" in os.listdir(location):
            continue
        info = imp.find_module(MainModule, [location])
        plugins.append({"name": i, "info": info, "location": location})
    return plugins

def loadPlugin(plugin):
    return imp.load_module(MainModule, *plugin["info"])

def runPlugin(name):
	target = next(i for i in getPlugins() if name == i["name"])
	plugin = loadPlugin(target)
	if ( plugin.enabled() ):
		plugin.run();

def comics():
	if len(sys.argv) == 2:
		comic = sys.argv[1]
		runPlugin(comic)
		return

	feedback_items = []
	for i in getPlugins():
		plugin = loadPlugin(i)
		if (plugin.enabled()):
			feedback_items.append(
				alfred.Item(
					attributes = { 
					'uid' : alfred.uid(i["name"]),
					'arg' : i["name"]
					},
					title = plugin.title(),
					subtitle = plugin.subtitle(),
					icon = os.path.join(i["location"], "icon.png")
				)
			)
	xml = alfred.xml(feedback_items)
	alfred.write(xml)

if __name__ == "__main__":
    comics()
