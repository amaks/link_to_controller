import sublime, sublime_plugin, os
# cmd + alt + 6

_myGlobal           = None
_myGlobalController = None

class LinkToControllerCommand(sublime_plugin.TextCommand):

  def run(self, edit):
    global _myGlobal
    global _myGlobalController
    _myGlobal   = None
    file_name   = self.view.file_name()
    source_path = os.path.dirname(file_name)
    folder_path = os.path.dirname(source_path)

    # FIXME - have to detect namespace for correct controller name

    if 'views' in folder_path:
      if folder_path.split('/')[-1] != 'views':
        last_folder = source_path.split('/')[-1]
        if os.path.exists(folder_path.replace(folder_path.split('/')[-1], '').replace('views', 'controllers') + last_folder):
          rails_view_path = os.path.dirname(source_path).replace('views', 'controllers') + '/'
        else:
          rails_view_path = os.path.dirname(folder_path).replace('views', 'controllers') + '/'
      else:
        rails_view_path = os.path.dirname(source_path).replace('views', 'controllers/')
    else: # helpers
      rails_view_path = os.path.dirname(source_path) + '/controllers/'

    region           = self.view.sel()[0]
    controller_point = self.view.word(region)
    controller_path  = self.view.substr(controller_point)
    files            = []
    controller_name  = controller_path.split('_path')[0]

    if len(controller_name.split('_')) == 1:

      if controller_name.split('_')[0][-1] == 's':
        file_name = rails_view_path + controller_name.split('_')[0] + '_controller.rb'
      else:
        file_name = rails_view_path + controller_name.split('_')[0] + 's_controller.rb'

      if os.path.isfile(file_name):
        self.detect_action_name(file_name, file_name)
        _myGlobalController = file_name
        sublime.active_window().open_file(file_name)

    elif len(controller_name.split('_')) > 1:
      name  = ''
      array = controller_name.split('_')

      for c in reversed(array):
        if name != '':
          if os.path.exists(rails_view_path + '/' + c): # detecting if namespace present
            name =  c + '/' + name
          else:
            name =  c + '_' + name
        else:
          name += c

        print(c)
        print(name)

        if name[-1] != 's':
          file_name = rails_view_path + name + 's_controller.rb'
        else:
          file_name = rails_view_path + name + '_controller.rb'

        if os.path.isfile(file_name):
          _myGlobalController = file_name
          files.append(file_name)

      if len(files) == 1:
        if os.path.isfile(files[0]):
          self.detect_action_name(file_name, files[0])
          sublime.active_window().open_file(files[0])
      else:
        self.files = files
        sublime.active_window().show_quick_panel(files, self.open_file)

  def open_file(self, index):
    if index >= 0:
      sublime.active_window().open_file(os.path.join(self.files[index]))

  def detect_action_name(self, file_name, first_file):
    global _myGlobal

    action_name = file_name.split('/')[-1].split(first_file.split('/')[-1])[0].replace('_', '')

    print('detect_action_name')
    print(file_name)
    print(file_name.split('/')[-1])
    print(first_file)
    print(first_file.split('/')[-1])
    print(action_name)

    if action_name is not None:
      # new || edit
      _myGlobal   = 'def ' + action_name
    else:
      # show || index
      if first_file.split('_path')[-1][-1] == 's':
        _myGlobal = 'def index'
      else:
        _myGlobal = 'def show'

class LoadListener(sublime_plugin.ViewEventListener):

  def on_activated(self):
    global _myGlobal
    global _myGlobalController
    if _myGlobalController == self.view.file_name():
      action_def   = self.view.find(_myGlobal, 0)
      line, column = self.view.rowcol(action_def.begin())
      self.view.run_command("goto_line", {"line": line + 2} )