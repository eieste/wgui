# -*- coding: utf-8 -*-
def get_char(name, ii=0):
    for _ in range(ii, len(name)):
        if name[_].isalpha():
            return _ + 1, name[_]
    return -1, ""


def get_initial_sign(email: str):
    email = email.lower()
    first = ""
    second = ""
    user = email.split("@")[0]
    dotted = user.split(".")
    minused = user.split("-")
    if (len(dotted) > 1):
        _, first = get_char(dotted[0])
        _, second = get_char(dotted[1])
    elif (len(minused) > 1):
        _, first = get_char(minused[0])
        _, second = get_char(minused[1])
    else:
        _, first = get_char(user)
        _, second = get_char(user, _)

    return f"{first}{second}"
