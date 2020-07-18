from py2neo import Graph
from neo4j import GraphDatabase

class Neo4jCreation:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.graph = Graph(uri, auth=(user, password))
        self.setConstraint()

    def setConstraint(self): #item and costumer name should be unique
        self.graph.run("CREATE CONSTRAINT ON ( item:Item ) ASSERT (item.name) IS UNIQUE")
        self.graph.run("CREATE CONSTRAINT ON ( cost:Cost ) ASSERT (cost.name) IS UNIQUE")
    def close(self):
        self.driver.close()

    def pandasImport(self, df):

        print(str)
        for index, row in df.iterrows():
            nodeCostExistence = True
            nodeItemExistence = True

            tmpQuery = self.graph.run("match (a:Costumer{name:'%s'}) return a.name"%(row['userID'])).evaluate()
            if tmpQuery==None:
                nodeCostExistence = False
            tmpQuery = self.graph.run("match (a:Item{name:'%s'}) return a.name"%(row['itemID'])).evaluate()
            if tmpQuery==None:
                nodeItemExistence = False

            if nodeItemExistence and not nodeCostExistence:
                addQuery = self.graph.run("CREATE (cost:Costumer {name: '%s'})"%(row['userID'])).data()
            elif not nodeCostExistence and not nodeItemExistence:
                addQuery = self.graph.run("CREATE (cost:Costumer {name: '%s'})" % (row['userID'])).data()
                addQuery = self.graph.run("CREATE (item:Item {name: '%s'})" % (row['itemID'])).data()

            addQuery = self.graph.run("MATCH (a:Costumer {name:'%s'}), (b:Item {name:'%s'})"
                                      " MERGE (a)-[r:used {rate: %d}]->(b) return *" % (
                                      row['userID'], row['itemID'], row['rating'])).data()
            print(addQuery)

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]


