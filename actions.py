# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/


# This is a simple example for a custom action which utters "Hello World!"
import json
from typing import Any, Text, Dict, List
import torch
from bert_serving.client import BertClient
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import numpy as np
from sentence_transformers import SentenceTransformer

# sentence embedding selection
sentence_transformer_select=True
pretrained_model='bert-base-nli-mean-tokens' # Refer: https://github.com/UKPLab/sentence-transformers/blob/master/docs/pretrained-models/nli-models.md
score_threshold = 0.80  # This confidence scores can be adjusted based on your need!!

# Custom Action
class ActionGetFAQAnswer(Action):

    def __init__(self):
        super(ActionGetFAQAnswer, self).__init__()
        self.faq_data = json.load(open("./data/nlu/faq.json", "rt", encoding="utf-8"))
        self.sentence_embedding_choose(sentence_transformer_select, pretrained_model)
        self.standard_questions_encoder = np.load("./data/standard_questions.npy")
        self.standard_questions_encoder_len = np.load("./data/standard_questions_len.npy")
        print(self.standard_questions_encoder.shape)

    def sentence_embedding_choose(self, sentence_transformer_select=True, pretrained_model='bert-base-nli-mean-tokens'):
        self.sentence_transformer_select = sentence_transformer_select
        if sentence_transformer_select:
            self.bc = SentenceTransformer(pretrained_model)
        else:
            self.bc = BertClient(check_version=False)

    def get_most_similar_standard_question_id(self, query_question):
        if self.sentence_transformer_select:
            query_vector = torch.tensor(self.bc.encode([query_question])[0]).numpy()
        else:
            query_vector = self.bc.encode([query_question])[0]
        print("Question received at action engineer")
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
        print(query)
        most_similar_id, score = self.get_most_similar_standard_question_id(query)
        print("The question is matched with id:{} with score: {}".format(most_similar_id,score))
        if float(score) > score_threshold: # This confidence scores can be adjusted based on your need!!
            response = self.faq_data[most_similar_id]['a']
            dispatcher.utter_message(response)
            dispatcher.utter_message("Problem solved?")
        else:
            response = "Sorry, this question is beyond my ability..."
            dispatcher.utter_message(response)
            dispatcher.utter_message("Sorry, I can't answer your question. You can dial the manual service...")
        return []


def encode_standard_question(sentence_transformer_select=True, pretrained_model='bert-base-nli-mean-tokens'):
    """
    This will encode all the questions available in question database into sentence embedding. The result will be stored into numpy array for comparision purpose.
    """
    if sentence_transformer_select:
        bc = SentenceTransformer(pretrained_model)
    else:
        bc = BertClient(check_version=False)
    data = json.load(open("./data/nlu/faq.json", "rt", encoding="utf-8"))
    standard_questions = [each['q'] for each in data]
    print("Standard question size", len(standard_questions))
    print("Start to calculate encoder....")
    if sentence_transformer_select:
        standard_questions_encoder = torch.tensor(bc.encode(standard_questions)).numpy()
    else:
        standard_questions_encoder = bc.encode(standard_questions)
    np.save("./data/standard_questions", standard_questions_encoder)
    standard_questions_encoder_len = np.sqrt(np.sum(standard_questions_encoder * standard_questions_encoder, axis=1))
    np.save("./data/standard_questions_len", standard_questions_encoder_len)


encode_standard_question(sentence_transformer_select,pretrained_model)
# if __name__ == '__main__':
#     encode_standard_question(True)
