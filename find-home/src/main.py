from SPARQLWrapper import SPARQLWrapper, JSON

sparql_endpoint = "http://landregistry.data.gov.uk/landregistry/query"
sparql = SPARQLWrapper(sparql_endpoint)

def count_transactions_by_town(town_name):
    sparql.setQuery(
        f"""
        PREFIX lrppi: <http://landregistry.data.gov.uk/def/ppi/>
        PREFIX lrcommon: <http://landregistry.data.gov.uk/def/common/>
        
        SELECT (COUNT(?transx) AS ?count)
        WHERE {{
            ?transx lrppi:propertyAddress ?addr .
            ?addr lrcommon:town ?town .
            FILTER(?town = "{town_name}")
        }}
        """
    )
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    return(results["results"]["bindings"][0]["count"]["value"])


def base_query():
     
    sparql.setQuery(
        """
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX lrppi: <http://landregistry.data.gov.uk/def/ppi/>
        PREFIX lrcommon: <http://landregistry.data.gov.uk/def/common/>
        
        SELECT (COUNT(?transx) AS ?count)
        # SELECT ?paon ?saon ?street ?town ?county ?postcode ?amount ?date
        WHERE {
            ?transx lrppi:pricePaid ?amount .
            ?transx lrppi:transactionDate ?date .
            ?transx lrppi:propertyAddress ?addr .
            ?addr lrcommon:postcode ?postcode .
            ?addr lrcommon:county ?county .
            ?addr lrcommon:paon ?paon .
            ?addr lrcommon:saon ?saon .
            ?addr lrcommon:street ?street .
            ?addr lrcommon:town ?town .
            FILTER(?town = "LONDON")
        }
        # LIMIT 10
        """
    )
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    yield results["results"]["bindings"]

def main():
    print(count_transactions_by_town("LONDON"))
    
if __name__ == "__main__":
    main()