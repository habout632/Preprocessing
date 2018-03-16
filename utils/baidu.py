import json

from aip import AipNlp

""" 你的 APPID AK SK """
APP_ID = '10935871'
API_KEY = '7WuyX2n4OLSsmGFqnWtGjrRB'
SECRET_KEY = 'qF1aGllUhmgrmcxrNiOEpNSPfEbGYcpx'

client = AipNlp(APP_ID, API_KEY, SECRET_KEY)


def get_lexical_result(text):
    """ 调用词法分析 """
    result = client.lexer(text)
    items = result.get("items")
    print(items)
    words = []
    if items:
        for item in items:
            word = item.get("item")
            pos = item.get("pos")
            ne = item.get("ne")
            basic_words = item.get("basic_words")
            if pos in ["n", "nr","v","vn","nz","ns","s","nt","nw"] or ne in ["PER", "LOC", "ORG"]:
                words.append(word)

            # print(basic_words)
    return list(set(words))

# get_lexical_result("震惊，华为拍照效果居然这么好 华为p9品质黑白照，分分钟get！")

# word = "日本"

# """ 调用词向量表示 """
# vector = client.wordEmbedding(word)
# print(vector)

# word1 = "跑酷"
#
# word2 = "极限运动"
#
# """ 调用词义相似度 """
# similarity = client.wordSimEmbedding(word1, word2)
# print(similarity)
#
# """ 如果有可选参数 """
# options = {}
# options["mode"] = 0
#
# """ 带参数调用词义相似度 """
# client.wordSimEmbedding(word1, word2, options)


# title = "在白云和岩石间自由飞行"
#
# content = "在白云和岩石间自由飞行，翼装飞行精选视频。"
#
# """ 调用文本标签 """
# tags = client.keyword(title, content)
# print(tags)

text = "嗅觉失灵的时间越长，神经的破坏也越彻底，恢复的机会也就渺茫了。所以一旦出现嗅觉失灵，最好尽快就医，找出病因，药物治疗细菌感染或是解决鼻塞症状，恢复鼻腔通气，或许有机会恢复嗅觉。"


def get_segmented_words(text):
    """
    调用词法分析
    """
    result = client.lexer(text)
    words = [item.get("item") for item in result.get("items")]
    # print(words)
    return words


if __name__ == "__main__":
    get_segmented_words(text)