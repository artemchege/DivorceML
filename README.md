
## Here we have an FAST API ML application that can predict whether you will be divorced or not based on 13 questions with accuracy 98%. 

More about my own machine learning research you can read from DivorceResearch notebook in DataScience directory. 

Resources:
- [Kaggle dataset](https://www.kaggle.com/datasets/csafrit2/predicting-divorce)
- [Backend app/docs](https://divorce-ml.herokuapp.com/redoc)

We have next questions: 

    1. Hate_subject: my discussion with my spouse is not calm.
    2. Happy: we're compatible with my spouse about what love should be.
    3. Dreams: most of our goals for people (children, friends, etc.) are the same.
    4. Freedom_value: I think that one day in the future, when I look back, I see that my spouse, and I have been in harmony with each other.
    5. Likes: my spouse and I have similar values in trust.
    6. Calm_breaks: we're just starting a discussion before I know what's going on.
    7. Harmony: most of our goals are common to my spouse.
    8. Roles: my spouse and I have similar ideas about how marriage should be
    9. Inner_world: I can tell you what kind of stress my spouse is facing in her/his life.
    10. Current_stress: I know my spouse's basic anxieties.
    11. Friends_social: I know my spouse very well.
    12. Contact: when we need it, we can take our discussions with my spouse from the beginning and correct it.
    13. Insult: I can use offensive expressions during our discussions.

The result will be an integer. 1 - you will be divorced with 98% chances, 0 - you will not. 

Main stack that were used: 
* FAST API 
* SQLAlchemy
* ML: Scikit-learn/Random Forest Tree
* Postgres
* Alembic
* Pandas + Numpy

Useful alembic commands:

    alembic init migrations
    alembic revision --autogenerate -m "Initial migrations"
    alembic upgrade heads 
    alembic revision -m "add a column to ..."