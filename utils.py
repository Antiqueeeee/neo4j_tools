
def open_connection():
    from config import username,password,uri
    from py2neo import Graph
    graph = Graph(uri, auth=(username, password))
    return graph

def text_input_properties_to_dict(properties):
    _property = dict()
    properties = properties.replace(":","：")
    properties = properties.split("\n")
    for prop in properties:
        if len(prop):
            key,value = prop.split("：")
            _property[key] = value
    return _property