from whoosh.index import open_dir
from whoosh.qparser import QueryParser
from whoosh.fields import Schema, TEXT, ID, STORED

def buscar_ropa_hombre(query_str):
    ix = open_dir("whoosh_index")
    with ix.searcher() as searcher:
        query = QueryParser("nombre", ix.schema).parse(query_str)
        results = searcher.search(query)
        return [hit['nombre'] for hit in results]
