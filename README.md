# Skyrim-Chatbot

A discord chatbot built using NLTK and Tensorflow featuring one of the most familiar NPC in Skyrim.

## Demo
![Demo1](https://user-images.githubusercontent.com/59202185/197256690-9183f8ad-c3d2-4f89-a0f3-0bb35b29943c.gif)
![Demo2](https://user-images.githubusercontent.com/59202185/197256790-23bca9d3-dee7-4b3a-b6c6-8fe7c5882e31.gif)

## Dataset
The guard dialogues were scrapped from The Unoffical Elder Scroll Pages and a [csv](dataset\guard_dialogues.csv) file was created.

This, in turn, helped me manually create the [intents.json](intents.json) file.

Using Bag Of Words Representation, we preprocess the JSON and create the [pickle](data.pickle) file which helps to train our model. You may directly use this for training or prediction.

## How to run
1.  Clone the repo
2.  Install the requirements with the command `pip install requirements.txt`
3.  Run main.py (see below for more details)
### Chatting in local system
If you just want to run it in your local system, you can use the `chat()` function. Just comment out lines in [main.py](/main.py) related to discord (153, 154, 155) and uncomment line 156. You should now be able to interact with the chatbot in the terminal.

### Chatting in Discord
This involves more steps.
1. Create an application in [Discord Developer Portal](https://discord.com/developers/applications)
2. Add a bot and give it permission to Send Text Messages.
3. Enable all Gateway Intents as well.
4. Copy the token and set it as the  environment variable / secret named "DISCORD_TOKEN"
5. Run main.py and you should be able to interact with the bot as long as the application is running.

If you want your bot stay online even after you switch off your PC, you might want to use an online platform which will let you run your python script continuously.
