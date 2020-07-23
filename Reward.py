import hashlib

class Reward:
    def __init__(self,rewardName,points,quantity,incentive):
        self.__rewardName = rewardName
        self.__rewardID = self.generate_rewardID()
        self.__points = points
        self.__quantity = quantity
        self.__incentive = incentive

    def generate_rewardID(self):
        prefix = f"reward-{hashlib.sha384(self.__rewardName.encode()).hexdigest()[0:6]}"
        return prefix

    def get_rewardID(self):
        return self.__rewardID
    def get_rewardName(self):
        return self.__rewardName
    def get_points(self):
        return self.__points
    def get_quantity(self):
        return self.__quantity
    def get_incentive(self):
        return self.__incentive

    def set_rewardID(self, userID):
        self.__userID = userID
    def set_rewardName(self, rewardName):
        self.__rewardName = rewardName
    def set_points(self, points):
        self.__points = points
    def set_quantity(self, quantity):
        self.__quantity = quantity
    def set_incentive(self, incentive):
        self.__incentive = incentive