from .intent_classifier import IntentClassifier

intent_classifier = IntentClassifier()

def is_correct(
    user_input: str,
    intent: str | None = None,
    classifier: IntentClassifier | None = None,
) -> bool:
    r"""Checks for the user input to not be OUT_OF_SCOPE
    """
    if intent is None:
        if classifier is None:
            classifier = intent_classifier
        intent = classifier.classify(user_input)
    return intent != "OUT_OF_SCOPE"