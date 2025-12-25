from controllers.menu_controller import MenuController


class AppContext:

    def __init__(self):
        self.menu_controller = MenuController()

    def run(self):
        return self.menu_controller.main_menu()
