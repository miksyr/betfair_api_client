
class Competition:

    def __init__(self, competitionName: str, competitionId: int):
        self.competitionName = competitionName.strip()
        self.competitionId = int(competitionId)

    def __repr__(self):
        return f'{self.competitionName} ({self.competitionId})'

    def __str__(self):
        return self.__repr__()

    def __eq__(self, other):
        return self.__hash__() == other.__hash__()

    def __hash__(self):
        return hash((self.competitionName, self.competitionId))
