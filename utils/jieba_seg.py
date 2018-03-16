## rebooking
# rebooking = '起飞（含）前同等舱位更改需收取票面价20%的更改费，起飞后需收取票面价30%的更改费。改期费与票价差额同时发生时，两者需同时收取。'

# rebooking = '起飞前2小时（含）以外同等舱位变更按票面价收取30%变更费；2小时以内及起飞后同等舱位变更按票面价收取50%变更费。改期费与升舱费同时发生时，则需同时收取改期费和升舱差额。'
# rebooking = '航班起飞前2小时（含）之前，免费变更；航班起飞前2小时之内及航班起飞后，收取5%变更费'
# rebooking = '航班预计离站时间前2小时（含）前，免费改签；航班预计离站时间前2小时(不含)后，收取5%变更费'
# rebooking = "航班离站4小时（含）之前，免费变更，航班离站4小时内以及飞后，收取10%变更费。升舱变更时，收取原舱位票面价与适用新舱位间票价差额，同时按原舱位对应规则收取变更费。"
# rebooking = "航班预计离站时间前2小时（含）前，免费改签；航班预计离站时间前2小时(不含)后，收取5%变更费"
import jieba.analyse

# rebooking = "允许签转，如变更后承运人适用票价高于国航票价，需补齐差额后进行变更，若低于国航票价，差额不退。"
# rebooking = "临潼区银桥大道与桃园步行街交汇口（大宅门6楼）"
from app.utils.baidu import get_lexical_result
from app.utils.mongo_util import get_client, get_col

rebooking = "龙凤头海滨度假村帐篷团住宿"

## refund
# refund = '航班预计离站时间前2小时（含）前，收取5%的退票费；航班预计离站时间前2小时(不含)后，收取15%的退票费。'
refund = "航班离站4小时（含）之前，收取5%退票费，航班离站4小时内以及飞后，收取10%退票费"

# refund = "航班预计离站时间前2小时（含）前，收取5%退票费；航班预计离站时间前2小时(不含)后，收取15%退票费"
refund = '航班起飞前2小时（含）之前，免费退票；航班起飞前2小时之内及航班起飞后，收取10%退票费'
# refund = '起飞前2小时（含）以外办理退票按票面价收取50%的退票费，2小时以内及起飞后不得退票。'
# refund = "起飞（含）前需收取票面价30%的退票费，起飞后需收取票面价40%的退票费。"

# # to dict
# rebooking = TicketChangeConvert.convert_to_simple_rebook(rebooking)
# refund = TicketChangeConvert.convert_to_simple_refund(refund)

# jieba
# import jieba.posseg as pseg
# words = pseg.cut(rebooking)
# for word, flag in words:
#     print('%s %s' % (word, flag))

# tags = jieba.analyse.extract_tags(rebooking, topK=10)
#
# print(",".join(tags))
# cut
jieba.enable_parallel(10)
jieba.load_userdict("matafy.dict")

client = get_client(url='localhost', port=27017, username='', password='')
videos_col = get_col(client, 'videos', 'video_test')
tags_col = get_col(client, 'videos', 'tags')


#
# def extract_keywords_jieba():
#     seg_list_name = jieba.lcut(name)
#     print(seg_list_name)
#     print("Name Default Mode: " + "/ ".join(seg_list_name))  # 精確模式
#
#     seg_list_note = jieba.lcut(note)
#     print(seg_list_note)
#     print("Note Default Mode: " + "/ ".join(seg_list_note))  # 精確模式
#
#     keywords_list = list(set(seg_list_name + seg_list_note))
#     print("keywords list: " + "/ ".join(keywords_list))
#
#     allowPOS = ('ns', "n", "v", "vn", "s")
#
#     for x, w in jieba.analyse.extract_tags(name, topK=10, withWeight=True):
#         print('name:>>>%s %s' % (x, w))
#
#     for x, w in jieba.analyse.extract_tags(note, topK=10, withWeight=True):
#         print('note:>>>%s %s' % (x, w))


def extract_keywords():
    videos = videos_col.find({}).batch_size(50)
    for index, video in enumerate(videos):
        try:
            print(index)
            print(type(video))
            name = video.get("name")
            note = video.get("note")
            words = get_lexical_result(name + note)
            videos_col.update_one({"_id": video.get("_id")}, {"$set": {"words": words}}, upsert=False)
        except Exception as e:
            print(str(e))


def extract_tags():
    videos = videos_col.find({}).batch_size(50)
    with open("matafy.dict") as dictionary:
        tags = dictionary.read().splitlines()
        print(tags)
        for index, video in enumerate(videos):
            try:
                print(index)
                print(type(video))
                name = video.get("name")
                note = video.get("note")
                text = ",".join(list(set([name, note])))
                print("text >>> %s" % text)
                keywords = []
                for tag in tags:
                    if tag in text:
                        keywords.append(tag)
                videos_col.update_one({"_id": video.get("_id")}, {"$set": {"tags": keywords}}, upsert=False)
            except Exception as e:
                print(str(e))


def add_basic_tags():
    videos = videos_col.find({}).batch_size(50)
    for index, video in enumerate(videos):
        try:
            print(index)
            print(type(video))
            keywords = video.get("tags")
            video_type = video.get("video_type")
            tag = tags_col.find_one({"tag":str(video_type)})
            keyword = tag.get("name")
            print(keyword)
            # text = ",".join(list(set([name, note])))
            # print("text >>> %s" % text)
            keywords.append(keyword)

            videos_col.update_one({"_id": video.get("_id")}, {"$set": {"tags": list(set(keywords))}}, upsert=False)
        except Exception as e:
            print(str(e))


def extract_locations():
    pass


if __name__ == '__main__':
    # tags = jieba.analyse.extract_tags("在白云和岩石间自由飞行，翼装飞行精选视频。", topK=10)
    # tags = jieba.analyse.extract_tags("初生与流逝，延时摄影快速剪辑", topK=5)
    # print(tags)
    add_basic_tags()
