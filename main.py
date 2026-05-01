from Voting import *

def main():
    application = QApplication([])
    window = Voting()
    window.show()
    application.exec()


if __name__ == "__main__":
    main()