import gradio as gr
from src.outline_generator import generate_outline_gr
from src.ppt_generator import generate_ppt_gr

with gr.Blocks() as demo:
    gr.Markdown("PPT制作器")
    with gr.Row():
        with gr.Column():
            theme = gr.Dropdown(label="选择PPT模板",choices=["purple-modern","blue-line"],value="purple-modern")
        with gr.Column():
            image_source = gr.Dropdown(label="图片来源",choices=["openai","pexels","sdxl","flux"],value="openai")
        with gr.Column():
            chapter_counts = gr.Number(label="章节数",value=3,precision=0)
        with gr.Column():
            keynote_counts = gr.Number(label="每章节要点数",value=3,precision=0)
    with gr.Row():
        with gr.Column():
            ppt_prompt = gr.Text(label="PPT内容提示语",placeholder="请输入用于生成PPT的内容的提示语")
    outline_gen_btn = gr.Button("生成大纲")
    with gr.Row():
        with gr.Column():
            ppt_outline = gr.TextArea(label="PPT大纲",lines=10)
    outline_gen_btn.click(generate_outline_gr,[ppt_prompt,chapter_counts,keynote_counts],ppt_outline)
    ppt_gen_btn = gr.Button("生成PPT")
    with gr.Row():
        with gr.Column():
            ppt_file = gr.File(label="生成的PPT文件")
    ppt_gen_btn.click(generate_ppt_gr,[ppt_outline,theme,image_source],ppt_file)

    gr.Examples(
        examples=[
            [
                "purple-modern",
                "sdxl",
                3,
                3,
                "太阳系简介"
            ],
            [
                "blue-line",
                "pexels",
                3,
                3,
                "海洋环境保护"
            ],
            [
                "purple-modern",
                "flux",
                2,
                4,
                "介绍中国的历史"
            ],
            [
                "blue-line",
                "openai",
                2,
                3,
                "新能源汽车"
            ],            
        ],
        inputs=[
            theme,
            image_source,
            chapter_counts,
            keynote_counts,
            ppt_prompt
        ],
        label="😺 Examples 😺",
    )

demo.launch(server_name="127.0.0.1", server_port=7860)
