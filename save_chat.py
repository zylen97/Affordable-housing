#!/usr/bin/env python3
"""
自动保存聊天记录工具
使用方法：python save_chat.py [主题名称]
"""

import os
import sys
from datetime import date

def save_chat_record(topic="聊天记录"):
    """保存聊天记录到当前目录，文件名自动加上日期"""
    today = date.today().strftime("%Y-%m-%d")
    filename = f"{topic}_{today}.md"
    
    print(f"请在下方粘贴聊天记录内容，输入'END'结束：")
    print("-" * 50)
    
    content_lines = []
    while True:
        try:
            line = input()
            if line.strip() == "END":
                break
            content_lines.append(line)
        except KeyboardInterrupt:
            print("\n操作已取消")
            return
    
    content = "\n".join(content_lines)
    
    # 保存到文件
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"# {topic}\n")
        f.write(f"**日期**: {today}\n\n")
        f.write(content)
    
    print(f"\n聊天记录已保存到: {os.getcwd()}/{filename}")

if __name__ == "__main__":
    topic = sys.argv[1] if len(sys.argv) > 1 else "聊天记录"
    save_chat_record(topic)