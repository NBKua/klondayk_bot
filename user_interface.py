# coding=utf-8


class UserPrompt(object):

    def __init__(self, gui_input=None):
        self.gui_input = None
        if gui_input:
            import  gui
            self.gui_input = gui.InputClass(gui_input)

    def prompt_user(self, prompt_string, choice):
        if len(choice) == 0:
            print "You have no  choice! Something went wrong."
        prompt_string += '\n' + "\n".join(
            [str(index + 1) + ": " + option
             for index, option in enumerate(choice)])
        prompt_string = prompt_string.encode('utf-8')
                                             # shouldn't be necessary
                                             # in Python3
                                             # http://bugs.python.org/issue7768
        while True:
            if self.gui_input:
                user_input = self.gui_input.raw_input(prompt_string)
            else:
                user_input = raw_input(prompt_string + "\n")
            try:
                selected_index = int(user_input) - 1
                if self.is_valid(selected_index, choice):
                    break
                else:
                    print user_input, "is invalid choice"
            except ValueError, e:
                print user_input, "is not a number"
        selected = choice[selected_index]
        print "You selected", selected
        return selected

    def is_valid(self, selected_index, choice):
        if selected_index in range(len(choice)):
            return True
        else:
            return False
