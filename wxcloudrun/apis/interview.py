from wxcloudrun.utils.doubao import client
import requests
from werkzeug.utils import secure_filename
import os
import uuid
from flask import request, jsonify
import base64
import tempfile


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


def process_audio():
    try:
        # 获取前端发送的base64编码的音频数据
        audio_base64 = request.json.get('audio')
        
        if not audio_base64:
            return jsonify({'success': False, 'error': 'No audio data received'}), 400

        # 解码base64数据
        audio_data = base64.b64decode(audio_base64)

        # 创建临时文件来保存音频数据
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_audio:
            temp_audio.write(audio_data)
            temp_audio_path = temp_audio.name

        # 使用speech_recognition库来识别音频

        # 删除临时文件
        os.unlink(temp_audio_path)

        # 返回识别结果
        return jsonify({
            'success': True,
            'transcription': "test"
        })

    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500


