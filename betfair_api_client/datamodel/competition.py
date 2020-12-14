
class Competition:

    def __init__(self, competitionName, competitionId):
        self.competitionName = competitionName
        self.competitionId = competitionId

    def __repr__(self):
        return f'{self.competitionName} ({self.competitionId})'
