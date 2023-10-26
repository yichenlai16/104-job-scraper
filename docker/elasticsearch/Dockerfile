# 使用 Elasticsearch 官方映像檔
FROM docker.elastic.co/elasticsearch/elasticsearch:8.9.0

# 安裝 Elasticsearch IK 插件
# Elatsicsearch & IK 兩者版本需一致
RUN elasticsearch-plugin install --batch https://github.com/medcl/elasticsearch-analysis-ik/releases/download/v8.9.0/elasticsearch-analysis-ik-8.9.0.zip

USER root

# 更新套件庫並安裝 OpenCC
# 移除 APT 暫存檔案
RUN apt-get update && apt-get install -y opencc && rm -rf /var/lib/apt/lists/*


# 移動到 Elasticsearch 的配置目錄
WORKDIR /usr/share/elasticsearch/config/analysis-ik

# 使用 OpenCC 將所有 *.dic 檔案轉換為台灣繁體
RUN for file in *.dic; do \
    opencc -c /usr/share/opencc/s2twp.json -i "$file" -o "/tmp/${file%.*}-tw.dic"; \
    done

# 複製所有 *.dic 到 /tmp
RUN cp *.dic /tmp/

# 合併所有 *-tw.dic 和相應的 *-cn.dic，排序並去除重複行，最後複製到 main.dic
RUN for file_tw in /tmp/*-tw.dic; do \
    file_cn="/tmp/$(basename "$file_tw" "-tw.dic")-cn.dic"; \
    cat "$file_tw" "$file_cn" | sort | uniq > "/usr/share/elasticsearch/config/analysis-ik/$(basename "$file_tw" "-tw.dic").dic"; \
    done

RUN rm -rf /tmp/*.dic

USER elasticsearch