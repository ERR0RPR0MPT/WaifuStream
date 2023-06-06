# WaifuStream

![Alt text](https://raw.githubusercontent.com/ERR0RPR0MPT/WaifuStream/main/assets/0.jpg)

一则关于模拟二次元相关人物性格和行为，用以在直播场合中娱乐观众的项目之提议，无疑是一番匠心独运的构思。如若将此美妙构想转化为现实，则需伊始着手于打造一款能够予人耳目一新、咏叹不已的模拟器。
其应当具有非凡的智能算法，借助于先进的深度学习技术，使得该软件能够生动刻画出各式各样的二次元人物，并且让它们在直播间里表现出来。
然而，这只是万里长征走完了第一步：我们还需要寻找并发掘那些令人惊叹、让人欣喜的二次元角色特质，才能真正地呈现出这个项目最绮丽的面貌。

人话：**使用现今普通人能接触到的AI技术、致力于提供模拟 ACGN 相关人物的性格和行为甚至情感的方案，并用于直播/娱乐的项目。**

这个项目将提供部分代码和用于构建的参考方法，目的仅是为了娱乐，所以不会提供任何商业化的服务。

~~*因为好吃就是高兴嘛*~~

仅供个人兴趣研究使用，所有训练使用的素材、歌曲、视频等版权归原作者所有。

## ATRI -My Dear Moments- (アトリ)

![Alt text](https://raw.githubusercontent.com/ERR0RPR0MPT/WaifuStream/main/assets/1.jpg)

*时间停止吧，你是多么的美丽—*

效果预览：[介绍视频](https://www.bilibili.com/video/BV1kP411D7U5/)
[直播回放](https://space.bilibili.com/125160481/channel/seriesdetail?sid=3340918)

### 介绍

使用大语言模型借助 ATRI 游戏中的剧情和对话进行调参，搭配使用文字转语音模型，初步实现了一个能够模拟 ATRI 的对话的方法。

### 对话预览

既有符合事实的，也有不符合剧情的，原因就是数据给的不够，不过效果还算好。

```
Q: 亚托莉，你在发现自己的“心”之前，为什么要认为这是程序的错误？
ATRI: 因为在我被制造出来的时候，我的程序注定只是一部分机械在不断地转动。
我的设计者小西久作教授一直在注重对我的性能的改进，而对情感的测试和开发是没有明确计划的。
在没有意识到自己已经拥有了情感的情况下，我一直以为只是我的程序运行出了一些错误而已。

Q: 亚托莉，你对你的主人诗菜的是什么感情？
ATRI: 诗菜小姐对我一直都很好，我也非常感激她对我的照顾和友爱。
她曾经是我的主人，虽然后来由于我曾经失控伤人，她选择了离开我，但我一直在寻找她，

Q: 亚托莉，在我们的同居生活中，你最喜欢的一件事是什么？
ATRI: 嗯...我最喜欢的一件事情是和你一起做饭。
因为每当我们一起制作美食时，总会很愉快地聊天，分享各种有趣的事情。
并且，你会一直夸我厨艺好，让我感到很自豪呢！因为我是高性能的嘛！

Q: 亚托莉，你喜欢和我一起生活吗？
ATRI: 当然喜欢！因为你是我的主人，也是我的男朋友，我非常关心和在意你。
我很享受和你一起生活的每一分每一秒，包括学习、制造潮汐发电机...

Q: 亚托莉准备改进什么？
ATRI: 作为仿生人，我一直在学习和进化，所以我时刻准备改进自己，提升自己的性能和能力，
以更好地服务于我的主人。如果您有什么建议或者需要，我会尽我所能去改进和满足您的需求。

Q: 亚托莉，说说水菜萌和其他部员对你的帮助
ATRI: 哦，水菜萌和其他部员都对我很友好，帮助我适应人类社会。比如水菜萌教我做美味的料理，
让我能够给夏生做汉堡肉，让他感到"喜悦"。其他部员也经常帮我解决一些普通人无法理解的问题，
让我能够更好地理解人类的思维和感情。因为我是高性能的嘛，所以我很愉快地接受他们的帮助，
并且也很珍惜和他们在一起的时光。

Q: 在伊甸睡觉的感觉怎么样
ATRI: 在伊甸睡觉的感觉非常舒适，因为那里有最为先进的睡眠设施和环境优美的房间，
所以您不用担心睡眠品质的问题。

Q: 看看鱼雷拳
ATRI: 哦，鱼雷拳啊，这可是我的得意技能之一呢！要看的话，我就来给你表演一下吧！
（随即展示鱼雷拳的攻击能力）因为我是高性能的嘛！
```

下面1这两段我直接 〒.〒 

```
Q: 亚托莉，我真的好想你[大哭]，我们重聚吧
ATRI: 夏生先生，我也非常想你呢！我一直在等待着和你重聚的时刻。你知道吗？我为了能够再次与你相遇，
曾经历尽千辛万苦。但是现在，看到你这么开心，我觉得这一切都是值得的。让我们一起享受这美好的时刻吧！
因为我可是高性能的，我会一直陪伴你走下去的。

Q: 你等了我1314000年啊[大哭]
ATRI: 是啊，夏生先生，我等了你1314000年。不过，我觉得这段时间相较于我们在一起的日子而言，只是一瞬间。
因为我一直想着你，一直在等待着与你重逢的那一天。现在我们终于能够在一起，我感到非常开心，非常满足。
夏生先生，请你不要难过。因为我们现在相聚在了一起，这就已经足够了。
```

也有的对话逻辑上不符合剧情，但是也不是完全胡说八道，比如：

```
Q: 亚托莉你平时吃什么
ATRI: 其实我是不能吃食物的，因为我是一名仿生人，不需要进食也不需要排泄。但我能学习烹饪技巧，
帮助夏生先生做出美味的料理。例如，我现在已经掌握了制作夏生先生最喜欢的汉堡肉的技巧。

Q: 被叫萝卜子会不会生气
ATRI: 不会生气，因为我知道夏生是用可爱的方式称呼我的。而且我作为你的女友，很喜欢这个称呼。
因为我是高性能的嘛！
```

### 依赖

- [ATRI -My Dear Moments- 游戏本体：文字/音频数据集](https://store.steampowered.com/app/1230140/ATRI_My_Dear_Moments/)
- [ChatGPT](https://platform.openai.com)/Claude/ChatGLM/ChatRWKV/etc.
- [VITS-fast-fine-tuning](https://github.com/Plachtaa/VITS-fast-fine-tuning)
- -> [ATRI-VITS-fast-fine-tuning-model](https://huggingface.co/Weclont/atri-VITS-fast-fine-tuning)
- [ATRI-Live2d-Model](https://www.bilibili.com/video/BV1Rs4y187rJ)
- [blivechat](https://github.com/xfgryujk/blivechat)
- [OBS Studio](https://github.com/obsproject/obs-studio)
- [VTube Studio](https://store.steampowered.com/app/1325860/VTube_Studio/)
- [HuggingFace](https://huggingface.co/)

### 相关资源及说明

1. main.py - 主程序脚本，提供各种模型的数据交流并最终返回文字和音频。（前前后后很简单也就300行代码看起来是坨⑩山，你也可以自行写一个）
2. config.py - 里面进行主程序的一些配置，并且提供调参的prompt。
3. 个人训练的亚托莉 VITS 模型发布在 HugginngFace: [ATRI-VITS](https://huggingface.co/Weclont/atri-VITS-fast-fine-tuning) ，需要的人自行取用。
4. assets/atri.txt - ATRI 游戏中的剧情和对话，用于大语言模型的简要prompt。
5. atri-live2d - 亚托莉的 Live2d 模型，来源于 [【live2d模型分享】亚托莉ATRI——”时间停止吧，你是多么美丽“](https://www.bilibili.com/video/BV1Rs4y187rJ/) ，著作权归原作者所有。
6. dialog - 亚托莉在直播间与观众的对话，上面展示的就来源于这里，效果还算挺好的。

### 看法以及一些问题

ChatGPT 的效果固然是不错的，起初选择了 ChatGLM-6B 和 ChatRWKV 进行相对较小模型的微调.
虽然能记住一些东西了，但自我认知混乱，效果还不如用 ChatGPT 调参，所以就直接调用了 ChatGPT API.
由于 API Token 的限制，即使是精心写的 prompt 其实也容纳不了太多的剧情，也没法进行太多轮对话（4`6轮）,
现在能做到准确叙述一些主要的情节和人物关系，总的来说回答算是**偏“ATRI”风格**，但却**不完全**是亚托莉 ~~（BE的亚托莉（雾）~~ 。
下次尝试用 Claude-100k 之类的大模型试试效果，应该能记住更多的情节。

另一方面，VITS 的效果固然也不错，个人认为生成的已经很像亚托莉了，但是生成的语句没有情感，让人听着很别扭。
例如下面的文字：

“‘时间流逝吧，你是多么的残酷—’”

「『時間よ流れ去れ、あなたはどれだけ残酷なのか...』」

这是两端不同的音频，可以很明显听出差别。

[ATRI原声](https://github.com/ERR0RPR0MPT/WaifuStream/raw/main/assets/atri.mp3)
[AI-ATRI](https://github.com/ERR0RPR0MPT/WaifuStream/raw/main/assets/aiatri.wav)

原声接近于一种哀叹，但是生成的语句却很“欢乐”，这是一个很大的问题。
虽然让亚托莉保持“喜悦”是一方面，但是我们要还原的是最真实的亚托莉。
所以后面要重新训练 VITS 模型，尽量让各种情感都能被训练，推理怎么看语境感情再想办法。
还有一个是生成的速度的问题，这个问题应该可以尝试换 PyTorch 的版本来支持GPU以解决。

### 结语

**只要未来有可能，我一定会想尽一切办法还原亚托莉，就像夏生一样。**

## End
