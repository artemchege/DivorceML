from enum import Enum

from pydantic import BaseModel, Field
# from schemas import UserCreated


# todo: вынести схемы юзера в корень проекта
class User(BaseModel):
    name: str
    email: str
    password: str


class UserCreated(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True


class DivorceChoices(Enum):
    worst = 1
    low = 2
    middle = 3
    good = 4
    best = 5


class DivorceQuestions(BaseModel):
    hate_subject: DivorceChoices  # 37. My discussion with my spouse is not calm.
    happy: DivorceChoices  # 16. We're compatible with my spouse about what love should be.
    dreams: DivorceChoices  # 14.	Most of our goals for people (children, friends, etc.) are the same.
    freedom_value: DivorceChoices  # 11. I think that one day in the future, when I look back, I see that my spouse,
    # and I have been in harmony with each other.
    likes: DivorceChoices  # 20. My spouse and I have similar values in trust.
    calm_breaks: DivorceChoices  # 40. We're just starting a discussion before I know what's going on.
    harmony: DivorceChoices  # 10.	Most of our goals are common to my spouse.
    roles: DivorceChoices  # 18. My spouse and I have similar ideas about how marriage should be
    inner_world: DivorceChoices  # 24. I can tell you what kind of stress my spouse is facing in her/his life.
    current_stress: DivorceChoices  # 26. I know my spouse's basic anxieties.
    friends_social: DivorceChoices  # 29. I know my spouse very well.
    contact: DivorceChoices  # 3. When we need it, we can take our discussions with my spouse from the beginning and
    # correct it.
    insult: DivorceChoices  # 34. I can use offensive expressions during our discussions.

    creator: UserCreated

    class Config:
        orm_mode = True

