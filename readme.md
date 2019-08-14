<h1 align="center">rasa-faq-bot-chinese</h1>
<p align="center">Using Rasa to build a FAQ bot</p>

<p align="center">
  <a href="https://github.com/nghuyong/rasa-faq-bot/stargazers">
    <img src="https://img.shields.io/github/stars/nghuyong/rasa-faq-bot.svg?colorA=orange&colorB=orange&logo=github"
         alt="GitHub stars">
  </a>
  <a href="https://github.com/nghuyong/rasa-faq-bot/issues">
        <img src="https://img.shields.io/github/issues/nghuyong/rasa-faq-bot.svg"
             alt="GitHub issues">
  </a>
  <a href="https://github.com/nghuyong/rasa-faq-bot/">
        <img src="https://img.shields.io/github/last-commit/nghuyong/rasa-faq-bot.svg">
  </a>
  <a href="https://github.com/nghuyong/rasa-faq-bot/blob/master/LICENSE">
        <img src="https://img.shields.io/github/license/nghuyong/rasa-faq-bot"
             alt="GitHub license">
  </a>
</p>

<h2 align="center">Introduction</h2>

[Rasa](https://rasa.com/) is a powerful dialog framework that we can easily use it to build a practical dialog system.

FAQ(Frequently Asked Questions) bot is the most important part of the smart customer service products, which help users to solve general problems.

Usually we collect common questions and answers from actual scenarios and we call these standard question-and-answer pairs for the knowledge base.
FAQ-bot will intelligently answer user questions based on this knowledge base.

So, in this project, we will use Rasa to build a smart faq-bot!


<h2 align="center">Get Started</h2>

1. Change the `BERT_CHINESE_MODEL_DIR` in `run_bert_service.sh` and run. More information about [bert-as-service](https://github.com/hanxiao/bert-as-service).

You need to install bert-serving-server and bert-serving-client, and then download the pre-trained bert model according to your need. In the example, we downloaded the [BERT-Base, Chinese](https://storage.googleapis.com/bert_models/2018_11_03/chinese_L-12_H-768_A-12.zip) model. More details are in [bert-as-service](https://github.com/hanxiao/bert-as-service).

After you download the bert model, you get a .zip file. And then, for example, you create a folder named "bert-models" and put the model into the folder and unzip the model. In our example, I will get a folder named "chinese_L-12_H-768_A-12". We change the name into "bert_zh". 

Next, you need to change "BERT_CHINESE_MODEL_DIR" into your model path(for example "F:/bert-models/bert_zh"):

```latex
bert-serving-start \
    -pooling_layer -4 -3 -2 -1 \
    -model_dir=BERT_CHINESE_MODLE_DIR \
    -num_worker=8 \
    -max_seq_len=16
```

After doing all these things, you can run the shell.

```bash 
./run_bert_service.sh
```

2. Run Rasa custom actions

First you need to change the port in endpoints.yml to keep the port the same as the port of rasa actions(default port is 5055):

```latex
action_endpoint:
  url: "http://localhost:5055/webhook"
```

Then run the command.

```bash
rasa run actions
```
Then you can get a log like this:

```latex
│2019-08-09 11:10:32 INFO     rasa_sdk.endpoint  - Starting action endpoint server...
│(1000, 3072)
│2019-08-09 11:10:33 INFO     rasa_sdk.executor  - Registered function for 'action_get_answer'.
│2019-08-09 11:10:33 INFO     rasa_sdk.endpoint  - Action endpoint is up and running. on ('0.0.0.0', 5055)
```


3. Run Rasa x

You need to install [rasa x](https://rasa.com/docs/rasa-x/installation-and-setup/) first.

```bash
rasa x
```


If you are using a server, you should specify a port(for example 8888).

```bash
rasa x --rasa-x-port 8888
```

And you can get a log like this:

```latex
Starting Rasa X in local mode... �🚀                                                                                               
 
The server is running at http://localhost:8888/login?username=me&password=zrjV0BwYSzYP
```
Change the localhost into your server ip, then you can access your rasa x page.



<h2 align="center">Dialogue Example</h2>

![](./images/happy_path.png)
