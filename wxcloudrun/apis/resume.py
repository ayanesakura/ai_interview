import requests
from flask import Flask, request, jsonify
from werkzeug.utils import secure_filename
import os
from wxcloudrun.utils.file_util import load_pdf

ALLOWED_EXTENSIONS = {'pdf'}

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
           

def upload_file(dir_path):
    # 检查是否有文件部分
    if 'file' not in request.files:
        return jsonify({'success': False, 'error': '没有文件部分'}), 400
    file = request.files['file']
    
    # 如果用户没有选择文件,浏览器也会发送一个空的文件名
    if file.filename == '':
        return jsonify({'success': False, 'error': '没有选择文件'}), 400
    
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(dir_path, filename)
        file.save(file_path)
        
        # 这里应该返回一个可以通过网络访问的URL
        # print('file_url:', file_url)
        return jsonify({
            'success': True, 
            'message': '文件上传成功'
        })
    
    return jsonify({'success': False, 'error': '不允许的文件类型'}), 400


def analyze_text(client, text):
    completion = client.chat.completions.create(
    model="ep-20241008143931-s48cx",
    messages = [
        {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
        {"role": "user", "content": "这是我的简历，请帮我对简历进行评分，评分维度可以是详细程度、有无亮点等"},
        {"role": "user", "content": f"简历内容：\n{text}"},
    ],
        )
    return completion.choices[0].message.content

def analyze_resume():
    data = request.json
    if not data or 'fileUrl' not in data:
        return jsonify({'success': False, 'error': '缺少文件URL'}), 400

    file_url = data['fileUrl']
    
    try:
        # 提取PDF文本
        file_name = file_url.split('/')[-1]
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file_name)
        resume_text = load_pdf(file_path)
        
        # 调用豆包API进行分析
        # analysis_result = analyze_text(resume_text)
        analysis_result = 'None'
        
        # 假设analyze_text函数返回一个包含summary, skills, experience和education的字典
        return jsonify({
            'success': True,
            'summary': analysis_result,
            'resume': resume_text
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500