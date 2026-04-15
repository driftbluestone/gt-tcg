import re

text_replace = {
    "_":"underscore",
    "/":"slash",
    ".":"period",
    "-":"dash",
    ",":"comma",
    "+":"plus",
    "*":"star",
    ")":"close_paren",
    "(":"open_paren",
    "'":"apostrophe",
    "&":"and",
    "%":"percent",
    "$":"dollar",
    "#":"hashtag",
    "\"":"quote",
    "!":"exclamation",
    "~":"tilde",
    "}":"close_curly",
    "{":"open_curly",
    "`":"backtick",
    "^":"carat",
    "]":"close_square",
    "[":"open_square",
    "\\":"backslash",
    "@":"at",
    "?":"question",
    ">":"greater_than",
    "=":"equal",
    "<":"less_than",
    ";":"semicolon",
    ":":"colon",
    "|":"pipe"
}
text_replace = str.maketrans(text_replace)
text = "test tes;'t test\n\ntest tEADest  test\nthe testing is comencing"

# re.sub(r"([a-z])", r"\g<1>2", word).translate(text_replace)
text = [[[re.sub(r"([a-z])", r"\g<1>2", character).translate(text_replace) for character in list(word)] for word in letter] for letter in [word.split(" ") for word in text.split("\n")]]
print(text)