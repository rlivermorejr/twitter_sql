import sqlite3
import random
from mimesis import Person, Text

############################################################
# Hopefully I have made this as easy as possible to run.   #
#                                                          #
# The functions are all called at the bottom of the page.  #
# The variables to control how many queries are above      #
# each of the add___() functions.                          #
#                                                          #
############################################################

# creates db file
con = sqlite3.connect('example.db')
cur = con.cursor()

# mimesis random person
en_person = Person('en')
# mimesis random tweet
tweet = Text()


class PrintTable():
    """
    This class is for displaying the tables in example.db
    Each of them are called at the bottom of program
    """
    def ShowUsers():
        cur.execute("SELECT * FROM twitteruser")
        print(cur.fetchall())

    def ShowTweets():
        cur.execute("SELECT * FROM tweet")
        print(cur.fetchall())

    def ShowNotifications():
        cur.execute("SELECT * FROM notification")
        print(cur.fetchall())


class Counter():
    """
    A basic counter class to stop while loop
    """

    def __init__(self):
        self.number = 1

    def add(self):
        self.number += 1

    def reset(self):
        self.number = 1

    def value(self):
        return self.number


# initialize counter
inc = Counter()

#############################################
#              Create Tables                #
#        queries are set up to not          #
#            create duplicates              #
#############################################

# create user table
cur.execute('''CREATE TABLE IF NOT EXISTS twitteruser(
              id INTEGER PRIMARY KEY,
              username VARCHAR(40) NOT NULL,
              password VARCHAR(40) NOT NULL,
              display_name VARCHAR(40) NOT NULL
  );''')

# create tweet table
cur.execute('''CREATE TABLE IF NOT EXISTS tweet(
              id INTEGER PRIMARY KEY,
              fk_twitteruser INT NOT NULL,
              body VARCHAR(140) NOT NULL,
              created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
  );''')

# create notification table
cur.execute('''CREATE TABLE IF NOT EXISTS notification (
              id INTEGER PRIMARY KEY,
              fk_user INT NOT NULL,
              fk_tweet INT NOT NULL
);''')


def ClearDB():
    """
    This will clear out each table. This function is
    called at the bottom of program. Deleting the file
    example.db will also reset the database.
    """
    cur.execute('''DELETE FROM twitteruser''')
    cur.execute('''DELETE FROM tweet''')
    cur.execute('''DELETE FROM notification''')


# amount of users to create
usernum = 500


def AddUser():
    """
    Function starts by getting a random
    name, password, and username from mimesis.
    The id is linked to the position of the counter.
    Then the queries are executed until the counter
    reaches the number defined in variable usernum.
    """
    print(inc.value())
    while inc.value() <= usernum:
        i = inc.value()
        n = en_person.name()
        pw = en_person.password()
        dn = en_person.username()
        cur.execute(
            '''INSERT INTO twitteruser (id, username, password, display_name) VALUES (?, ?, ?, ?);''', (i, n, pw, dn))
        inc.add()
        print(inc.value())
    inc.reset()
    print(inc.value())


# amount of tweets to make
twenum = 1000


def AddTweets():
    """
    Function starts by using mimesis to get a
    random string to be content of the tweet.
    The id is linked to the position of the counter.
    The user_id is the user that created the tweet,
    it is a randomly generated number based on the
    amount of users created above. Then the queries
    are executed until the counter reaches the
    number defined in variable twenum.
    """
    print(inc.value())
    while inc.value() <= twenum:
        t = tweet.text(quantity=1)
        i = inc.value()
        user_id = random.randrange(1, usernum)
        cur.execute(
            '''INSERT INTO tweet (id, fk_twitteruser, body) VALUES (?, ?, ?);''', (i, user_id, t))
        inc.add()
        print(inc.value())
    inc.reset()
    print(inc.value())


# amount of notifications to make
notinum = 200


def AddNotify():
    """
    Function starts by using random to get a user_id
    for the sending and recieving user. If the
    random numbers are the same, it will generate
    a new one for user2. Then the queries
    are executed until the counter reaches the
    number defined in variable notinum.
    """
    print(inc.value())
    while inc.value() <= notinum:
        user1 = random.randrange(1, usernum)
        user2 = random.randrange(1, twenum)
        if user1 == user2:
            user2 = random.randrange(1, usernum)
        cur.execute('''INSERT INTO notification (fk_user, fk_tweet) VALUES ((SELECT id FROM twitteruser WHERE id=?), (SELECT fk_twitteruser FROM tweet WHERE id=?));''', (user1, user2))
        inc.add()
        print(inc.value())
    inc.reset()
    print(inc.value())

###############################################################
#                    Function Calls                           #
# Uncomment the one you want to run, or run all at once       #
# I would not recommend printing the tables while running any #
# of the add___() functions. Run the add___() functions, then #
# uncomment whichever table you want to view.                 #
###############################################################


# AddUser()
# AddTweets()
# AddNotify()

# PrintTable.ShowUsers()
# PrintTable.ShowTweets()
# PrintTable.ShowNotifications()

#################
# CLEARS THE DB #
#################
# ClearDB()


con.commit()

con.close()
