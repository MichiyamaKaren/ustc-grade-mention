import json
from typing import List, Dict, Union


class Score:
        def __init__(self, id, courseNameCh, score, gp, **kwargs):
            self.id = str(id)
            self.courseNameCh = courseNameCh
            self.score = score
            self.gp = gp

        def __eq__(self, other):
            iseq = True
            for attr in dir(self):
                if not attr.startswith('_') and not callable(self.__getattribute__(attr)):
                    iseq = iseq and (self.__getattribute__(attr) == other.__getattribute__(attr))
            return iseq

        scorejsondict = Dict[str, str]

        def to_dict(self):
            return {'id': self.id, 'courseNameCh': self.courseNameCh, 'score': self.score, 'gp': self.gp}


class Semester:
    def __init__(self, id: str, scores: List[Dict[str, str]], **kwargs):
        self.id: str = str(id)
        self.scores: Dict[str, Score] = {str(s['id']): Score(**s) for s in scores}

    def difference_from(self, other: 'Semester') -> List[Score]:
        '''
        给出other.scores.update(self.scores)会被更新的Score（更新后的值）
        '''
        difference = []
        for course in other.scores:
            if course not in other.scores or (self.scores[course] != other.scores[course]):
                difference.append(self.scores[course])
        return difference

    semjsondict = Dict[str, Union[str, List[Score.scorejsondict]]]

    def to_dict(self) -> semjsondict:
        return {'id': self.id, 'scores': [s.to_dict() for s in self.scores.values()]}


def store_grade(allsems: Dict[str, Semester], filename):
    jsondict: Dict[str, Semester.semjsondict] = {semid: allsems[semid].DictForJSON() for semid in allsems}
    with open(filename, 'w') as jsonfile:
        json.dump(jsondict, jsonfile)


def load_grade(filename) -> Dict[str, Semester]:
    with open(filename) as jsonfile:
        jsondict: Dict[str, Semester.semjsondict] = json.load(jsonfile)

    allsems = {semid: Semester(**semjson) for semid, semjson in jsondict.items()}
    return allsems


def semester_dict_change(old: Dict[str, Semester], new: Dict[str, Semester]) -> List[Score]:
    change = []
    for semid in new:
        if semid in old:
            change.extend(new[semid].difference_from(old[semid]))
        else:
            change.extend(new[semid].scores.values())
    return change
