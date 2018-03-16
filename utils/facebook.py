from pyfasttext import FastText
model = FastText()
model.load_model("wiki.zh.vec")
print(model["跑酷"])