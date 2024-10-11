from wxcloudrun.utils.doubao import client
import requests
from werkzeug.utils import secure_filename
import os
import uuid
from flask import request, jsonify


def get_question():
    data = request.json
    resume = data.get('resume', '')
    questions = data.get('questions', [])
    answers = data.get('answers', [])

    # 构建提示词
    prompt = f"你是一位专业的面试官。根据以下简历信息进行面试:\n\n{resume}\n\n"
    
    if questions:
        prompt += "之前的问题和回答:\n"
        for q, a in zip(questions, answers):
            prompt += f"问: {q}\n答: {a}\n"
    
    prompt += "\n请根据简历和之前的对话(如果有),生成下一个合适的面试问题。"

    # 调用豆包API
    completion = client.chat.completions.create(
    model="ep-20241008143931-s48cx",
    messages = [
        {"role": "system", "content": "你是豆包，是由字节跳动开发的 AI 人工智能助手"},
        {"role": "user", "content": prompt},
    ],
        )
    question = completion.choices[0].message.content

    return jsonify({"success": True, "question": question})


def process_audio(app):
    if 'audio' not in request.files:
        app.logger.error("No audio file in request")
        return jsonify({"success": False, "error": "No audio file"}), 400
    
    audio_file = request.files['audio']
    
    if audio_file.filename == '':
        app.logger.error("No selected file")
        return jsonify({"success": False, "error": "No selected file"}), 400
    
    if audio_file:
        filename = secure_filename(str(uuid.uuid4()) + '.mp3')
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        audio_file.save(filepath)
        
        app.logger.info(f"Audio file saved at {filepath}")
        return jsonify({"success": True, "transcription": "mp3"})


