import sqlite3
conn = sqlite3.connect('/Users/mohedano/mcr30.sqlite')

WORD_TYPES = {
    'n' : 'n.',
    'v' : 'v.',
    'a' : 'adj.',
    'r' : 'adv.'
}

class MRCModel():

    def __init__(self, lang, iliId, localId, word, word_type, score, sense, gloss):

        self.lang = lang
        self.iliId = iliId
        self.localId = localId
        self.word = word
        self.type = WORD_TYPES[word_type]
        self.sense = sense
        self.score = score
        self.gloss = gloss
        self.examples = []

class MRCService:

    @staticmethod
    def find_synonyms(word):

        data = []
        c = conn.cursor()

        query = ("""
            select * from (
                select 'spa' as 'lang', ili2.iliOffset, var.offset, var.word, var.pos, var.csco, var.sense, syn.gloss
                from "wei_spa-30_relation" rel
                inner join "wei_relations" r
                on r.id = rel.relation
                inner join "wei_spa-30_variant" var
                on var.offset = rel.targetSynset
                inner join "wei_spa-30_synset" syn
                on syn.offset = var.offset
                inner join "wei_spa-30_to_ili" ili
                on ili.offset = var.offset
                inner join "wei_spa-30_to_ili" ili2
                on ili2.offset = rel.sourceSynset
                where r.name = 'near_synonym'
                and rel.sourcePos = rel.targetPos
                and rel.sourceSynset in (select offset from "wei_spa-30_variant" where word = ?)

                union

                select 'eng' as 'lang', ili2.iliOffset, var.offset, var.word, var.pos, var.csco, var.sense, syn.gloss
                from "wei_eng-30_relation" rel
                inner join "wei_relations" r
                on r.id = rel.relation
                inner join "wei_eng-30_variant" var
                on var.offset = rel.targetSynset
                inner join "wei_eng-30_synset" syn
                on syn.offset = var.offset
                inner join "wei_eng-30_to_ili" ili
                on ili.offset = var.offset
                inner join "wei_eng-30_to_ili" ili2
                on ili2.offset = rel.sourceSynset
                where r.name = 'near_synonym'
                and rel.sourcePos = rel.targetPos
                and rel.sourceSynset in (
                    select offset from "wei_eng-30_to_ili" where iliOffset in (
                        select iliOffset from "wei_spa-30_to_ili" where offset in(
                            select offset from "wei_spa-30_variant" where word = ?
                        )
                    )
                ) 
            ) order by lang desc, csco desc, sense desc;
        """)

        results = c.execute(query, (word, word))

        for row in results:
            
            model = MRCModel( row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7] )
            data.append(model)

        return data