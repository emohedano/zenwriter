import sqlite3
conn = sqlite3.connect('./data/quotesdb.sqlite')

class Quote():

    def __init__(self, author, text, lang):

        self.author = author
        self.text = text
        self.lang = lang

class QuotesService:

    @staticmethod
    def getRandomQuote(lang = 'es'):

        c = conn.cursor()

        query = """
            SELECT * FROM quotes WHERE _id IN (
                SELECT _id FROM quotes
                where lang = ?
                ORDER BY RANDOM() LIMIT 1
            )
        """

        results = c.execute(query, (lang,))
        
        quote = results.fetchone()

        if quote:
            return Quote(quote[1], quote[2], quote[3])
        
        return Quote('Eduardo Mohedano', 'Hi, welcome to Zenwriter', 'en')