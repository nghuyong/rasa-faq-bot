# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"
import json
from typing import Any, Text, Dict, List

from bert_serving.client import BertClient
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import numpy as np


class ActionGetFAQAnswer(Action):

    def __init__(self):
        super(ActionGetFAQAnswer, self).__init__()
        self.bc = BertClient()
        self.faq_data = json.load(open("./data/nlu/faq.json", "rt", encoding="utf-8"))
        self.standard_questions_encoder = np.load("./data/standard_questions.npy")
        self.standard_questions_encoder_len = np.load("./data/standard_questions_len.npy")
        print(self.standard_questions_encoder.shape)

    def get_most_similar_standard_question_id(self, query_question):
        query_vector = self.bc.encode([query_question])[0]
        score = np.sum((self.standard_questions_encoder * query_vector), axis=1) / (
                self.standard_questions_encoder_len * (np.sum(query_vector * query_vector) ** 0.5))
        top_id = np.argsort(score)[::-1][0]
        return top_id, score[top_id]

    def name(self) -> Text:
        return "action_get_answer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        query = tracker.latest_message['text']
        most_similar_id, score = self.get_most_similar_standard_question_id(query)
        if float(score) > 0.93:
            response = self.faq_data[most_similar_id]['a']
            dispatcher.utter_message(response)
            dispatcher.utter_message("Problem solved?")
        else:
            response = "Sorry, this question is beyond my ability..."
            dispatcher.utter_message(response)
            dispatcher.utter_message("Sorry, I can't answer your question. You can dial the manual serviece...")
        return []


def encode_standard_question():
    bc = BertClient()
    data = json.load(open("./data/nlu/faq.json", "rt", encoding="utf-8"))
    standard_questions = [each['q'] for each in data]
    print("Standard question size", len(standard_questions))
    print("Start to calculate encoder....")
    standard_questions_encoder = bc.encode(standard_questions)
    np.save("./data/standard_questions", standard_questions_encoder)
    standard_questions_encoder_len = np.sqrt(np.sum(standard_questions_encoder * standard_questions_encoder, axis=1))
    np.save("./data/standard_questions_len", standard_questions_encoder_len)


if __name__ == '__main__':
    encode_standard_question()
