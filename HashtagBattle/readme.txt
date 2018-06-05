Instructions To run

1. Git clone from repo
2. Create and activate a virtual environment with python 3.6.5 installed
3. Install using pip requirements.txt
4. Generate Twitter credentials and put them in the appropriate place in settings.py
5. Create super-admin
6. Run the server with 'manage.py runserver'. Go to the admin site at http://localhost:8000/admin/
7. Create a new battle with given dates, then create at least two tags. Then create a new battle-tag for each new tag to be assocated with the newly created battle. After the second battle-tag is created. The program will keep a connection open listening to twitter for new tags and then adding 
the number of typos in the db. This programs supports more than two tags in a given battle. Note if the program is halted for whatever reason
or the provided start time is earlier than the start of the program there will be gaps in the number of typos collected.
8.  In order to access the winner, call GET {route}/api/winner/{battleId}.

http://127.0.0.1:8000/api/winner/12 would return something like...

{
    "battle": [
        {
            "id": 13,
            "name": "last",
            "start_date": "2018-06-05T21:00:06Z",
            "end_date": "2018-06-05T23:00:08Z"
        }
    ],
    "tags": [
        {
            "typos": 6,
            "tag": {
                "tag_text": "Clinton",
                "id": 4
            }
        },
        {
            "typos": 46,
            "tag": {
                "tag_text": "Obama",
                "id": 8
            }
        },
        {
            "typos": 490,
            "tag": {
                "tag_text": "Trump",
                "id": 5
            }
        }
    ],
    "winning": {
        "typos": 6,
        "tag": {
            "tag_text": "Clinton",
            "id": 4
        }
    }
}

Ideas for improvement. A cache followed by periodic bulk uploads instead of just writing to the database as the data stream comes in. Deprecate pyenchant, the spellchecking library which is no longer in development. Replace it with a more sophisticated natural language processing library. Keep track of the
length of each tweet in the database to do length comparisons and average typo per word typed. As things stand right now, the person tweeted 
about the most will be the one withe most typos. Also, add in tweet history with the Twitter search tweets resource even if it does
not have perfect data fidelity.

If you have any questions. Please do not hesitate to email me at parksa243@gmail.com.

