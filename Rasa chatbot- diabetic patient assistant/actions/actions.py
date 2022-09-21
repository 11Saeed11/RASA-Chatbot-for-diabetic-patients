# This files contains your custom actions which can be used to run
# custom Python code.

# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

from msilib.schema import Error
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import sqlite3 # importing sqlite3 to be able to read from the food database CaloriesDB

# Class used to connect with the database
def create_connection(db_file):
    """ create a database connection to the SQLite database
    specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn
# Class developed to print out the message of the user using the slots given
def select_from_foods(conn, slot_name, slot_value):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"""SELECT * FROM CaloriesDB
            WHERE {slot_name} = '{slot_value.lower()}'""")
    rows = cur.fetchall()
    for row in rows:
        return f"One {row[0]} contain {row[1]} Calories and {row[2]} grams of Carbohydrates"

# Class used to query the database for foods mentioned (currently fruits)
class QueryNumberOfCalories(Action):

    def name(self) -> Text:
        return "query_number_of_calories"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        conn = create_connection("C:/Rasa Projects/Rasa chatbot- diabetic patient assistant/CaloriesDB/CaloriesDB")
        slot_value = tracker.get_slot("food")
        slot_name = "Food"

        get_query_results = select_from_foods(conn,slot_name,slot_value)


        dispatcher.utter_message(text=str(get_query_results))



        return []


