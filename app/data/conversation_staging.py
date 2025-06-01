import difflib

def word_similarity(a, b, threshold=0.85):

    ratio = difflib.SequenceMatcher(None, a.lower(), b.lower()).ratio()
    return ratio >= threshold


def find_closest_match(input_str, options, threshold=0.85):

    input_str = input_str.strip()


    if input_str.isdigit():
        index = int(input_str) - 1
        if 0 <= index < len(options):
            return options[index]

    best_match = None
    best_score = 0
    for option in options:
        score = difflib.SequenceMatcher(None, input_str.lower(), option.lower()).ratio()
        if score > best_score:
            best_score = score
            best_match = option

    if best_score >= threshold:
        return best_match
    return None
