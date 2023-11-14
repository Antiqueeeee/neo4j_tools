
def open_connection():
    from config import username,password,uri
    from py2neo import Graph
    graph = Graph(uri, auth=(username, password))
    return graph

