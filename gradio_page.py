import gradio
from utils import open_connection,text_input_properties_to_dict
from py2neo import Node,Relationship,NodeMatcher,RelationshipMatcher

graph = open_connection()



# 添加
def button_function_create_entity(new_entity_type,new_entity_properties):
    node_matcher = NodeMatcher(graph)
    _property = text_input_properties_to_dict(new_entity_properties)
    nodes = node_matcher.match(new_entity_type).where(**_property)
    if not len(nodes):
        node = Node(new_entity_type,**_property)
        graph.create(node)
    return node_matcher.match(new_entity_type).where(**_property).first()

def button_function_create_relation(
        head_entity_type,head_entity_properties
        ,tail_entity_type,tail_entity_properties
        ,relation
):
    relation_matcher = RelationshipMatcher(graph)
    head_entity = button_function_create_entity(head_entity_type,head_entity_properties)
    tail_entity = button_function_create_entity(tail_entity_type,tail_entity_properties)
    if not relation_matcher.match((head_entity,tail_entity), r_type=relation) and not relation_matcher.match((tail_entity,head_entity), r_type=relation):
        relationship = Relationship(head_entity, relation, tail_entity)
        graph.create(relationship)
    return list(relation_matcher.match((head_entity,tail_entity), r_type=relation)) + list(relation_matcher.match((tail_entity,head_entity), r_type=relation))
# 删除
def button_function_delete_entity(entity_type,entity_properites):
    node_matcher = NodeMatcher(graph)
    relation_matcher = RelationshipMatcher(graph)
    _property = text_input_properties_to_dict(entity_properites)
    nodes = node_matcher.match(entity_type).where(**_property)
    for node in nodes:
        relationships = relation_matcher.match([node],r_type=None)
        for relationship in relationships:
            graph.delete(relationship)
        graph.delete(node)
def button_function_delete_relation(head_entity_type,head_entity_properties,tail_entity_type,tail_entity_properites,relation=None):
    node_matcher = NodeMatcher(graph)
    relation_matcher = RelationshipMatcher(graph)
    _property = text_input_properties_to_dict(head_entity_properties)
    head_entity = node_matcher.match(head_entity_type).where(**_property).first()
    _property = text_input_properties_to_dict(tail_entity_properites)
    tail_entity = node_matcher.match(tail_entity_type).where(**_property).first()
    relationships = relation_matcher.match((head_entity,tail_entity),r_type=relation)
    for relationship in relationships:
        graph.separate(relationship)
    relationships = relation_matcher.match((tail_entity,head_entity),r_type=relation)
    for relationship in relationships:
        graph.separate(relationship)
def button_function_delete_spo(head_entity_type,head_entity_properites,tail_entity_type,tail_entity_properites):
    node_matcher = NodeMatcher(graph)
    relation_matcher = RelationshipMatcher(graph)
    _property = text_input_properties_to_dict(head_entity_properites)
    head_entity = node_matcher.match(head_entity_type).where(**_property).first()
    _property = text_input_properties_to_dict(tail_entity_properites)
    tail_entity = node_matcher.match(tail_entity_type).where(**_property).first()
    relationships = relation_matcher.match((head_entity,tail_entity),r_type=None)
    for relationship in relationships:
        graph.delete(relationship)
    relationships = relation_matcher.match((tail_entity,head_entity),r_type=None)
    for relationship in relationships:
        graph.delete(relationship)
# button_function_create_relation("痤疮","疾病","胃炎","疾病","别名")
# button_function_create_relation("痤疮","疾病","胃炎","疾病","名别")
# button_function_create_relation("痤疮","疾病","胃炎","疾病","吃饭")

# 修改
def button_function_update_entity(entity_name,entity_type,new_name,new_type):
    pass

with gradio.Blocks() as demo:
    with gradio.Tab("增加"):
        gradio.Markdown("操作实体")
        with gradio.Row():
            text_input_entity_type = gradio.Text(label="实体类型")
            text_input_entity_property = gradio.TextArea(label="实体属性",value="name：")
            button_apply = gradio.Button("添加")
            button_apply.click(
                button_function_create_entity
                ,inputs=[
                    text_input_entity_type
                    ,text_input_entity_property
                ]
                ,outputs=None
            )
        gradio.Markdown("操作三元组")
        with gradio.Row():
            with gradio.Column():
                text_input_entity_1_type = gradio.Text(label="实体1类型")
                text_input_entity_1_properties = gradio.TextArea(label="实体1属性",value="name：")
            with gradio.Column():
                text_input_entity_2_type = gradio.Text(label="实体2类型")
                text_input_entity_2_properties = gradio.TextArea(label="实体2属性",value="name：")
        with gradio.Row():
            text_input_relation = gradio.Text(label="关系")
            button_apply = gradio.Button("添加")
            button_apply.click(
                button_function_create_relation
                ,inputs=[
                    text_input_entity_1_type,text_input_entity_1_properties
                    ,text_input_entity_2_type,text_input_entity_2_properties
                    ,text_input_relation
                ]
                ,outputs=None
            )
    with gradio.Tab("删除"):
        gradio.Markdown("操作实体")
        with gradio.Row():
            text_input_entity_type = gradio.Text(label="实体名称")
            text_input_entity_properites = gradio.TextArea(label="实体属性",value="name：")
            # text_input_entity_property = gradio.TextArea(label="实体属性")
            button_apply = gradio.Button("删除")
            button_apply.click(button_function_delete_entity,inputs=[text_input_entity_type,text_input_entity_properites],outputs=None)
        gradio.Markdown("操作关系")
        with gradio.Row():
            with gradio.Column():
                text_input_entity_1_type = gradio.Text(label="实体1类型")
                text_input_entity_1_properties = gradio.TextArea(label="实体1属性",value="name：")
            with gradio.Column():
                text_input_entity_2_type = gradio.Text(label="实体2类型")
                text_input_entity_2_properties = gradio.TextArea(label="实体2属性",value="name：")
        with gradio.Row():
            text_input_relation = gradio.Text(label="关系")
            button_apply = gradio.Button("删除")
            button_apply.click(
                button_function_delete_relation
                ,inputs=[text_input_entity_1_type,text_input_entity_1_properties,text_input_entity_2_type,text_input_entity_2_properties]
                ,outputs=None
            )
        gradio.Markdown("操作三元组")
        with gradio.Row():
            text_input_entity_1_name = gradio.Text(label="头实体名称")
            text_input_entity_1_type = gradio.Text(label="头实体类型")
        with gradio.Row():
            text_input_entity_2_name = gradio.Text(label="尾实体名称")
            text_input_entity_2_type = gradio.Text(label="尾实体类型")
        with gradio.Row():
            button_apply = gradio.Button("删除")
            button_apply.click(
                button_function_delete_spo
                ,inputs=[text_input_entity_1_name,text_input_entity_1_type,text_input_entity_2_name,text_input_entity_2_type]
                ,outputs=None
            )
    with gradio.Tab("修改"):
        pass


app,local_url,share_url = demo.launch()
# demo.queue().launch(share=True,server_name='0.0.0.0',server_port=7475,show_error=True)