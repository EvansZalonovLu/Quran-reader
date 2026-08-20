# Please install OpenAI SDK first: `pip3 install openai`
import streamlit as st
import os
from openai import OpenAI
client = OpenAI(
    api_key="sk-1dd8fb865ae84deb844b2f48ca95fdde",  # 直接粘贴在这里
    base_url="https://api.deepseek.com")
FILE_PATH = "./伊斯兰教/quran-chinese.txt" # 你的文件路径


# ========== 第一步：读文件 ==========
def read_file(path):
    with open(path, 'r', encoding='utf-8') as f:
        return f.read()


# ========== 第二步：检索（关键词匹配） ==========
def search_keywords(question, content):
    """从内容里找到包含问题关键词的句子"""
    # 把内容按句子分割
    sentences = content.split('。')  # 中文按句号分
    
    # 找出包含关键词的句子
    matched = []
    for sentence in sentences:
        # 简单匹配：问题里的词出现在句子里
        for word in question:
            if word in sentence:
                matched.append(sentence)
                break
    
    return matched#[:5]  # 最多返回5句


# ========== 第三步：生成回答 ==========
def ask_deepseek(question, context):
    
    """把问题和资料发给DeepSeek"""
    prompt = f"""
请根据以下资料回答问题：

【资料】
{context}

【问题】
{question}

【要求】
- 据资料回答，按照伊斯兰教的价值观和思维方式，对经文做出解释，关联经文与问题
- 纯文本回答，不要用任何标记符号
- 不要用 ##、***、--- 等任何格式符号，更不要用表格
- 不要用 Markdown 格式
- 直接输出纯文字内容
-根据提问的语言，使用相同的回答语言
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": "详细的回答问题"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content


# ========== 主程序 ==========
def main():
    # 读文件
    print("📖 正在读取文件...")
    content = read_file(FILE_PATH)
    print(f"✅ 读取完成，共 {len(content)} 个字符")
    
    while True:
        question = input("\n 你问：")
        if question in ['退出', 'exit', 'quit']:
            break
        
        # 检索
        print("🔍 正在查找相关资料...")
        context = search_keywords(question, content)
        
        if not context:
            print("资料里没找到相关内容")
            continue
        
        # 生成回答
        print("思考中...")
        answer = ask_deepseek(question, "\n".join(context))
        print(f" 答：{answer}")


if __name__ == "__main__":
    main()

