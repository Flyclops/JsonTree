import sublime, sublime_plugin, json
from collections import OrderedDict

class JsonTreeCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        self.keys = []
        self.trimkeys = []
        content = self.view.substr(sublime.Region(0, self.view.size()))
        try:
            #json_data = json.loads(content)
            json_data = json.JSONDecoder(object_pairs_hook=OrderedDict).decode(content)
            self.fill_keys(json_data)
            sublime.active_window().show_quick_panel(self.keys, self.goto)
        except Exception as ex:
            print(ex)

    def fill_keys(self, json_data, indent=0):
        if isinstance(json_data, OrderedDict):
            for key in json_data:
                item = json_data[key]
                post = '"..."'
                if isinstance(item, dict):
                    post = '{...}'
                elif isinstance(item, list):
                    post = '[...]'
                self.keys.append('%s%s: %s' % (' ' * indent, key, post))
                self.trimkeys.append('"%s"' % key)
                self.fill_keys(json_data[key], indent+3)
        elif isinstance(json_data, list):
            for index, item in enumerate(json_data):
                if isinstance(item, str):
                    self.keys.append('%s%d. %s' % (' ' * indent, index, item))
                    self.trimkeys.append('"%s"' % item)
                elif isinstance(item, dict):
                    self.keys.append('%s%d. {...}' % (' ' * indent, index))
                    self.trimkeys.append('')
                    self.fill_keys(item, indent+3)



    def goto(self, arrpos):
        # The position gives us the line number
        strgo = self.trimkeys[arrpos]

        # Check for matches in the array before 48
        found = 0
        for index, item in enumerate(self.trimkeys):
            if index >= arrpos:
                break
            if item == strgo:
                found += 1

        # Now we need to find that string N times in 
        # the text, and go to its line number
        # and highlight it, why not?
        regions = self.view.find_all(strgo, sublime.LITERAL)
        region = regions[found]
        self.view.sel().clear()
        self.view.sel().add(region)
        self.view.show(region)


