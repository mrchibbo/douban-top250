import requests
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
import time

# 爬取函数：获取豆瓣 Top250 书籍信息
def fetch_douban_books():
    books = []
    base_url = "https://book.douban.com/top250?start={}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    
    # 遍历每一页
    for page in range(0, 250, 25):
        url = base_url.format(page)
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        # 获取每本书的信息
        for book in soup.find_all('tr', class_='item'):
            # 书名
            title = book.find('div', class_='pl2').find('a').get_text(strip=True)
            
            # 作者信息
            info = book.find('p', class_='pl').get_text(strip=True)
            
            # 评分
            rating = book.find('span', class_='rating_nums').get_text(strip=True)
            
            # 评论数
            comments = book.find('span', class_='pl').get_text(strip=True)
            comments = comments.replace('(', '').replace(')', '').replace('人评价', '').strip()
            
            # 简评（若有）
            quote_tag = book.find('span', class_='inq')
            quote = quote_tag.get_text(strip=True) if quote_tag else "无"

            # 添加到列表
            books.append([title, info, rating, comments, quote])
        
        # 延时，避免请求过快
        time.sleep(1)
    
    # 转换为 DataFrame
    df = pd.DataFrame(books, columns=["书名", "作者", "评分", "评论数", "简评"])
    return df

# Streamlit 应用界面
st.title("豆瓣读书 Top250 爬取展示")
st.write("点击下方按钮获取豆瓣读书 Top250 的书籍信息，包括书名、作者、评分、评论数和简评。")

# 按钮触发爬取
if st.button("获取豆瓣读书 Top250 书籍信息"):
    with st.spinner("正在爬取数据，请稍候..."):
        data = fetch_douban_books()
    st.success("数据爬取完成！")
    st.write(data)

    # 保存为 CSV 的下载选项
    csv = data.to_csv(index=False, encoding='utf-8-sig')
    st.download_button(
        label="下载数据为 CSV 文件",
        data=csv,
        file_name="douban_books_top250.csv",
        mime="text/csv"
    )

