import csv
from DuplicateIDError import DuplicateIDError
from PyQt6.QtWidgets import *
from gui import *
import os


class Voting(QMainWindow, Ui_MainWindow):
    def __init__(self) -> None:
        """
        Method that sets up the UI, buttons with their respective methods, and
        loads existing CSV data or creates CSV file
        """
        super().__init__()
        self.setupUi(self)
        self.list = []
        self.vote_count1 = 0
        self.vote_count2 = 0

        self.Submit_button.clicked.connect(lambda: self.submit())
        self.Votes_button.clicked.connect(lambda: self.total_votes())


        if not os.path.isfile('voting.csv'):
            with open('voting.csv', 'w', newline = '') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(['ID', 'Candidate1', 'Candidate2'])

        else:
            header = True
            with open('voting.csv', 'r') as csvfile:
                reader = csv.reader(csvfile)
                for row in reader:
                    if header:
                        header = False

                    else:
                        self.list.append(row[0])

                        if row[1] == '✓ Voted':
                            self.vote_count1 += 1
                        elif row[2] == '✓ Voted':
                            self.vote_count2 += 1

    def submit(self) -> None:
        """
        Method that occurs when press submit button that
        collects and appends data to csv file
        """
        if self.Error_message.text() != '':
            self.Error_message.setText('')


        with open('voting.csv', 'a') as csvfile:
            writer = csv.writer(csvfile)

            try:
                user_id = self.ID_number.text()

                if not (user_id.isdigit() and len(user_id) == 5):
                    raise ValueError

                if user_id in self.list:
                    raise DuplicateIDError('')

                if not self.Candidate_1.isChecked() and not self.Candidate_2.isChecked():
                    self.Error_message.setText('Select a candidate')

                else:
                    self.list.append(user_id)

                if self.Candidate_1.isChecked():
                        self.vote_count1 += 1
                        writer.writerow([user_id, '✓ Voted', ''])

                elif self.Candidate_2.isChecked():
                        self.vote_count2 += 1
                        writer.writerow([user_id, '', '✓ Voted'])


            except ValueError:
                QMessageBox().critical(None, 'Error', 'ID must be 5 digits long')

            except DuplicateIDError:
                self.Error_message.setText('Already voted')


    def total_votes(self) -> None:
        """
        Method that displays the vote count for each candidate
        """
        voting_total = (
            'Total Votes:\n'
            f'Candidate 1:   {self.vote_count1}\n'
            f'Candidate 2:   {self.vote_count2}\n'
        )

        self.Votes_message.setText(voting_total)



