
        c = conn.cursor()

        results = c.execute("""
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
                and rel.sourceSynset in (select offset from "wei_spa-30_variant" where word = 'oscuro')

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
                            select offset from "wei_spa-30_variant" where word = 'oscuro'
                        )
                    )
                ) 
            ) order by lang desc, csco desc, sense desc;
        """)

        data = []

        for row in results:
            
            data.append({
                'lang', row[0]
                'iliId', row[1],
                'localId', row[2],
                'word', row[3],
                'type', row[4],
                'score', row[5],
                'gloss', row[6]
            })

        return data