import nltk, os

nltk.download('punkt')

from nltk.stem.lancaster import LancasterStemmer

stemmer = LancasterStemmer()

import numpy as np
import tensorflow as tf
import tflearn
import random
import json
import pickle
import discord

with open("intents.json") as file:
  data = json.load(file)

try:
  with open("data.pickle", "rb") as f:
    words, labels, training, output = pickle.load(f)

except:
  words = []
  labels = []
  docs_x = []
  docs_y = []
  for intent in data["intents"]:
    for pattern in intent["patterns"]:
      wrds = nltk.word_tokenize(pattern)
      words.extend(wrds)
      docs_x.append(wrds)
      docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
      labels.append(intent["tag"])

  words = [stemmer.stem(w.lower()) for w in words if w != "?"]
  words = sorted(list(set(words)))
  labels = sorted(labels)

  training = []
  output = []
  out_empty = [0 for _ in range(len(labels))]

  for x, doc in enumerate(docs_x):
    bag = []

    wrds = [stemmer.stem(w.lower()) for w in doc]

    for w in words:
      if w in wrds:
        bag.append(1)
      else:
        bag.append(0)

    output_row = out_empty[:]
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)

  training = np.array(training)
  output = np.array(output)

  with open("data.pickle", "wb") as f:
    pickle.dump((words, labels, training, output), f)

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, len(output[0]), activation="softmax")
net = tflearn.regression(net)

model = tflearn.DNN(net)
print(training, output.shape)
if [os.path.isfile(i)
    for i in ["model.tflearn.meta", "model.tflearn.index"]] == [True, True]:
  model.load("model.tflearn")
else:
  print("Training")
  model.fit(training.values, output, n_epoch=1, batch_size=8, show_metric=True)
  print("Training complete")
  model.save("model.tflearn")


def bag_of_words(s, words):
  bag = [0 for _ in range(len(words))]

  s_words = nltk.word_tokenize(s)
  s_words = [stemmer.stem(word.lower()) for word in s_words]

  for se in s_words:
    for i, w in enumerate(words):
      if w == se:
        bag[i] = 1

  return np.array(bag)


def chat():
  print("Yawn... Another day of work. (type dismissed to stop)")
  while True:
    inp = input("You: ")
    if inp.lower() == "dismissed":
      print("Going to hit the haysack now. Stay out of trouble.")
      break

    result = model.predict([bag_of_words(inp, words)])[0]
    result_index = np.argmax(result)
    tag = labels[result_index]

    if result[result_index] > 0.7:
      for tg in data["intents"]:
        if tg['tag'] == tag:
          responses = tg['responses']
      print(random.choice(responses))

    else:
      print("Hmm? I don't understand you.")


class MyClient(discord.Client):

  async def on_ready(self):
    print('Logged in as')
    print(self.user.name)
    print(self.user.id)
    print('------')

  async def on_message(self, message):
    if message.author.id == self.user.id:
      return

    else:
      inp = message.content
      result = model.predict([bag_of_words(inp, words)])[0]
      result_index = np.argmax(result)
      tag = labels[result_index]
      if result[result_index] > 0.7:
        for tg in data["intents"]:
          if tg['tag'] == tag:
            responses = tg['responses']

        bot_response = random.choice(responses)
        await message.channel.send(bot_response.format(message))
      else:
        pass
        # await message.channel.send("I didn't understand that.".format(message))


token = os.environ['DISCORD_TOKEN']
client = MyClient(intents=discord.Intents.all())
client.run(token)
#chat()
