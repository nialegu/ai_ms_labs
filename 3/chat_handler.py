import os
import logging
from collections import defaultdict

from nlu import classify_intent, get_answer_by_intent, get_failure_phrase
from dialogue import DialogueGenerator, check_ad_trigger

logger = logging.getLogger("handler")

_user_state = defaultdict(lambda: {
    'message_count': 0,
    'last_ad_at': 0,
})

_dialogue = None


def init_chat_system():
    global _dialogue

    base = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(base, 'data', 'dialogues.txt')

    _dialogue = DialogueGenerator(path)
    logger.info("Dialogue module initialized")


def get_response(text: str, user_id: int) -> str:
    state = _user_state[user_id]
    state['message_count'] += 1

    intent = classify_intent(text)
    answer = None

    if intent:
        answer = get_answer_by_intent(intent)

    if not answer and _dialogue:
        answer = _dialogue.generate_answer(text)

    if not answer:
        answer = get_failure_phrase()

    ad, _ = check_ad_trigger(
        text,
        intent,
        state['message_count'],
        state['last_ad_at']
    )

    if ad:
        answer += "\n\n" + ad
        state['last_ad_at'] = state['message_count']

    return answer