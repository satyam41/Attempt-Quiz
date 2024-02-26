import mysql.connector as mysql

class Register:
    def __init__(self):
        self.con = mysql.connect(host='localhost', username='root',
                                 password='satyam10', database='quiz')
        if self.con.is_connected() == True:
            print("Connected to database")

    # TODO: unique username functionality for keep track of user and decrease the data duplicaticy.
    # FIXME: this fuciton check that username is unique or not if it's not unique it give a warning that user is already exists or if username is not unique it gives a success message and the process will continue.

    def unique_username(self, username):
        cursor = self.con.cursor()
        query = "SELECT * FROM register WHERE username = %s"
        cursor.execute(query, ([username]))
        result = cursor.fetchall()
        if len(result) == 0:
            print("UserName is already registered")
            return True
        else:
            return False

    # TODO: Register functions start from here
    # FIXME: new user can register for attempt quiz

    def register(self, userName, password, name, phoneNumber):
        try:
            cursor = self.con.cursor()
            query = "INSERT INTO register (username, password, name, phoneNumber) VALUES (%s, %s, %s, %s)"
            cursor.execute(query, (userName, password, name, phoneNumber))
            self.con.commit()
            print("You are now registered!!!")
        except mysql.Error as e:
            print("UserName is already exists")

    # TODO: Login functions start from here
    # FIXME: it works if username is already registered and password is set than its check the password and username of ther user and than you can login in and ready for attempt quiz

    def login(self, userName, password):
        cursor = self.con.cursor()
        query = "SELECT * FROM register WHERE username = %s AND password = %s"
        cursor.execute(query, (userName, password))
        result = cursor.fetchall()
        if len(result) == 1:
            print("You are now logged in!!!")
            return True
        else:
            print("Wrong username or password")
            return False

    # TODO: change password
    def change_password(self, userName, password):
        cursor = self.con.cursor()
        query = "update register set password=%s where userName=%s"
        cursor.execute(query, (password, userName))
        self.con.commit()
        print('Successfully updated password')

    # TODO: show profile information

    def show_profile(self, userName):
        cursor = self.con.cursor()
        query = "SELECT * FROM register WHERE userName = %s"
        cursor.execute(query, ([userName]))
        data = cursor.fetchall()
        for row in data:
            print(row)
        self.con.commit()

    # TODO: Attempt quiz functions start from here
    # FIXME: this fuction is for appear in the quiz

    def attempt_quiz(self, username, password):
        if self.login(username, password) == False:
            print("You are not login. Please try again!!!")
            return
        else:
            quiz = [
                {
                    "question": "Who developed Python Programming Language?",
                    "answer": "Guido van Rossum"
                },
                {
                    "question": "Is Python case sensitive when dealing with identifiers?",
                    "answer": "Yes"
                },
                {
                    "question": "Which keyword is used for function in Python language?",
                    "answer": "def"
                },
                {
                    "question": "What is output of print(math.pow(3, 2))?",
                    "answer": "9.0"
                }
            ]

        # Initialize result
        result = 0

        # Iterate through each question in the quiz
        for i, question in enumerate(quiz, 1):
            print(f"\nQuestion {i}: {question['question']}")
            user_answer = input("Your answer: ")

            # Check if the user's answer matches the correct answer
            if user_answer.lower() == question['answer'].lower():
                print("Correct!")
                result += 1
            else:
                print("Incorrect.")

        # Display final result
        cursor = self.con.cursor()
        query = "UPDATE register SET result = %s WHERE username = %s"
        cursor.execute(query, (result, username))
        self.con.commit()
        print("successfully result updated")

    # TODO: Reulst of the quiz is display here

    def getQuizResults(self, username):
        cursor = self.con.cursor()
        cursor.execute(
            "SELECT * FROM register WHERE username = '{}'".format(username))
        data = cursor.fetchall()
        for row in data:
            print(row)
        self.con.commit()


if __name__ == '__main__':
    try:
        register = Register()
        while True:
            print("======Welcome to the Quiz Game!======")
            print('''
                1.Register
                2.Login
                3.Change Password
                4.Show Profile
                5.Attemp Quiz
                6.Quiz Results
                7.Exit
            ''')
            choice = int(input('Enter your choice: '))
            if choice == 1:
                userName = input('Enter your username: ')
                password = input('Enter your password: ')
                name = input('Enter your name: ')
                phoneNumber = input('Enter your phone number: ')
                register.register(userName, password, name, phoneNumber)
            elif choice == 2:
                userName = input('Enter your username: ')
                password = input('Enter your password: ')
                register.login(userName, password)
            elif choice == 3:
                userName = input('Enter your username: ')
                password = input('Enter your new password: ')
                register.change_password(userName, password)
            elif choice == 4:
                userName = input('Enter your username: ')
                register.show_profile(userName)
            elif choice == 5:
                userName = input('Enter your username: ')
                password = input('Enter your password: ')
                register.attempt_quiz(userName, password)
            elif choice == 6:
                userName = input('Enter your username: ')
                register.getQuizResults(userName)
            elif choice == 7:
                print("Thank you for registering")
                break

    except KeyboardInterrupt:
        print('Exiting...')
