import gradio
from utils import button_function_create_entity,button_function_create_relation 
from utils import button_function_delete_entity,button_function_delete_relation,button_function_delete_spo


# button_function_create_relation("痤疮","疾病","胃炎","疾病","别名")
# button_function_create_relation("痤疮","疾病","胃炎","疾病","名别")
# button_function_create_relation("痤疮","疾病","胃炎","疾病","吃饭")
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
            with gradio.Column():
                text_input_relation = gradio.Text(label="关系")
                text_input_relation_properties = gradio.TextArea(label="关系属性",value="name：")
        button_apply = gradio.Button("添加")
        button_apply.click(
            button_function_create_relation
            ,inputs=[
                text_input_entity_1_type,text_input_entity_1_properties
                ,text_input_entity_2_type,text_input_entity_2_properties
                ,text_input_relation,text_input_relation_properties
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
            with gradio.Column():
                text_input_relation = gradio.Text(label="关系")
                text_input_relation_properties = gradio.TextArea(label="关系属性")
            with gradio.Row():
                button_apply = gradio.Button("删除")
            button_apply.click(
                button_function_delete_relation
                ,inputs=[
                    text_input_entity_1_type,text_input_entity_1_properties
                    ,text_input_entity_2_type,text_input_entity_2_properties
                    ,text_input_relation,text_input_relation_properties
                ]
                ,outputs=None
            )
        gradio.Markdown("操作三元组")
        with gradio.Column():
            text_input_entity_1_type = gradio.Text(label="实体1类型")
            text_input_entity_1_properties = gradio.TextArea(label="实体1属性",value="name：")
        with gradio.Column():
            text_input_entity_2_name = gradio.Text(label="实体2类型")
            text_input_entity_2_type = gradio.TextArea(label="实体2属性",value="name：")
        with gradio.Column():
            text_input_relation = gradio.Text(label="关系")
            text_input_relation_properties = gradio.TextArea(label="关系属性")
        button_apply = gradio.Button("删除")
        button_apply.click(
            button_function_delete_spo
            ,inputs=[
                text_input_entity_1_type,text_input_entity_1_properties
                ,text_input_entity_2_type,text_input_entity_2_properties
                ,text_input_relation,text_input_relation_properties
            ]
            ,outputs=None
        )
    with gradio.Tab("修改"):
        pass


app,local_url,share_url = demo.launch()
# demo.queue().launch(share=True,server_name='0.0.0.0',server_port=7475,show_error=True)