import random
import time

from bs4 import BeautifulSoup

from utils.baidu import get_segmented_words
from utils.mongodb_util import zhidao_dev_col


def extract_text(html):
    soup = BeautifulSoup(html)
    result = soup.getText()
    return result


def preprocess_dureader(target=zhidao_dev_col):
    """
    首次使用app　既没有候选集，也没有历史记录　根据不同类别分别选择不同的视频推荐
    :return:
    """
    qas = target.find().batch_size(50)
    with open("/tmp/dureader.txt", "w+") as f:
        for index, qa in enumerate(qas):
            try:
                # print(index)
                # question
                question = qa.get("segmented_question")

                if not qa.get("answer_docs"):
                    continue
                answer_doc = qa.get("answer_docs")[0]
                document = qa.get("documents")[answer_doc]
                question = " ".join(question)
                # print(question)

                # document title paras
                title = document.get("segmented_title")
                most_related_para = document.get("most_related_para")
                paragraphs = document.get("paragraphs")
                para = paragraphs[most_related_para]
                para = extract_text(para)
                para = get_segmented_words(para)
                para = " ".join(para)
                # print(para)

                # answers
                if not qa.get("fake_answers"):
                    continue
                fake_answer = qa.get("fake_answers")[0]
                fake_answer = extract_text(fake_answer)
                answer = get_segmented_words(fake_answer)
                # answer_index = qa.get("answers").index(fake_answer)
                # answer = qa.get("segmented_answers")[answer_index]
                # print(answer)
                answer = " ".join(answer)

                # print into dureader txt
                f.write("%s\t%s\t%s\r\n" % (para, question, answer))

            except Exception as e:
                print(index)
                print(str(e))
                print(qa.get("_id"))
                # print(fake_answer)
                # print(qa.get("answers"))

    return


if __name__ == "__main__":
    # rd = randomDate("2018-01-25 15:45:34", "2018-02-01 15:45:34", random.random())
    # print(rd)
    # update_datetime()
    preprocess_dureader()
