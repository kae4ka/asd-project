# method 4 
class KWICListener:
    def on_keyword_found(self, position, context):
        print(f"Position {position}: ...{' '.join(context)}...")

class KWICEvent:
    def __init__(self, text, keyword, listener):
        self.text = text
        self.keyword = keyword.lower()
        self.listener = listener

    def process(self):
        words = self.text.split()
        for i, word in enumerate(words):
            if word.lower() == self.keyword:
                context = words[max(i-num_words , 0):min(i+num_words, len(words))]
                self.listener.on_keyword_found(i, context)

# Event-driven execution
text = """Python is a high-level, general-purpose programming language.
        Its design philosophy emphasizes code readability with the use of significant indentation.
        Python is dynamically typed and garbage-collected.
        It supports multiple programming paradigms, including structured (particularly procedural),
        object-oriented and functional programming.
        It is often described as a batteries include language due to its comprehensive standard library.
        Guido van Rossum began working on Python in the late 1980s as a successor to the ABC programming language
        and first released it in 1991 as Python 0.9.0.
        Python 2.0 was released in 2000. Python 3.0, released in 2008, was a major revision not completely backward-compatible
        with earlier versions. Python 2.7.18, released in 2020, was the last release of Python 2.
        Python consistently ranks as one of the most popular programming languages,
        and has gained widespread use in the machine learning community."""
keyword = "python"
num_words = 4
listener = KWICListener()
event = KWICEvent(text, keyword, listener)
event.process()
