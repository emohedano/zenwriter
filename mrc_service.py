import sqlite3
conn = sqlite3.connect('/Users/mohedano/mcr30.sqlite')

WORD_TYPES = {
    'n': 'n.',
    'v': 'v.',
    'a': 'adj.',
    'r': 'adv.'
}


class MRCModel():

    def __init__(self, lang, iliId, localId, word, wordType, score, sense, gloss):

        self.lang = lang
        self.iliId = iliId
        self.localId = localId
        self.word = word
        self.type = WORD_TYPES[wordType]
        self.sense = sense
        self.score = score
        self.gloss = gloss if gloss != 'None' else None
        self.examples = []
        self.synonyms = []

    def fetchEngDefinition(self):

        c = conn.cursor()

        if self.gloss:
            return

        query = """
            select syn.gloss
            from "wei_eng-30_variant" var
            inner join "wei_eng-30_synset" syn
                on syn.offset = var.offset
            inner join "wei_eng-30_to_ili" ili
                on ili.offset = syn.offset
            where ili.iliOffset = ?
        """
        
        results = c.execute(query, (self.iliId,))

        glosses = results.fetchone()

        if glosses:
            self.gloss = glosses[0]

    def fetchSynonyms(self):

        c = conn.cursor()

        query = """
            select word
            from "wei_spa-30_variant" var
            where offset = ?
        """
        
        results = c.execute(query, (self.localId,))

        self.synonyms = [ i[0] for  i in results.fetchall() ]

    def fetchExamples(self):

        c = conn.cursor()

        if self.examples:
            return

        query = """
            select examples from "wei_{0}-30_examples" exa
            where exa.offset = ?;
        """.format(self.lang)
        
        results = c.execute(query, (self.localId,))

        results = [ i[0] for  i in results.fetchall()]
        self.examples = results

class MRCService:

    @staticmethod
    def find_synonyms(_word):

        word = _word.lower()
        data = []
        c = conn.cursor()

        query = """
            select 'spa', ili.iliOffset, var.offset, var.word, var.pos, 100, var.sense, syn.gloss
            from "wei_spa-30_variant" var
            inner join "wei_spa-30_synset" syn
                on syn.offset = var.offset
            inner join "wei_spa-30_to_ili" ili
                on ili.offset = syn.offset
            where var.word = ?
        """

        results = c.execute(query, (word,))
        
        for row in results:

            model = MRCModel(row[0], row[1], row[2], row[3],
                             row[4], row[5], row[6], row[7])

            model.fetchEngDefinition()
            model.fetchSynonyms()
            model.fetchExamples()
            
            data.append(model)

        return data

