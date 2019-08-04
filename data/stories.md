## greet_part
* greet
   - utter_greet
   - utter_ask_need_help
> greet_part

## qa_happy_1
> greet_part
* faq
   - action_get_answer
* affirm
   - utter_ask_need_more_help
* deny 
   - utter_goodbye
   - export
   - action_restart

## bye
* goodbye
   - utter_goodbye
   - export
   - action_restart

## qa_happy_2
> greet_part
* faq
   - action_get_answer
* affirm
   - utter_ask_need_more_help
* faq
   - action_get_answer
* affirm
   - utter_ask_need_more_help
* deny 
   - utter_goodbye
   - export
   - action_restart

## qa_happy_3
* faq
   - action_get_answer
* affirm
   - utter_ask_need_more_help
* deny 
   - utter_goodbye
   - export
   - action_restart

## qa_bad_1
> greet_part
* faq
   - action_get_answer
* deny
   - utter_sorry
