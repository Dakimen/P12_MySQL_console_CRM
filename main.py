from controllers.app_controller import AppController


def main():
    """
    Start application.
    Entry point of the application, initializing the app controller
    and entering the application.
    """
    app = AppController()
    app.run()


main()
