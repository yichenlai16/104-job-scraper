# 104-job-scraper

Web scraping with scrapy for job vacancies from 104人力銀行

這個專案使用Scrapy框架爬取104人力銀行的職缺資訊，並將資料存入Elasticsearch中。爬蟲使用104的搜尋API來取得職缺資訊，由於API限制，僅能取得前150頁的資料。

Elasticsearch 含IK 分詞器並用OpenCC轉成繁體中文。

開始使用

1. 請確認 `.env` 檔案的內容是否正確設置。
    
2. 執行指令以啟動專案：
    
    `docker-compose -f "docker-compose.yml" up -d --build`
    
3. Elasticsearch 伺服器運行在 [http://localhost:9200](http://localhost:9200)
