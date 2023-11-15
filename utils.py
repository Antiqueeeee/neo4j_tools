def open_connection():
    from config import username,password,uri
    from py2neo import Graph
    graph = Graph(uri, auth=(username, password))
    return graph

from py2neo import Node,Relationship,NodeMatcher,RelationshipMatcher
graph = open_connection()
def text_input_properties_to_dict(properties):
    _property = dict()
    properties = properties.replace(":","：")
    properties = properties.split("\n")
    for prop in properties:
        if len(prop):
            key,value = prop.split("：")
            _property[key] = value
    return _property

#
#查询
#
def button_function_search_entity(entity_type,entity_properties):
    node_matcher = NodeMatcher(graph)
    _property = text_input_properties_to_dict(entity_properties)
    nodes = node_matcher.match(entity_type).where(**_property)
    if not nodes:
        return None
    else:
        return nodes.first()
    
        

#
# 添加
#
def button_function_create_entity(new_entity_type,new_entity_properties):
    nodes = button_function_search_entity(new_entity_type,new_entity_properties)
    if not nodes:
        _property = text_input_properties_to_dict(new_entity_properties)
        node = Node(new_entity_type,**_property)
        graph.create(node)
    return button_function_search_entity(new_entity_type,new_entity_properties)

def button_function_create_relation(
        head_entity_type,head_entity_properties
        ,tail_entity_type,tail_entity_properties
        ,relation,relation_properties
):
    relation_matcher = RelationshipMatcher(graph)
    head_entity = button_function_create_entity(head_entity_type,head_entity_properties)
    tail_entity = button_function_create_entity(tail_entity_type,tail_entity_properties)
    _property = text_input_properties_to_dict(relation_properties)
    if not relation_matcher.match((head_entity,tail_entity), r_type=relation,**_property) and not relation_matcher.match((tail_entity,head_entity), r_type=relation):
        relationship = Relationship(head_entity, relation, tail_entity,**_property)
        graph.create(relationship)
    return list(relation_matcher.match((head_entity,tail_entity), r_type=relation)) + list(relation_matcher.match((tail_entity,head_entity), r_type=relation))
# 
# 删除
#
def button_function_delete_entity(entity_type,entity_properites):
    relation_matcher = RelationshipMatcher(graph)
    nodes = button_function_create_entity(entity_type,entity_properites)
    for node in nodes:
        # 接触与该节点相关的所有关系
        # 然后删除该节点
        relationships = relation_matcher.match([node],r_type=None)
        for relationship in relationships:
            graph.separate(relationship)
        graph.delete(node)
def button_function_delete_relation(
        head_entity_type,head_entity_properties
        ,tail_entity_type,tail_entity_properites
        ,relation=None,relation_properties=""
):
    relation_matcher = RelationshipMatcher(graph)

    head_entity = button_function_create_entity(head_entity_type,head_entity_properties)
    tail_entity = button_function_create_entity(tail_entity_type,tail_entity_properites)
    _property = text_input_properties_to_dict(relation_properties)
    relationships = relation_matcher.match((head_entity,tail_entity),r_type=relation,**_property)
    for relationship in relationships:
        graph.separate(relationship)
    relationships = relation_matcher.match((tail_entity,head_entity),r_type=relation,**_property)
    for relationship in relationships:
        graph.separate(relationship)
def button_function_delete_spo(
        head_entity_type,head_entity_properites
        ,tail_entity_type,tail_entity_properites
        ,text_input_relation=None,text_input_relation_properties=""
):
    relation_matcher = RelationshipMatcher(graph)
    head_entity = button_function_create_entity(head_entity_type,head_entity_properites)
    tail_entity = button_function_create_entity(tail_entity_type,tail_entity_properites)
    # 考虑两个方向
    _property = text_input_properties_to_dict(text_input_relation_properties)
    relationships = relation_matcher.match((head_entity,tail_entity),r_type=text_input_relation,**_property)
    for relationship in relationships:
        graph.delete(relationship)
    relationships = relation_matcher.match((tail_entity,head_entity),r_type=text_input_relation,**_property)
    for relationship in relationships:
        graph.delete(relationship)

# 修改
def button_function_update_entity(
                entity_type,entity_properties
                ,new_type,new_properties
):
    pass