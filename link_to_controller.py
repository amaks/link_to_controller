import sublime, sublime_plugin, os

class LinkToControllerCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    # find word on region
    file_name       = self.view.file_name()
    source_path     = os.path.dirname(file_name)
    rails_view_path = os.path.dirname(source_path).replace('views', 'controllers/')

    region           = self.view.sel()[0]
    controller_point = self.view.word(region)
    controller_path  = self.view.substr(controller_point)
    files            = []
    controller_name  = controller_path.split('_path')[0]

    if len(controller_name.split('_')) == 1:
      sublime.active_window().open_file(rails_view_path + controller_name.split('_')[0] + '_controller.rb')
    elif len(controller_name.split('_')) > 1:
      name = ''
      array = controller_name.split('_')
      for c in reversed(array):
        if name != '':
          name =  c + '_' + name
        else:
          name += c

        if name[-1] != 's':
          file_name = rails_view_path + name + 's_controller.rb'
        else:
          file_name = rails_view_path + name + '_controller.rb'
        if os.path.isfile(file_name):
          files.append(file_name)

      if len(files) == 1:
        sublime.active_window().open_file(files[0])
      else:
        self.files = files
        sublime.active_window().show_quick_panel(files, self.open_file)

  def open_file(self, index):
    if index >= 0:
      sublime.active_window().open_file(os.path.join(self.files[index]))