from Member import Member
import shelve
import hashlib

class Feedback(Member):
    def __init__(self, fullName, userName, password, email, message):
        self.__fullName = fullName
        self.__userName = userName
        self.__email = email
        self.__message = message
        self.__status = "Pending"
        self.__id = self.generateFeedbackID()
        Member.__init__(self, userName, password)


    def generateFeedbackID(self):
        prefix = f"feedback-{hashlib.sha384(self.__message.encode() + self.__userName.encode()).hexdigest()[0:6]}"
        return prefix

    def get_fullName(self):
        return self.__fullName

    def get_userName(self):
        return self.__userName

    def get_email(self):
        return self.__email

    def get_message(self):
        return self.__message

    def get_status(self):
        return self.__status
    
    def get_feedbackID(self):
        return self.__id

    def set_fullName(self, fullName):
        self.__fullName = fullName

    def set_userName(self, userName):
        self.__userName = userName

    def set_email(self, email):
        self.__email = email

    def set_message(self, message):
        self.__message = message

    def set_status(self, status):
        self.__status = status
