
# This backend consists of two main parts that live in separate app folders. 

<h2 align="center">
First part is Prediction Divorce app. 
</h2>

 Here we have an FAST API ML application that can predict whether you will be divorced or not based on 13 questions with accuracy 98%. 

You can read More about my own machine learning research (EDA) from DivorceResearch notebook in [DataScience directory](/DataScience). 

Resources:
- [Kaggle dataset](https://www.kaggle.com/datasets/csafrit2/predicting-divorce)
- [Backend app/docs](https://divorce-ml.herokuapp.com/redoc)
- [Mobile React Native app created by my friend](https://expo.dev/@plambir555/divorce)

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

Answers to these questions are numbers from 0 (Definitely no) to 4 (Definitely YES). 

The result will be a float value. Maximum is 1 - you will be divorced, 0 - you will not with 98% chances in both cases. 
The result will be produced by trained machine learning model named Random Forest Tree. 

<h2 align="center">
Second app is Mom's scientist app. 
</h2>

This app is continuation of the previous one. The main key point is: **what if user itself want to submit his own files and try to make some prediction?**


I'm willing to give an user such opportunity.
No need for low level knowledge, mathematics degree or PhD in Data Science. Just submit a csv, set target column and predict new outcomes in just a matter of 5 minutes. 
This app may be used for a wide range of tasks.
Using my app you will be able to predict the future, some kinds of outcomes with some degree of accuracy using ML algorithms under the hood. 

On current stage Mom's scientist app train two different type of ML models: Random forest and K-neighbours. The architecture of the app is made to be highly scalable in introducing new ML models, including neural nets (might be released later). 

Good to know or some constraints: 
1. On current stage app works only with csv files. 
2. Csv files values must be separated by comma. 
3. [EDA](https://cloud.google.com/blog/products/ai-machine-learning/building-ml-models-with-eda-feature-selection) is very important. 60% of success lies in EDA and preparing data for ML models. usually EDA and data cleaning is made by [Pandas](https://pandas.pydata.org). Let's suppose you are novice in data science. 
Before submitting files to train ML models you must be sure that you data does not have null values, if you have - [fill](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.fillna.html) it with 0 or [median](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.median.html) values (the last is much more preferable). 
Moreover you must get rid of dirty information, columns with data that definitely will not help in predicting results, but opposite (for example names of Titanic passengers if we want to predict will a passenger survive or no). And the last you must get rid of categorical values, [get_dummies](https://pandas.pydata.org/docs/reference/api/pandas.get_dummies.html) is right choice for you.
4. Structure (columns and values in columns) of a csv file must be the same in both cases: when we train models and when we predict new results.
5. When models are trained you will see [accuracy](https://developers.google.com/machine-learning/crash-course/classification/accuracy), [precision, recall](https://developers.google.com/machine-learning/crash-course/classification/precision-and-recall) values. Comparing these values you may choose the best model for your case. Usually the higher score - the better, max value is one. 
6. [Random forest](https://www.newgenapps.com/blogs/random-forest-analysis-in-ml-and-when-to-use-it-2/) and [K neighbours](https://towardsdatascience.com/knn-algorithm-what-when-why-how-41405c16c36f) ML models may not work in some cases. Neural nets (might be added later) are more universal. 


The below is example of how to use the Mom's scientist app. You can repeat these steps using titanic.csv and titanic_predict.csv files in root directory. Steps with registering and authorization are omitted, let's suppose that you acquired an JWT token and placed it in your authorization headers (if you interact with backend manually). EDA and data cleaning steps are omitted too, this is another topic. 
1. First you should upload a csv file using which models will be trained. Path is /moms_scientist/upload_csv. 
2. Then we can list uploaded file, so we might be sure that our file is correctly uploaded. Path /moms_scientist/list_csv


    [
        {
            "id": 8,
            "name": "titanic",
            "created": "2022-04-24T10:09:38.711020+00:00"
        }
    ]

3. [Optional] Next one should be training step, but this step may take a while because training models is CPU bound process. So you may connect to a socket on my backend and receive information about training completion in real time. socker connection address is: ws://localhost:8123/event_channel , after connection you must submit number of the channel you want to listen, this number is user id of your account. So to connect to the socket we must submit an message to connected socket:


    {
        "channel": "1"
    }

Where 1 - is user id. User id may be acquired here: /user/.
After submitting the message to the socket you will get information that connection has been successfully installed. 
NOTE (!) you must submit JWT tokens in authorization headers as you would do it with usual HTTP requests. After connecting to the socket and triggering model training you will get messages in socket connection. It will looks like that:

    Model k_neighbors was created for user_file_id 8
    Model random_forest_tree was created for user_file_id 8
    you are connected
    { "channel": "1" }
    Connected to ws://localhost:8123/event_channel

4. To start a training you must submit name of target column (column that you want to predict in the future) and user_file_id from step 2.


    {
      "target_column": "target",
      "user_file_id": 8
    }

5. When models are trained you can list them and chose the best. Path /moms_scientist/trained_models : 


    [
        {
            "id": 71,
            "name": "random_forest_tree",
            "accuracy": 0.8305084745762712,
            "precision": 0.85,
            "recall": 0.7083333333333334,
            "user_file_id": 8
        },
        {
            "id": 72,
            "name": "k_neighbors",
            "accuracy": 0.6711864406779661,
            "precision": 0.6949152542372882,
            "recall": 0.3416666666666667,
            "user_file_id": 8
        }
    ]

Here we can see that random forest three gave us the best results, this model can predict the future with 83% accuracy and that is not bad. 

6. Prediction time. For this purpose we are going to use titanic_predict.csv. This csv file is the same as titanic.csv file with only two exceptions: first we do not have target column named target, because we want to predict target, isn't? 
Second exception is that this csv consists of 5 first rows of titanic.csv file. This is made for simplicity purposes only, in real world prediction data must be different from that under which models was trained. 
The key point is that model must predict outcomes of data that it has not seen before. So we submit our csv files in here: /moms_scientist/get_prediction/71 where 71 is model id from step 5. And prediction result is:


    {
        "predictions": [
            [
                0.8648484848484849,
                0.13515151515151516
            ],
            [
                0.06666666666666667,
                0.9333333333333332
            ],
            [
                0.5763636363636364,
                0.4236363636363637
            ],
            [
                0.06666666666666667,
                0.9333333333333332
            ],
            [
                0.8365151515151515,
                0.16348484848484848
            ]
        ]
    }

Actual results were 0, 1, 1, 1, 0 for first 5 rows, where 0 - not survived, 1 - survived. We can see that our prediction model made wrong outcome only once, in third case.
We have got results in binary format, where first value in a group is probability of 0 (will die), the second is probability of 1 (will survive). The outcome may be different, it depends on the structure of target column and may be slightly difficult. 
For the first row our model predicts that with 86% chance this passenger will be survived. 


The result may be improved, usually it may be achieved by doing much better EDA, feature engineering and data cleaning. 

<h2 align="center">
About backend
</h2>

For both app the same backend is used, including the same DB, authorization and authentication JWT system.

Main stack techs that were used: 
* FAST API 
* SQLAlchemy
* ML: Scikit-learn Random Forest Tree, K-Neighbours
* Postgres, LISTEN/NOTIFY 
* Alembic
* Pandas + Numpy

Useful alembic commands:

    alembic init migrations
    alembic revision --autogenerate -m "Initial migrations"
    alembic upgrade heads 
    alembic revision -m "add a column to ..."