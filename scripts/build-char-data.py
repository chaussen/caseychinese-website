#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build learn/char-data.js for the Character Explorer (characters.html).

Merges the curated 300-character content table below (pinyin, kid-friendly
gloss, theme group, common word, example sentence) with stroke paths +
medians from the makemeahanzi project
(https://github.com/skishore/makemeahanzi).

Usage:
    python3 scripts/build-char-data.py [--graphics PATH] [--dict PATH]

If --graphics/--dict are not given, the two makemeahanzi data files are
downloaded into .cache/ (about 33 MB, one-off).
"""
import argparse
import json
import os
import re
import sys
import unicodedata
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "learn", "char-data.js")
MMAH = "https://raw.githubusercontent.com/skishore/makemeahanzi/master/"

# ---------------------------------------------------------------------------
# Curated content: 300 common characters in kid-friendly theme groups.
# Entry: (char, pinyin, gloss,
#         word, per-char word pinyin, word gloss,
#         sentence, per-CJK-char sentence pinyin, sentence gloss)
# The sentence fields are None for the original twelve characters, whose
# hand-written example sentences (OVERRIDES below) are kept as-is.
# ---------------------------------------------------------------------------
GROUPS = [
("Me & my body", [
  ("人","rén","person","大人","dà rén","grown-up",None,None,None),
  ("大","dà","big","大家","dà jiā","everyone",None,None,None),
  ("小","xiǎo","small","大小","dà xiǎo","size",None,None,None),
  ("口","kǒu","mouth","门口","mén kǒu","doorway",None,None,None),
  ("手","shǒu","hand","拍手","pāi shǒu","clap your hands",
   "我有两只小手。","wǒ yǒu liǎng zhī xiǎo shǒu","I have two little hands."),
  ("心","xīn","heart","小心","xiǎo xīn","be careful",
   "过马路要小心。","guò mǎ lù yào xiǎo xīn","Be careful crossing the road."),
  ("头","tóu","head","头发","tóu fa","hair",
   "点点头，摇摇头。","diǎn diǎn tóu yáo yáo tóu","Nod your head, shake your head."),
  ("目","mù","eye","目光","mù guāng","a look, a gaze",
   "这个题目真有趣。","zhè gè tí mù zhēn yǒu qù","This question is really interesting."),
  ("耳","ěr","ear","耳朵","ěr duo","ear",
   "兔子的耳朵长长的。","tù zi de ěr duo cháng cháng de","Rabbits have long ears."),
  ("眼","yǎn","eye","眼睛","yǎn jing","eyes",
   "我的眼睛大大的。","wǒ de yǎn jing dà dà de","My eyes are big."),
  ("身","shēn","body","身体","shēn tǐ","body, health",
   "运动让身体更好。","yùn dòng ràng shēn tǐ gèng hǎo","Exercise makes your body stronger."),
  ("体","tǐ","body","体育","tǐ yù","sport, PE",
   "我喜欢上体育课。","wǒ xǐ huan shàng tǐ yù kè","I love PE class."),
  ("自","zì","self","自己","zì jǐ","oneself",
   "我自己穿衣服。","wǒ zì jǐ chuān yī fu","I get dressed by myself."),
  ("己","jǐ","oneself","自己","zì jǐ","oneself",
   "自己的事自己做。","zì jǐ de shì zì jǐ zuò","Do your own things yourself."),
  ("力","lì","strength","用力","yòng lì","use your strength",
   "大象力气真大。","dà xiàng lì qi zhēn dà","Elephants are really strong."),
  ("声","shēng","sound, voice","大声","dà shēng","loudly",
   "请大声读课文。","qǐng dà shēng dú kè wén","Please read the text out loud."),
]),
("Family & people", [
  ("你","nǐ","you","你们","nǐ men","you all",None,None,None),
  ("我","wǒ","I, me","我们","wǒ men","we, us",
   "我爱我的家。","wǒ ài wǒ de jiā","I love my family."),
  ("他","tā","he","他们","tā men","they",
   "他是我的同学。","tā shì wǒ de tóng xué","He is my classmate."),
  ("她","tā","she","她们","tā men","they (girls and women)",
   "她是我妹妹。","tā shì wǒ mèi mei","She is my little sister."),
  ("它","tā","it","它们","tā men","they (animals and things)",
   "它是一只小猫。","tā shì yì zhī xiǎo māo","It's a kitten."),
  ("们","men","(makes words plural)","我们","wǒ men","we, us",
   "我们一起玩吧。","wǒ men yì qǐ wán ba","Let's play together."),
  ("好","hǎo","good","你好","nǐ hǎo","hello",None,None,None),
  ("妈","mā","mum","妈妈","mā ma","Mum",
   "妈妈给我讲故事。","mā ma gěi wǒ jiǎng gù shi","Mum tells me stories."),
  ("爸","bà","dad","爸爸","bà ba","Dad",
   "爸爸带我去公园。","bà ba dài wǒ qù gōng yuán","Dad takes me to the park."),
  ("子","zǐ","child","孩子","hái zi","child",
   "这个孩子真可爱。","zhè gè hái zi zhēn kě ài","This child is so cute."),
  ("女","nǚ","woman, girl","女儿","nǚ ér","daughter",
   "那个女孩在唱歌。","nà gè nǚ hái zài chàng gē","That girl is singing."),
  ("男","nán","man, boy","男孩","nán hái","boy",
   "他是个男孩。","tā shì gè nán hái","He's a boy."),
  ("孩","hái","child","女孩","nǚ hái","girl",
   "孩子们在操场上跑。","hái zi men zài cāo chǎng shàng pǎo","The children are running on the playground."),
  ("儿","ér","child, son","儿子","ér zi","son",
   "鸟儿在天上飞。","niǎo ér zài tiān shàng fēi","Birds fly in the sky."),
  ("家","jiā","family, home","家人","jiā rén","family members",None,None,None),
  ("朋","péng","friend","朋友","péng you","friend",
   "我有很多好朋友。","wǒ yǒu hěn duō hǎo péng you","I have lots of good friends."),
  ("友","yǒu","friend","好友","hǎo yǒu","good friend",
   "小朋友们手拉手。","xiǎo péng yǒu men shǒu lā shǒu","The little friends hold hands."),
  ("老","lǎo","old","老师","lǎo shī","teacher",
   "老师教我们写字。","lǎo shī jiāo wǒ men xiě zì","The teacher teaches us to write."),
  ("师","shī","teacher","老师","lǎo shī","teacher",
   "王老师真好。","wáng lǎo shī zhēn hǎo","Teacher Wang is so kind."),
  ("生","shēng","to be born; student","学生","xué sheng","student",
   "我是一年级学生。","wǒ shì yī nián jí xué shēng","I'm a Year One student."),
  ("名","míng","name","名字","míng zi","name",
   "你叫什么名字？","nǐ jiào shén me míng zi","What's your name?"),
  ("王","wáng","king","国王","guó wáng","king",
   "国王住在城堡里。","guó wáng zhù zài chéng bǎo lǐ","The king lives in a castle."),
]),
("Numbers & counting", [
  ("一","yī","one","一百","yì bǎi","one hundred",
   "一年有十二个月。","yì nián yǒu shí èr gè yuè","A year has twelve months."),
  ("二","èr","two","二月","èr yuè","February",
   "我上二年级。","wǒ shàng èr nián jí","I'm in Year Two."),
  ("三","sān","three","三个","sān gè","three of them",
   "我家有三口人。","wǒ jiā yǒu sān kǒu rén","There are three people in my family."),
  ("四","sì","four","四季","sì jì","the four seasons",
   "一年有四个季节。","yì nián yǒu sì gè jì jié","A year has four seasons."),
  ("五","wǔ","five","五星","wǔ xīng","five stars",
   "我的手有五个手指。","wǒ de shǒu yǒu wǔ gè shǒu zhǐ","My hand has five fingers."),
  ("六","liù","six","六岁","liù suì","six years old",
   "我今年六岁。","wǒ jīn nián liù suì","I'm six this year."),
  ("七","qī","seven","七天","qī tiān","seven days — a week",
   "一个星期有七天。","yí gè xīng qī yǒu qī tiān","A week has seven days."),
  ("八","bā","eight","八点","bā diǎn","eight o'clock",
   "现在是八点。","xiàn zài shì bā diǎn","It's eight o'clock."),
  ("九","jiǔ","nine","九月","jiǔ yuè","September",
   "九加一是十。","jiǔ jiā yī shì shí","Nine plus one is ten."),
  ("十","shí","ten","十分","shí fēn","completely — ten parts full",
   "我会从一数到十。","wǒ huì cóng yī shǔ dào shí","I can count from one to ten."),
  ("百","bǎi","hundred","百花","bǎi huā","a hundred flowers",
   "这本书有一百页。","zhè běn shū yǒu yì bǎi yè","This book has a hundred pages."),
  ("千","qiān","thousand","一千","yì qiān","one thousand",
   "天上有一千颗星星吗？","tiān shàng yǒu yì qiān kē xīng xing ma","Are there a thousand stars in the sky?"),
  ("万","wàn","ten thousand","一万","yí wàn","ten thousand",
   "万里长城真长。","wàn lǐ cháng chéng zhēn cháng","The Great Wall is so long."),
  ("两","liǎng","two (of something)","两个","liǎng gè","two of them",
   "桌上有两个苹果。","zhuō shàng yǒu liǎng gè píng guǒ","There are two apples on the table."),
  ("几","jǐ","how many","几个","jǐ gè","how many?",
   "现在几点了？","xiàn zài jǐ diǎn le","What time is it now?"),
  ("个","gè","(counting word)","一个","yí gè","one of them",
   "我有一个好朋友。","wǒ yǒu yí gè hǎo péng you","I have a good friend."),
  ("半","bàn","half","一半","yí bàn","half",
   "现在是三点半。","xiàn zài shì sān diǎn bàn","It's half past three."),
  ("第","dì","(makes 'first, second…')","第一","dì yī","number one, first",
   "我得了第一名。","wǒ dé le dì yī míng","I came first!"),
  ("数","shù","number","数学","shù xué","maths",
   "我喜欢数学课。","wǒ xǐ huan shù xué kè","I like maths class."),
  ("多","duō","many","很多","hěn duō","lots",
   "公园里人真多。","gōng yuán lǐ rén zhēn duō","There are so many people in the park."),
  ("少","shǎo","few","多少","duō shǎo","how many?",
   "这本书多少钱？","zhè běn shū duō shǎo qián","How much is this book?"),
]),
("Time & days", [
  ("天","tiān","sky; day","今天","jīn tiān","today",
   "今天天气真好。","jīn tiān tiān qì zhēn hǎo","The weather is lovely today."),
  ("日","rì","sun; day","生日","shēng rì","birthday",
   "今天是我的生日。","jīn tiān shì wǒ de shēng rì","Today is my birthday."),
  ("月","yuè","moon; month","月亮","yuè liang","the moon",
   "月亮挂在天上。","yuè liang guà zài tiān shàng","The moon hangs in the sky."),
  ("年","nián","year","新年","xīn nián","New Year",
   "新年快乐！","xīn nián kuài lè","Happy New Year!"),
  ("时","shí","time; hour","时间","shí jiān","time",
   "吃饭的时间到了。","chī fàn de shí jiān dào le","It's time to eat."),
  ("候","hòu","time, moment","时候","shí hou","a time, a moment",
   "你什么时候回家？","nǐ shén me shí hou huí jiā","When are you going home?"),
  ("分","fēn","minute; to divide","分钟","fēn zhōng","minute",
   "还有五分钟下课。","hái yǒu wǔ fēn zhōng xià kè","Five more minutes until class ends."),
  ("点","diǎn","o'clock; dot","三点","sān diǎn","three o'clock",
   "我们八点上课。","wǒ men bā diǎn shàng kè","We start class at eight."),
  ("现","xiàn","now; to appear","现在","xiàn zài","now",
   "现在轮到我了。","xiàn zài lún dào wǒ le","Now it's my turn!"),
  ("今","jīn","now, this","今年","jīn nián","this year",
   "今天我们学了五个字。","jīn tiān wǒ men xué le wǔ gè zì","We learned five characters today."),
  ("明","míng","bright; next","明天","míng tiān","tomorrow",
   "明天见！","míng tiān jiàn","See you tomorrow!"),
  ("昨","zuó","yesterday","昨天","zuó tiān","yesterday",
   "昨天下了大雨。","zuó tiān xià le dà yǔ","It rained hard yesterday."),
  ("早","zǎo","early; morning","早上","zǎo shang","morning",
   "早上好！","zǎo shang hǎo","Good morning!"),
  ("晚","wǎn","late; evening","晚上","wǎn shang","evening",
   "晚上我们看星星。","wǎn shang wǒ men kàn xīng xing","At night we look at the stars."),
  ("期","qī","period of time","星期","xīng qī","week",
   "星期六我去中文学校。","xīng qī liù wǒ qù zhōng wén xué xiào","On Saturday I go to Chinese school."),
  ("常","cháng","often","常常","cháng cháng","often",
   "我常常帮妈妈做饭。","wǒ cháng cháng bāng mā ma zuò fàn","I often help Mum cook."),
  ("再","zài","again","再见","zài jiàn","goodbye — see you again",
   "再读一遍吧。","zài dú yí biàn ba","Read it one more time."),
]),
("Nature & weather", [
  ("水","shuǐ","water","水果","shuǐ guǒ","fruit",None,None,None),
  ("火","huǒ","fire","火车","huǒ chē","train",
   "火车开得真快。","huǒ chē kāi de zhēn kuài","The train goes so fast."),
  ("山","shān","mountain","爬山","pá shān","climb a mountain",
   "我们去爬山吧。","wǒ men qù pá shān ba","Let's go climb the mountain."),
  ("田","tián","field","田野","tián yě","open fields",
   "田里种着青菜。","tián lǐ zhòng zhe qīng cài","Greens are growing in the field."),
  ("土","tǔ","earth, soil","土地","tǔ dì","land",
   "种子在土里发芽。","zhǒng zi zài tǔ lǐ fā yá","Seeds sprout in the soil."),
  ("木","mù","wood; tree","木头","mù tou","wood",
   "这把椅子是木头做的。","zhè bǎ yǐ zi shì mù tou zuò de","This chair is made of wood."),
  ("树","shù","tree","大树","dà shù","a big tree",
   "树上有一个鸟窝。","shù shàng yǒu yí gè niǎo wō","There's a bird's nest in the tree."),
  ("花","huā","flower","开花","kāi huā","to bloom",
   "春天花儿开了。","chūn tiān huā ér kāi le","Flowers bloom in spring."),
  ("草","cǎo","grass","小草","xiǎo cǎo","little grass",
   "草地绿绿的。","cǎo dì lǜ lǜ de","The grass is so green."),
  ("风","fēng","wind","大风","dà fēng","a strong wind",
   "风把树叶吹落了。","fēng bǎ shù yè chuī luò le","The wind blew the leaves down."),
  ("雨","yǔ","rain","下雨","xià yǔ","to rain",
   "下雨了，带上伞。","xià yǔ le dài shàng sǎn","It's raining — take an umbrella."),
  ("雪","xuě","snow","下雪","xià xuě","to snow",
   "雪人有红红的鼻子。","xuě rén yǒu hóng hóng de bí zi","The snowman has a red nose."),
  ("云","yún","cloud","白云","bái yún","white clouds",
   "白云像棉花糖。","bái yún xiàng mián hua táng","The clouds look like fairy floss."),
  ("气","qì","air; breath","天气","tiān qì","weather",
   "别生气，笑一笑。","bié shēng qì xiào yi xiào","Don't be cross — have a smile."),
  ("阳","yáng","sun, sunshine","太阳","tài yáng","the sun",
   "太阳出来了。","tài yáng chū lái le","The sun is out."),
  ("光","guāng","light","阳光","yáng guāng","sunshine",
   "阳光照进窗户。","yáng guāng zhào jìn chuāng hu","Sunshine comes through the window."),
  ("星","xīng","star","星星","xīng xing","stars",
   "星星在眨眼睛。","xīng xing zài zhǎ yǎn jing","The stars are twinkling."),
  ("海","hǎi","sea","大海","dà hǎi","the sea",
   "大海是蓝色的。","dà hǎi shì lán sè de","The sea is blue."),
  ("河","hé","river","小河","xiǎo hé","a stream",
   "小河里有小鱼。","xiǎo hé lǐ yǒu xiǎo yú","There are little fish in the stream."),
  ("地","dì","ground, earth","草地","cǎo dì","grassy lawn",
   "别把纸扔在地上。","bié bǎ zhǐ rēng zài dì shàng","Don't throw paper on the ground."),
]),
("Animals", [
  ("鱼","yú","fish","金鱼","jīn yú","goldfish",None,None,None),
  ("马","mǎ","horse","骑马","qí mǎ","ride a horse",None,None,None),
  ("鸟","niǎo","bird","小鸟","xiǎo niǎo","little bird",
   "鸟儿飞得很高。","niǎo ér fēi de hěn gāo","The bird flies high."),
  ("鸡","jī","chicken","小鸡","xiǎo jī","chick",
   "公鸡早上喔喔叫。","gōng jī zǎo shang wō wō jiào","The rooster crows in the morning."),
  ("牛","niú","cow, ox","奶牛","nǎi niú","dairy cow",
   "牛在草地上吃草。","niú zài cǎo dì shàng chī cǎo","The cow eats grass in the meadow."),
  ("羊","yáng","sheep","山羊","shān yáng","goat",
   "小羊咩咩叫。","xiǎo yáng miē miē jiào","The lamb goes baa baa."),
  ("狗","gǒu","dog","小狗","xiǎo gǒu","puppy",
   "小狗爱追皮球。","xiǎo gǒu ài zhuī pí qiú","The puppy loves chasing the ball."),
  ("猫","māo","cat","小猫","xiǎo māo","kitten",
   "小猫在睡觉。","xiǎo māo zài shuì jiào","The kitten is sleeping."),
  ("龙","lóng","dragon","恐龙","kǒng lóng","dinosaur",
   "过年舞龙真热闹。","guò nián wǔ lóng zhēn rè nao","Dragon dancing at New Year is such fun."),
]),
("Food & drink", [
  ("吃","chī","to eat","好吃","hǎo chī","yummy",None,None,None),
  ("喝","hē","to drink","喝水","hē shuǐ","drink water",
   "渴了就喝水。","kě le jiù hē shuǐ","Drink water when you're thirsty."),
  ("饭","fàn","rice; a meal","吃饭","chī fàn","have a meal",
   "吃饭前要洗手。","chī fàn qián yào xǐ shǒu","Wash your hands before eating."),
  ("菜","cài","vegetables; a dish","青菜","qīng cài","green veggies",
   "多吃青菜身体好。","duō chī qīng cài shēn tǐ hǎo","Eat your greens to stay strong."),
  ("米","mǐ","rice (grains)","米饭","mǐ fàn","cooked rice",
   "米饭香喷喷的。","mǐ fàn xiāng pēn pēn de","The rice smells delicious."),
  ("肉","ròu","meat","牛肉","niú ròu","beef",
   "包子里有肉。","bāo zi lǐ yǒu ròu","There's meat in the bun."),
  ("果","guǒ","fruit","苹果","píng guǒ","apple",
   "我爱吃水果。","wǒ ài chī shuǐ guǒ","I love eating fruit."),
  ("蛋","dàn","egg","鸡蛋","jī dàn","egg",
   "早饭我吃了鸡蛋。","zǎo fàn wǒ chī le jī dàn","I had an egg for breakfast."),
  ("奶","nǎi","milk","牛奶","niú nǎi","milk",
   "睡前喝杯牛奶。","shuì qián hē bēi niú nǎi","Have a glass of milk before bed."),
  ("包","bāo","bun; bag","面包","miàn bāo","bread",
   "书包里有课本。","shū bāo lǐ yǒu kè běn","There are textbooks in my school bag."),
  ("糖","táng","sugar; sweets","糖果","táng guǒ","sweets",
   "糖果甜甜的。","táng guǒ tián tián de","Sweets are so sweet."),
]),
("Colours & describing", [
  ("红","hóng","red","红色","hóng sè","red",
   "红灯停，绿灯行。","hóng dēng tíng lǜ dēng xíng","Red light stop, green light go."),
  ("黄","huáng","yellow","黄色","huáng sè","yellow",
   "香蕉是黄色的。","xiāng jiāo shì huáng sè de","Bananas are yellow."),
  ("蓝","lán","blue","蓝天","lán tiān","blue sky",
   "天空蓝蓝的。","tiān kōng lán lán de","The sky is so blue."),
  ("绿","lǜ","green","绿色","lǜ sè","green",
   "春天树叶变绿了。","chūn tiān shù yè biàn lǜ le","Leaves turn green in spring."),
  ("白","bái","white","白色","bái sè","white",
   "小兔子白白的。","xiǎo tù zi bái bái de","The bunny is snowy white."),
  ("黑","hēi","black","黑色","hēi sè","black",
   "天黑了，回家吧。","tiān hēi le huí jiā ba","It's getting dark — let's go home."),
  ("色","sè","colour","彩色","cǎi sè","colourful",
   "彩虹有七种颜色。","cǎi hóng yǒu qī zhǒng yán sè","A rainbow has seven colours."),
  ("新","xīn","new","新书","xīn shū","a new book",
   "我穿上了新衣服。","wǒ chuān shàng le xīn yī fu","I put on my new clothes."),
  ("高","gāo","tall, high","高山","gāo shān","high mountains",
   "长颈鹿长得真高。","cháng jǐng lù zhǎng de zhēn gāo","Giraffes grow so tall."),
  ("长","cháng","long; (zhǎng) to grow","长城","cháng chéng","the Great Wall",
   "大象的鼻子长长的。","dà xiàng de bí zi cháng cháng de","An elephant's trunk is so long."),
  ("真","zhēn","real; really","真好","zhēn hǎo","really good!",
   "这朵花真美！","zhè duǒ huā zhēn měi","This flower is so beautiful!"),
  ("美","měi","beautiful","美丽","měi lì","beautiful",
   "公园里风景很美。","gōng yuán lǐ fēng jǐng hěn měi","The park is beautiful."),
  ("快","kuài","fast","快乐","kuài lè","happy",
   "我跑得很快。","wǒ pǎo de hěn kuài","I run fast."),
  ("慢","màn","slow","慢慢","màn màn","slowly",
   "乌龟走得很慢。","wū guī zǒu de hěn màn","Tortoises walk slowly."),
  ("冷","lěng","cold","很冷","hěn lěng","very cold",
   "冬天真冷啊！","dōng tiān zhēn lěng a","Winter is so cold!"),
  ("热","rè","hot","热水","rè shuǐ","hot water",
   "夏天很热。","xià tiān hěn rè","Summer is hot."),
  ("亮","liàng","bright","月亮","yuè liang","the moon",
   "月亮真亮啊！","yuè liang zhēn liàng a","The moon is so bright!"),
]),
("Come & go", [
  ("来","lái","to come","过来","guò lái","come over",
   "快来看小狗！","kuài lái kàn xiǎo gǒu","Come quick and see the puppy!"),
  ("去","qù","to go","去学校","qù xué xiào","go to school",
   "周末我们去海边。","zhōu mò wǒ men qù hǎi biān","We're going to the beach on the weekend."),
  ("走","zǒu","to walk","走路","zǒu lù","to walk",
   "我们走路去学校。","wǒ men zǒu lù qù xué xiào","We walk to school."),
  ("跑","pǎo","to run","跑步","pǎo bù","to go running",
   "别跑太快，小心点。","bié pǎo tài kuài xiǎo xīn diǎn","Don't run too fast — careful!"),
  ("飞","fēi","to fly","起飞","qǐ fēi","to take off",
   "飞机飞上天了。","fēi jī fēi shàng tiān le","The plane flew up into the sky."),
  ("坐","zuò","to sit","坐下","zuò xià","sit down",
   "请坐下来听故事。","qǐng zuò xià lái tīng gù shi","Sit down and listen to the story."),
  ("站","zhàn","to stand; station","车站","chē zhàn","bus stop, station",
   "我们在车站等车。","wǒ men zài chē zhàn děng chē","We wait for the bus at the stop."),
  ("进","jìn","to go in","进来","jìn lái","come in",
   "请进，欢迎你！","qǐng jìn huān yíng nǐ","Come in — welcome!"),
  ("出","chū","to go out","出去","chū qù","go out",
   "我们出去玩吧。","wǒ men chū qù wán ba","Let's go out and play."),
  ("回","huí","to return","回家","huí jiā","go home",
   "放学了，回家吃饭。","fàng xué le huí jiā chī fàn","School's out — home for dinner."),
  ("起","qǐ","to get up, to rise","起床","qǐ chuáng","get out of bed",
   "我每天七点起床。","wǒ měi tiān qī diǎn qǐ chuáng","I get up at seven every day."),
  ("开","kāi","to open","开门","kāi mén","open the door",
   "请帮我开门。","qǐng bāng wǒ kāi mén","Please open the door for me."),
  ("关","guān","to close","关门","guān mén","close the door",
   "睡觉前关灯。","shuì jiào qián guān dēng","Turn off the light before bed."),
  ("到","dào","to arrive","到家","dào jiā","arrive home",
   "火车到站了。","huǒ chē dào zhàn le","The train has arrived."),
]),
("Everyday actions", [
  ("看","kàn","to look, to read","看见","kàn jiàn","to see",None,None,None),
  ("听","tīng","to listen","听见","tīng jiàn","to hear",
   "上课要认真听。","shàng kè yào rèn zhēn tīng","Listen carefully in class."),
  ("说","shuō","to speak","说话","shuō huà","to talk",
   "我会说中文。","wǒ huì shuō zhōng wén","I can speak Chinese."),
  ("话","huà","words, speech","电话","diàn huà","telephone",
   "打电话给奶奶。","dǎ diàn huà gěi nǎi nai","Call Grandma on the phone."),
  ("读","dú","to read","读书","dú shū","to read books",
   "我们一起读课文。","wǒ men yì qǐ dú kè wén","Let's read the text together."),
  ("写","xiě","to write","写字","xiě zì","write characters",
   "我会写自己的名字。","wǒ huì xiě zì jǐ de míng zi","I can write my own name."),
  ("睡","shuì","to sleep","睡觉","shuì jiào","go to sleep",
   "九点要上床睡觉。","jiǔ diǎn yào shàng chuáng shuì jiào","Bedtime is nine o'clock."),
  ("觉","jiào","a sleep; (jué) to feel","睡觉","shuì jiào","go to sleep",
   "小宝宝在睡觉。","xiǎo bǎo bao zài shuì jiào","The baby is sleeping."),
  ("做","zuò","to do, to make","做饭","zuò fàn","to cook",
   "我们一起做游戏。","wǒ men yì qǐ zuò yóu xì","Let's play a game together."),
  ("作","zuò","to do (work)","作业","zuò yè","homework",
   "我写完作业再玩。","wǒ xiě wán zuò yè zài wán","I finish my homework before playing."),
  ("用","yòng","to use","不用","bú yòng","no need",
   "我用筷子吃饭。","wǒ yòng kuài zi chī fàn","I eat with chopsticks."),
  ("打","dǎ","to hit; to play","打球","dǎ qiú","play ball",
   "我们去打球吧。","wǒ men qù dǎ qiú ba","Let's go play ball."),
  ("找","zhǎo","to look for","找到","zhǎo dào","to find",
   "我的笔找到了！","wǒ de bǐ zhǎo dào le","I found my pen!"),
  ("叫","jiào","to call, to shout","大叫","dà jiào","to shout",
   "我的小狗叫豆豆。","wǒ de xiǎo gǒu jiào dòu dòu","My puppy is called Doudou."),
  ("问","wèn","to ask","问题","wèn tí","a question",
   "不懂就要问老师。","bù dǒng jiù yào wèn lǎo shī","If you don't understand, ask the teacher."),
  ("给","gěi","to give","送给","sòng gěi","to give (someone something)",
   "请把书给我。","qǐng bǎ shū gěi wǒ","Please pass me the book."),
  ("送","sòng","to give, to send","送礼物","sòng lǐ wù","give a present",
   "我送你一张画。","wǒ sòng nǐ yì zhāng huà","I'll give you a picture."),
  ("放","fàng","to put; to let go","放学","fàng xué","school's out",
   "把书放进书包。","bǎ shū fàng jìn shū bāo","Put the books in your school bag."),
  ("帮","bāng","to help","帮忙","bāng máng","to help out",
   "谢谢你帮我！","xiè xie nǐ bāng wǒ","Thanks for helping me!"),
  ("住","zhù","to live (somewhere)","住在","zhù zài","to live in",
   "我住在墨尔本。","wǒ zhù zài mò ěr běn","I live in Melbourne."),
  ("买","mǎi","to buy","买菜","mǎi cài","buy groceries",
   "妈妈去超市买菜。","mā ma qù chāo shì mǎi cài","Mum buys groceries at the supermarket."),
  ("洗","xǐ","to wash","洗手","xǐ shǒu","wash your hands",
   "我自己洗脸刷牙。","wǒ zì jǐ xǐ liǎn shuā yá","I wash my face and brush my teeth by myself."),
]),
("Songs, games & stories", [
  ("唱","chàng","to sing","唱歌","chàng gē","sing songs",
   "我们一起唱儿歌。","wǒ men yì qǐ chàng ér gē","Let's sing a nursery rhyme together."),
  ("歌","gē","song","儿歌","ér gē","nursery rhyme",
   "这首歌真好听。","zhè shǒu gē zhēn hǎo tīng","This song sounds lovely."),
  ("音","yīn","sound","音乐","yīn yuè","music",
   "我喜欢上音乐课。","wǒ xǐ huan shàng yīn yuè kè","I love music class."),
  ("乐","lè","happy; (yuè) music","快乐","kuài lè","happy",
   "祝你生日快乐！","zhù nǐ shēng rì kuài lè","Happy birthday to you!"),
  ("玩","wán","to play","好玩","hǎo wán","fun",
   "我们去公园玩吧。","wǒ men qù gōng yuán wán ba","Let's go play in the park."),
  ("跳","tiào","to jump","跳舞","tiào wǔ","to dance",
   "小兔子跳得真高。","xiǎo tù zi tiào de zhēn gāo","The bunny jumps so high."),
  ("游","yóu","to swim","游泳","yóu yǒng","to swim",
   "夏天我去游泳。","xià tiān wǒ qù yóu yǒng","In summer I go swimming."),
  ("事","shì","matter, thing","故事","gù shi","story",
   "睡前讲个故事吧。","shuì qián jiǎng gè gù shi ba","Tell a story before bed."),
  ("故","gù","old; reason","故事","gù shi","story",
   "我最爱听故事了。","wǒ zuì ài tīng gù shi le","I love stories most of all."),
]),
("Think & feel", [
  ("想","xiǎng","to think; to miss","想家","xiǎng jiā","to miss home",
   "我想妈妈了。","wǒ xiǎng mā ma le","I miss Mum."),
  ("知","zhī","to know","知道","zhī dào","to know",
   "我知道答案！","wǒ zhī dào dá àn","I know the answer!"),
  ("道","dào","way, path","知道","zhī dào","to know",
   "我知道回家的路。","wǒ zhī dào huí jiā de lù","I know the way home."),
  ("认","rèn","to recognise","认字","rèn zì","recognise characters",
   "我认识很多汉字。","wǒ rèn shi hěn duō hàn zì","I know lots of Chinese characters."),
  ("识","shí","to know","认识","rèn shi","to know (someone)",
   "很高兴认识你！","hěn gāo xìng rèn shi nǐ","Nice to meet you!"),
  ("怕","pà","to fear","害怕","hài pà","scared",
   "我不怕打雷。","wǒ bú pà dǎ léi","I'm not scared of thunder."),
  ("爱","ài","to love","我爱你","wǒ ài nǐ","I love you",
   "我爱爸爸妈妈。","wǒ ài bà ba mā ma","I love Mum and Dad."),
  ("喜","xǐ","to like; joy","喜欢","xǐ huan","to like",
   "我喜欢吃饺子。","wǒ xǐ huan chī jiǎo zi","I like dumplings."),
  ("欢","huān","happy, merry","欢迎","huān yíng","welcome!",
   "欢迎来我们学校！","huān yíng lái wǒ men xué xiào","Welcome to our school!"),
  ("笑","xiào","to laugh, to smile","微笑","wēi xiào","a smile",
   "弟弟笑得真开心。","dì di xiào de zhēn kāi xīn","Little brother laughs so happily."),
  ("哭","kū","to cry","大哭","dà kū","to cry loudly",
   "别哭，我帮你。","bié kū wǒ bāng nǐ","Don't cry — I'll help you."),
  ("兴","xìng","excitement","高兴","gāo xìng","happy",
   "见到你真高兴。","jiàn dào nǐ zhēn gāo xìng","So happy to see you."),
  ("谢","xiè","to thank","谢谢","xiè xie","thank you",
   "谢谢老师！","xiè xie lǎo shī","Thank you, teacher!"),
  ("请","qǐng","please; to invite","请坐","qǐng zuò","please sit",
   "请再说一遍。","qǐng zài shuō yí biàn","Please say it again."),
]),
("School & learning", [
  ("学","xué","to learn","上学","shàng xué","go to school",
   "我在学中文。","wǒ zài xué zhōng wén","I'm learning Chinese."),
  ("习","xí","to practise","学习","xué xí","to study",
   "好好学习，天天向上。","hǎo hǎo xué xí tiān tiān xiàng shàng","Study well and improve every day."),
  ("校","xiào","school","学校","xué xiào","school",
   "我们学校真大。","wǒ men xué xiào zhēn dà","Our school is really big."),
  ("书","shū","book","看书","kàn shū","read a book",
   "我爱看图画书。","wǒ ài kàn tú huà shū","I love picture books."),
  ("本","běn","(counting books); root","课本","kè běn","textbook",
   "这本书真好看。","zhè běn shū zhēn hǎo kàn","This book is great."),
  ("课","kè","lesson","上课","shàng kè","class time",
   "上课了，请坐好。","shàng kè le qǐng zuò hǎo","Class is starting — sit up nicely."),
  ("同","tóng","same","同学","tóng xué","classmate",
   "我和同学一起玩。","wǒ hé tóng xué yì qǐ wán","I play with my classmates."),
  ("字","zì","character, word","汉字","hàn zì","Chinese characters",
   "这个字怎么读？","zhè gè zì zěn me dú","How do you read this character?"),
  ("文","wén","writing","中文","zhōng wén","Chinese",
   "中文课真有趣。","zhōng wén kè zhēn yǒu qù","Chinese class is fun."),
  ("语","yǔ","language","汉语","hàn yǔ","the Chinese language",
   "英语和汉语我都会。","yīng yǔ hé hàn yǔ wǒ dōu huì","I can speak both English and Chinese."),
  ("笔","bǐ","pen","毛笔","máo bǐ","brush pen",
   "我用铅笔写字。","wǒ yòng qiān bǐ xiě zì","I write with a pencil."),
  ("画","huà","to draw; a painting","画画","huà huà","draw pictures",
   "我画了一只小猫。","wǒ huà le yì zhī xiǎo māo","I drew a kitten."),
  ("考","kǎo","to take a test","考试","kǎo shì","exam",
   "考试不要紧张。","kǎo shì bú yào jǐn zhāng","Don't be nervous in the test."),
  ("试","shì","to try; a test","试试","shì shi","have a try",
   "让我试一试！","ràng wǒ shì yi shì","Let me have a try!"),
  ("教","jiāo","to teach","教书","jiāo shū","to teach",
   "爷爷教我下棋。","yé ye jiāo wǒ xià qí","Grandpa teaches me chess."),
  ("汉","hàn","Chinese (Han)","汉字","hàn zì","Chinese characters",
   "汉字真有意思。","hàn zì zhēn yǒu yì si","Chinese characters are fascinating."),
]),
("Position & direction", [
  ("上","shàng","up; on","上面","shàng miàn","on top",
   "书在桌子上。","shū zài zhuō zi shàng","The book is on the table."),
  ("下","xià","down; under","下面","xià miàn","underneath",
   "猫在椅子下。","māo zài yǐ zi xià","The cat is under the chair."),
  ("中","zhōng","middle","中间","zhōng jiān","in the middle",
   "我站在中间。","wǒ zhàn zài zhōng jiān","I stand in the middle."),
  ("里","lǐ","inside","里面","lǐ miàn","inside",
   "鱼在水里游。","yú zài shuǐ lǐ yóu","Fish swim in the water."),
  ("外","wài","outside","外面","wài miàn","outside",
   "外面下雨了。","wài miàn xià yǔ le","It's raining outside."),
  ("面","miàn","side; face","前面","qián miàn","in front",
   "学校前面有个公园。","xué xiào qián miàn yǒu gè gōng yuán","There's a park in front of the school."),
  ("前","qián","front; before","以前","yǐ qián","before",
   "我坐在前面。","wǒ zuò zài qián miàn","I sit at the front."),
  ("后","hòu","back; after","后面","hòu miàn","behind",
   "放学后我们去玩。","fàng xué hòu wǒ men qù wán","After school we go play."),
  ("左","zuǒ","left","左手","zuǒ shǒu","left hand",
   "往左走就到了。","wǎng zuǒ zǒu jiù dào le","Turn left and you're there."),
  ("右","yòu","right","右手","yòu shǒu","right hand",
   "我用右手写字。","wǒ yòng yòu shǒu xiě zì","I write with my right hand."),
  ("东","dōng","east","东西","dōng xi","a thing",
   "太阳从东边升起。","tài yáng cóng dōng biān shēng qǐ","The sun rises in the east."),
  ("西","xī","west","西瓜","xī guā","watermelon",
   "西瓜又大又甜。","xī guā yòu dà yòu tián","The watermelon is big and sweet."),
  ("南","nán","south","南方","nán fāng","the south",
   "燕子飞向南方。","yàn zi fēi xiàng nán fāng","The swallows fly south."),
  ("北","běi","north","北京","běi jīng","Beijing",
   "北京是中国的首都。","běi jīng shì zhōng guó de shǒu dū","Beijing is China's capital."),
  ("边","biān","side","旁边","páng biān","beside",
   "小河边开满了花。","xiǎo hé biān kāi mǎn le huā","Flowers bloom by the stream."),
  ("方","fāng","direction; square","地方","dì fang","a place",
   "这个地方真美。","zhè gè dì fang zhēn měi","This place is beautiful."),
  ("远","yuǎn","far","不远","bù yuǎn","not far",
   "学校离我家不远。","xué xiào lí wǒ jiā bù yuǎn","School isn't far from my home."),
  ("近","jìn","near","附近","fù jìn","nearby",
   "我家离公园很近。","wǒ jiā lí gōng yuán hěn jìn","My home is close to the park."),
]),
("Out & about", [
  ("国","guó","country","中国","zhōng guó","China",
   "我爱中国，也爱澳大利亚。","wǒ ài zhōng guó yě ài ào dà lì yà","I love China and Australia."),
  ("城","chéng","city; wall","城市","chéng shì","city",
   "城市的晚上很亮。","chéng shì de wǎn shang hěn liàng","The city is bright at night."),
  ("房","fáng","house","房子","fáng zi","a house",
   "我的房间很干净。","wǒ de fáng jiān hěn gān jìng","My room is nice and tidy."),
  ("门","mén","door","大门","dà mén","the gate",
   "有人在敲门。","yǒu rén zài qiāo mén","Someone's knocking at the door."),
  ("车","chē","car","汽车","qì chē","car",
   "路上车真多。","lù shàng chē zhēn duō","There are so many cars on the road."),
  ("路","lù","road","马路","mǎ lù","the road",
   "过马路要看红绿灯。","guò mǎ lù yào kàn hóng lǜ dēng","Watch the lights when crossing the road."),
  ("机","jī","machine","手机","shǒu jī","mobile phone",
   "我坐飞机去中国。","wǒ zuò fēi jī qù zhōng guó","I fly to China by plane."),
  ("电","diàn","electricity","电灯","diàn dēng","electric light",
   "打雷时有闪电。","dǎ léi shí yǒu shǎn diàn","Lightning comes with thunder."),
  ("视","shì","to look at","电视","diàn shì","television",
   "少看电视，多看书。","shǎo kàn diàn shì duō kàn shū","Less TV, more books."),
  ("脑","nǎo","brain","电脑","diàn nǎo","computer",
   "爸爸在用电脑。","bà ba zài yòng diàn nǎo","Dad is using the computer."),
  ("医","yī","doctor; medicine","医生","yī shēng","doctor",
   "医生帮我看病。","yī shēng bāng wǒ kàn bìng","The doctor checks me over."),
  ("园","yuán","garden","公园","gōng yuán","park",
   "公园里花开了。","gōng yuán lǐ huā kāi le","The flowers in the park are out."),
  ("公","gōng","public","公鸡","gōng jī","rooster",
   "公共汽车来了。","gōng gòng qì chē lái le","The bus is coming."),
  ("衣","yī","clothes","衣服","yī fu","clothes",
   "天冷了，多穿衣服。","tiān lěng le duō chuān yī fu","It's cold — put on more clothes."),
  ("服","fú","clothes; to serve","舒服","shū fu","comfortable",
   "这件衣服真舒服。","zhè jiàn yī fu zhēn shū fu","These clothes are so comfy."),
  ("钱","qián","money","花钱","huā qián","spend money",
   "我把零钱存起来。","wǒ bǎ líng qián cún qǐ lái","I save up my pocket money."),
]),
("Question words", [
  ("什","shén","what (in 什么)","什么","shén me","what?",
   "这是什么？","zhè shì shén me","What's this?"),
  ("么","me","(in 什么)","什么","shén me","what?",
   "你在做什么？","nǐ zài zuò shén me","What are you doing?"),
  ("谁","shéi","who","是谁","shì shéi","who is it?",
   "门外是谁呀？","mén wài shì shéi ya","Who's at the door?"),
  ("哪","nǎ","which","哪里","nǎ lǐ","where?",
   "你住在哪里？","nǐ zhù zài nǎ lǐ","Where do you live?"),
  ("怎","zěn","how","怎么","zěn me","how?",
   "这个字怎么写？","zhè gè zì zěn me xiě","How do you write this character?"),
  ("样","yàng","kind; way","一样","yí yàng","the same",
   "我们的书包不一样。","wǒ men de shū bāo bù yí yàng","Our school bags are different."),
  ("吗","ma","(turns it into a question)","好吗","hǎo ma","okay?",
   "你吃饭了吗？","nǐ chī fàn le ma","Have you eaten?"),
  ("呢","ne","(bounces a question back)","你呢","nǐ ne","and you?",
   "我很好，你呢？","wǒ hěn hǎo nǐ ne","I'm well — and you?"),
  ("吧","ba","(a gentle suggestion)","走吧","zǒu ba","let's go!",
   "我们回家吧。","wǒ men huí jiā ba","Let's head home."),
  ("啊","a","(adds feeling)","好啊","hǎo a","sure!",
   "这朵花真香啊！","zhè duǒ huā zhēn xiāng a","This flower smells so nice!"),
  ("为","wèi","for; for the sake of","为什么","wèi shén me","why?",
   "天为什么是蓝的？","tiān wèi shén me shì lán de","Why is the sky blue?"),
  ("因","yīn","because; cause","因为","yīn wèi","because",
   "因为下雨，我们在家玩。","yīn wèi xià yǔ wǒ men zài jiā wán","Because it's raining, we play at home."),
  ("所","suǒ","(in 所以); place","所以","suǒ yǐ","so, therefore",
   "我困了，所以想睡觉。","wǒ kùn le suǒ yǐ xiǎng shuì jiào","I'm sleepy, so I want to go to bed."),
  ("以","yǐ","(in 可以 and 所以)","可以","kě yǐ","may, can",
   "我可以进来吗？","wǒ kě yǐ jìn lái ma","May I come in?"),
  ("如","rú","if; like","如果","rú guǒ","if",
   "如果晴天，我们去公园。","rú guǒ qíng tiān wǒ men qù gōng yuán","If it's sunny, we'll go to the park."),
]),
("Little glue words", [
  ("的","de","(links describing words)","我的","wǒ de","my, mine",
   "这是我的书包。","zhè shì wǒ de shū bāo","This is my school bag."),
  ("了","le","(something happened)","下雨了","xià yǔ le","it's raining!",
   "花开了，春天来了。","huā kāi le chūn tiān lái le","The flowers are out — spring is here!"),
  ("是","shì","to be","是的","shì de","yes",
   "我是小学生。","wǒ shì xiǎo xué shēng","I'm a primary school student."),
  ("不","bù","not","不是","bú shì","is not",
   "我不怕黑。","wǒ bú pà hēi","I'm not afraid of the dark."),
  ("没","méi","not have","没有","méi yǒu","there isn't",
   "今天没有下雨。","jīn tiān méi yǒu xià yǔ","It didn't rain today."),
  ("有","yǒu","to have","有用","yǒu yòng","useful",
   "我有一个妹妹。","wǒ yǒu yí gè mèi mei","I have a little sister."),
  ("着","zhe","(happening right now)","看着","kàn zhe","watching",
   "妹妹笑着说好。","mèi mei xiào zhe shuō hǎo","Little sister says yes with a smile."),
  ("过","guò","to pass; (done before)","过年","guò nián","Chinese New Year",
   "我去过北京。","wǒ qù guò běi jīng","I've been to Beijing."),
  ("得","de","(links action and how)","跑得快","pǎo de kuài","runs fast",
   "哥哥跑得真快。","gē ge pǎo de zhēn kuài","Big brother runs so fast."),
  ("和","hé","and","我和你","wǒ hé nǐ","you and me",
   "我和弟弟玩积木。","wǒ hé dì di wán jī mù","My little brother and I play blocks."),
  ("也","yě","also","我也是","wǒ yě shì","me too",
   "你去，我也去。","nǐ qù wǒ yě qù","If you go, I'll go too."),
  ("都","dōu","all","都是","dōu shì","all are",
   "我们都爱唱歌。","wǒ men dōu ài chàng gē","We all love singing."),
  ("还","hái","still; also","还有","hái yǒu","and also",
   "我还有一个问题。","wǒ hái yǒu yí gè wèn tí","I have one more question."),
  ("就","jiù","right away; then","就是","jiù shì","exactly",
   "写完作业就去玩。","xiě wán zuò yè jiù qù wán","Finish homework, then play."),
  ("只","zhǐ","only","只有","zhǐ yǒu","only",
   "我只有一块糖。","wǒ zhǐ yǒu yí kuài táng","I only have one sweet."),
  ("很","hěn","very","很好","hěn hǎo","very good",
   "今天我很开心。","jīn tiān wǒ hěn kāi xīn","I'm very happy today."),
  ("太","tài","too (much)","太好了","tài hǎo le","wonderful!",
   "这个故事太好听了！","zhè gè gù shi tài hǎo tīng le","This story is wonderful!"),
  ("最","zuì","the most","最好","zuì hǎo","the best",
   "我最喜欢星期六。","wǒ zuì xǐ huan xīng qī liù","Saturday is my favourite."),
  ("更","gèng","even more","更大","gèng dà","even bigger",
   "哥哥比我更高。","gē ge bǐ wǒ gèng gāo","Big brother is even taller than me."),
  ("又","yòu","again","又来了","yòu lái le","here we go again",
   "苹果又大又红。","píng guǒ yòu dà yòu hóng","The apple is big and red."),
  ("对","duì","right, correct","对不起","duì bu qǐ","sorry",
   "你答对了！","nǐ dá duì le","You got it right!"),
]),
("This & that", [
  ("在","zài","at, in","在家","zài jiā","at home",
   "妈妈在厨房做饭。","mā ma zài chú fáng zuò fàn","Mum's cooking in the kitchen."),
  ("这","zhè","this","这里","zhè lǐ","here",
   "这是我的家。","zhè shì wǒ de jiā","This is my home."),
  ("那","nà","that","那里","nà lǐ","there",
   "那是谁的书？","nà shì shéi de shū","Whose book is that?"),
  ("每","měi","every","每天","měi tiān","every day",
   "我每天都读书。","wǒ měi tiān dōu dú shū","I read every day."),
  ("把","bǎ","handle; (grammar helper)","把手","bǎ shǒu","a handle",
   "请把门关上。","qǐng bǎ mén guān shàng","Please close the door."),
  ("被","bèi","quilt; (by)","被子","bèi zi","a quilt",
   "饼干被弟弟吃了。","bǐng gān bèi dì di chī le","The biscuits got eaten by little brother."),
  ("比","bǐ","to compare","比一比","bǐ yi bǐ","compare them!",
   "我比去年高了。","wǒ bǐ qù nián gāo le","I'm taller than last year."),
  ("跟","gēn","with; to follow","跟我学","gēn wǒ xué","learn with me",
   "请跟我读。","qǐng gēn wǒ dú","Read after me."),
  ("从","cóng","from","从小","cóng xiǎo","ever since little",
   "我从家走到学校。","wǒ cóng jiā zǒu dào xué xiào","I walk from home to school."),
]),
("Can & must", [
  ("会","huì","can (know how to)","会写字","huì xiě zì","can write characters",
   "我会唱这首歌。","wǒ huì chàng zhè shǒu gē","I can sing this song."),
  ("能","néng","can (be able to)","不能","bù néng","can't",
   "明天能去公园吗？","míng tiān néng qù gōng yuán ma","Can we go to the park tomorrow?"),
  ("要","yào","to want; must","想要","xiǎng yào","to want",
   "我要学好中文。","wǒ yào xué hǎo zhōng wén","I want to learn Chinese well."),
  ("让","ràng","to let","让一让","ràng yi ràng","excuse me — make way",
   "妈妈让我早点睡。","mā ma ràng wǒ zǎo diǎn shuì","Mum tells me to sleep early."),
  ("别","bié","don't","别哭","bié kū","don't cry",
   "别忘了带课本。","bié wàng le dài kè běn","Don't forget your textbook."),
  ("可","kě","can; (but)","可是","kě shì","but",
   "外面冷，可是很好玩。","wài miàn lěng kě shì hěn hǎo wán","It's cold outside, but such fun."),
  ("应","yīng","should","应该","yīng gāi","should",
   "小朋友应该早睡。","xiǎo péng yǒu yīng gāi zǎo shuì","Children should sleep early."),
  ("该","gāi","should","应该","yīng gāi","should",
   "该睡觉了。","gāi shuì jiào le","Time for bed."),
  ("成","chéng","to become","完成","wán chéng","to finish",
   "我想成为老师。","wǒ xiǎng chéng wéi lǎo shī","I want to become a teacher."),
  ("完","wán","to finish","吃完","chī wán","eat it all up",
   "我吃完饭了。","wǒ chī wán fàn le","I've finished eating."),
  ("经","jīng","to pass through","已经","yǐ jīng","already",
   "我已经七岁了。","wǒ yǐ jīng qī suì le","I'm already seven."),
  ("已","yǐ","already","已经","yǐ jīng","already",
   "天已经黑了。","tiān yǐ jīng hēi le","It's already dark."),
  ("正","zhèng","just now; upright","正在","zhèng zài","right now",
   "我们正在上课。","wǒ men zhèng zài shàng kè","We're in class right now."),
]),
]

# ---------------------------------------------------------------------------
# The original twelve hand-written example sentences (and origin stories) —
# preserved verbatim from the first edition of char-data.js.
# ---------------------------------------------------------------------------
OVERRIDES = {
"人": {"origin":"Looks like a person walking — two legs caught mid-stride.",
  "ex":{"seg":[["一","yí"],["个","gè"],["人","rén"],["，",""],["两","liǎng"],["只","zhī"],["手","shǒu"],["。",""]],"en":"One person, two hands."}},
"口": {"origin":"Looks like an open mouth — the simplest little picture there is.",
  "ex":{"seg":[["张","zhāng"],["口","kǒu"],["说","shuō"],["“",""],["你","nǐ"],["好","hǎo"],["”",""],["。",""]],"en":"Open your mouth and say “hello”."}},
"大": {"origin":"A person 大 standing with both arms flung wide — as big as can be.",
  "ex":{"seg":[["大","dà"],["象","xiàng"],["的","de"],["耳","ěr"],["朵","duo"],["真","zhēn"],["大","dà"],["。",""]],"en":"An elephant's ears are really big."}},
"小": {"origin":"The mirror of 大 (big): 小 is small — a neat pair of opposites.",
  "ex":{"seg":[["小","xiǎo"],["鸟","niǎo"],["在","zài"],["树","shù"],["上","shàng"],["唱","chàng"],["歌","gē"],["。",""]],"en":"A little bird is singing up in the tree."}},
"你": {"origin":"Left side 亻 is a person; the rest carries the sound. 你 is 'you' — the person across from me.",
  "ex":{"seg":[["你","nǐ"],["叫","jiào"],["什","shén"],["么","me"],["名","míng"],["字","zi"],["？",""],["我","wǒ"],["叫","jiào"],["小","xiǎo"],["华","huá"],["。",""]],"en":"What's your name? Mine is Xiaohua."}},
"好": {"origin":"女 (woman) cradling 子 (a child) — together they mean good.",
  "ex":{"seg":[["妈","mā"],["妈","ma"],["做","zuò"],["的","de"],["饭","fàn"],["，",""],["好","hǎo"],["吃","chī"],["极","jí"],["了","le"],["。",""]],"en":"The food Mum makes is so good."}},
"家": {"origin":"A roof 宀 with a 豕 (pig) sheltered beneath it — a home.",
  "ex":{"seg":[["放","fàng"],["学","xué"],["了","le"],["，",""],["我","wǒ"],["们","men"],["回","huí"],["家","jiā"],["吧","ba"],["。",""]],"en":"School's out — let's head home."}},
"水": {"origin":"The flowing three-drop radical 氵 grows from 水 — it runs through 河 (river), 海 (sea), 洗 (wash).",
  "ex":{"seg":[["小","xiǎo"],["鱼","yú"],["离","lí"],["不","bu"],["开","kāi"],["水","shuǐ"],["。",""]],"en":"A little fish can't live without water."}},
"鱼": {"origin":"A whole fish: ⺈ is the head, 田 the body, 一 the tail.",
  "ex":{"seg":[["小","xiǎo"],["猫","māo"],["爱","ài"],["吃","chī"],["鱼","yú"],["。",""]],"en":"Kittens love to eat fish."}},
"马": {"origin":"The same 马 gallops inside 妈 (mum): 女 + 马.",
  "ex":{"seg":[["马","mǎ"],["儿","ér"],["在","zài"],["草","cǎo"],["原","yuán"],["上","shàng"],["跑","pǎo"],["得","de"],["快","kuài"],["。",""]],"en":"The horse runs fast across the meadow."}},
"看": {"origin":"A hand 手 raised over an eye 目 — shading your eyes to look far.",
  "ex":{"seg":[["看","kàn"],["，",""],["天","tiān"],["上","shàng"],["有","yǒu"],["一","yì"],["朵","duǒ"],["云","yún"],["。",""]],"en":"Look — there's a cloud in the sky."}},
"吃": {"origin":"Built on the mouth radical 口 — you 吃 (eat) with your mouth.",
  "ex":{"seg":[["大","dà"],["家","jiā"],["一","yì"],["起","qǐ"],["吃","chī"],["饺","jiǎo"],["子","zi"],["。",""]],"en":"Everyone eats dumplings together."}},
}

# Hand-tuned origin stories for characters whose makemeahanzi etymology is
# missing, too dry, or too scholarly for a children's page.
ORIGIN_FIX = {
"头": "Simplified from 頭, where 页 means head — two little drops sit on top of 大 (big): the big part up top is your head.",
"体": "A person 亻 beside 本 (root) — your body is a person's root and trunk.",
"声": "Simplified from 聲 — a stone chime being struck, ringing out a sound.",
"它": "Long, long ago this was a drawing of a snake! It was borrowed to mean 'it'.",
"他": "A person 亻 plus 也 (also) — an extra person: him.",
"师": "Once the word for a whole army — and for the masters who led it. Today it lives in 老师, your teacher.",
"一": "One single stroke — the number one, and the very first character most children ever write.",
"六": "Early forms looked like a little hut: a roof with legs. Count it on one hand — six!",
"七": "Looks like 十 with the bottom stroke bent up — an old cross-cut sign that came to mean seven.",
"十": "One stroke across, one stroke down — a perfect crossing for a perfectly round number: ten.",
"千": "A slanting stroke over 十 (ten) — ten upon ten upon ten makes a thousand.",
"万": "Once a picture of a scorpion! It was borrowed long ago for the huge number ten thousand.",
"时": "The sun 日 next to 寸 (a tiny measure) — the sun's journey measured out in little steps: time.",
"风": "Simplified from 風 — a billowing sail with a swirl tucked inside: wind you can almost see.",
"气": "Three wavy lines of rising steam — air and breath drifting upward.",
"雪": "Rain 雨 that you can sweep up with a hand 彐 — snow!",
"鸟": "Simplified from 鳥 — a perched bird, with a dot for its eye.",
"朋": "Two moons 月 side by side — friends sticking together.",
"去": "A figure striding away from an opening 厶 below — off it goes.",
"关": "Simplified from 關 — a bar laid across a gate 門, shutting it tight.",
"听": "A mouth 口 on the left: someone speaks, you listen. The old form 聽 even had an ear 耳 inside.",
"写": "Under the cover 冖 there once perched a little magpie — its character was borrowed for 'to write'.",
"觉": "见 (see) under a little roof — what you 'see' with your eyes closed: sleep and feelings.",
"用": "Said to be an old picture of a bucket — a handy thing you use every day.",
"买": "Simplified from 買 — a net scooping up shells, the coins of long ago. Shopping!",
"事": "A hand holding a writing brush, hard at work — busy with matters and tasks.",
"哭": "Two crying eyes 口口 above a dog 犬 howling — waaah!",
"笑": "Bamboo ⺮ bending in the wind above a person 夭 — bent over double with laughter.",
"欢": "An open mouth 欠 beside a hand 又 — cheering out loud with joy.",
"兴": "Simplified from 興 — many hands lifting something up together: everyone excited.",
"习": "Half a pair of wings 羽 — a young bird practising its flying, again and again.",
"汉": "Simplified from 漢 — the water radical 氵 names the Han River, then the Han people, then Chinese itself.",
"前": "Long ago: a foot on a boat, drifting ahead — forward, in front.",
"后": "A figure with a mouth 口 below — an ancient title for a queen, later borrowed for 'behind, after'.",
"右": "A hand above a mouth 口 — the right hand, the one most people eat and write with.",
"方": "An old picture of a knife with a handle — borrowed for 'square' and 'direction'.",
"边": "The walking radical 辶 — walk as far as you can and you reach the edge, the side.",
"脑": "The flesh radical ⺼ beside a little drawing of hair above a head — your brain.",
"医": "An arrow 矢 in an open box 匸 — the doctor's case, ready to pull arrows out and make you better.",
"色": "Find 色 at the end of every colour word: 红色, 黄色, 蓝色 — it is 'colour' itself.",
"么": "A tiny twist of thread — a tiny word that tags along after 什 to ask 'what?'",
"为": "Simplified from 爲 — a hand leading an elephant to work! Now it mostly means 'for'.",
"因": "A person 大 lying on a mat 囗 — the thing everything rests on: the reason, the cause.",
"以": "An old drawing of someone carrying a tool — to use; you'll meet it in 可以 (can).",
"如": "女 and 口 side by side — borrowed long ago for 'if'. You'll meet it in 如果.",
"的": "白 (white) plus 勺 (a ladle) for the sound — it once meant 'bright'; now it's the busiest little word in Chinese.",
"有": "A hand 𠂇 holding meat ⺼ — food in hand means you have something.",
"着": "It grew out of 著 — now it sticks to an action word to say it's happening right now.",
"也": "An old picture — maybe a snake, maybe a basin — borrowed long ago for 'also'.",
"还": "The walking radical 辶 under 不 — turning around and coming back; still on the way.",
"更": "An old picture of a hand making a change — now it cranks things up: even more!",
"这": "The walking radical 辶 carrying 文 — simplified from 這, the one that walks right up to you: this!",
"那": "A town 阝 in the distance — point at it: that one, over there.",
"每": "Look for 母 (mother) inside, wearing a little sprout on top — every, each.",
"是": "The sun 日 above a foot walking straight ahead — exactly right: 'to be'.",
"可": "A mouth 口 saying yes — can do! You'll find it doubled in 哥 (big brother).",
"别": "另 (other) plus a knife 刂 — cut apart, set aside: don't!",
"应": "Simplified from 應 — under the shelter 广, what ought to be done.",
"成": "A blade 戈 striking true — the job is done, complete; it has become.",
"已": "Almost 己 — but the top is closed in: the task is already done. Compare the open 己 (self)!",
}

# ---------------------------------------------------------------------------
# Radical → English name (Kangxi radicals that occur in this set).
# ---------------------------------------------------------------------------
RAD_EN = {
"人":"person","亻":"person","儿":"legs","入":"enter","八":"eight","刀":"knife",
"力":"strength","又":"right hand","口":"mouth","囗":"enclosure","土":"earth",
"夕":"evening","大":"big","女":"woman","子":"child","宀":"roof","寸":"inch",
"小":"small","⺌":"small","尸":"body","山":"mountain","巾":"cloth","广":"shelter",
"廴":"long stride","彳":"step","心":"heart","忄":"heart","戈":"halberd",
"户":"door","手":"hand","扌":"hand","攴":"tap","攵":"tap","文":"writing",
"斤":"axe","方":"square","无":"not","日":"sun","曰":"say","月":"moon",
"木":"tree","欠":"yawn","止":"stop","母":"mother","毛":"fur","气":"breath",
"水":"water","氵":"water","火":"fire","灬":"fire","爪":"claw","爫":"claw",
"父":"father","牛":"cow","犬":"dog","犭":"dog","玉":"jade","王":"king",
"田":"field","白":"white","皮":"skin","目":"eye","石":"stone","示":"altar",
"礻":"altar","禾":"grain","立":"stand","竹":"bamboo","⺮":"bamboo","米":"rice",
"糸":"silk","纟":"silk","耳":"ear","聿":"brush","肉":"meat","月⺼":"flesh",
"自":"self","至":"arrive","舌":"tongue","色":"colour","艸":"grass","艹":"grass",
"虫":"insect","行":"go","衣":"clothes","衤":"clothes","见":"see","言":"speech",
"讠":"speech","贝":"shell","走":"walk","足":"foot","⻊":"foot","身":"body",
"车":"cart","辵":"walk","⻌":"walk","邑":"town","阝":"mound or town","金":"metal",
"钅":"metal","门":"gate","隹":"short-tailed bird","雨":"rain","页":"head",
"风":"wind","飞":"fly","食":"eat","饣":"eat","马":"horse","高":"tall",
"鸟":"bird","鱼":"fish","龙":"dragon","麦":"wheat","黑":"black","鼠":"mouse",
"一":"one","丨":"line","丶":"dot","丿":"slant","乙":"hook","亅":"hook",
"二":"two","亠":"lid","冂":"open box","冖":"cover","冫":"ice","几":"table",
"凵":"open box","勹":"wrap","匕":"spoon","匚":"box","十":"ten","卜":"divine",
"卩":"seal","厂":"cliff","厶":"private","干":"dry","幺":"tiny","弓":"bow",
"彐":"snout","彡":"hair strokes","工":"work","己":"self","巳":"snake",
"廾":"hands","弋":"dart","夂":"go slowly","士":"scholar","老":"old","耂":"old",
"而":"and","羊":"sheep","⺶":"sheep","羽":"feather","西":"west",
"覀":"cover","角":"horn","谷":"valley","豕":"pig","豸":"badger","赤":"red",
"辛":"bitter","辰":"dawn","酉":"wine jar","里":"village","青":"green",
"非":"not","面":"face","革":"leather","音":"sound","骨":"bone","鬼":"ghost",
"麻":"hemp","黄":"yellow","鼓":"drum","齐":"even","龺":"sunrise",
"牜":"cow","𥫗":"bamboo","龰":"stop","殳":"club",
"斗":"dipper","片":"slice","爿":"split wood","疋":"bolt of cloth","疒":"sickness",
"癶":"footsteps","皿":"dish","矛":"spear","矢":"arrow","禸":"track","穴":"cave",
"网":"net","罒":"net","缶":"jar","耒":"plough","臣":"minister","舟":"boat",
"艮":"mountain ridge","虍":"tiger","血":"blood","襾":"cover","豆":"bean",
"貝":"shell","釆":"distinguish","長":"long","韦":"leather",
"飠":"eat","鬥":"fight","鹵":"salt","龶":"life","生":"life","长":"long",
"辶":"walk","丷":"eight","刂":"knife","用":"use","⺼":"flesh","匸":"box",
"乚":"hook","尢":"lame","比":"compare","能":"able",
}

# Correct curated readings that differ from the first reading listed in the
# makemeahanzi dictionary (e.g. 长 zhǎng/cháng) — checked by hand.
PY_OK = {"地", "长", "觉", "谁"}

# ---------------------------------------------------------------------------
def fetch(name, override):
    if override:
        return override
    cache = os.path.join(ROOT, ".cache")
    os.makedirs(cache, exist_ok=True)
    path = os.path.join(cache, name)
    if not os.path.exists(path):
        print("downloading " + MMAH + name + " …")
        urllib.request.urlretrieve(MMAH + name, path)
    return path

def load_jsonl(path, key="character"):
    out = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                rec = json.loads(line)
                out[rec[key]] = rec
    return out

def strip_tones(s):
    s = unicodedata.normalize("NFD", s)
    return "".join(c for c in s if not unicodedata.combining(c)).replace("ü","u").lower()

def sentence_case(s):
    s = re.sub(r"\s+", " ", s).strip().rstrip(".") + "."
    return s[0].upper() + s[1:]

def is_cjk(c):
    return "㐀" <= c <= "鿿"

def seg_from(text, py):
    """Pair every character of `text` with a pinyin token; punctuation
    (non-CJK) gets an empty string. Token count must match exactly."""
    toks = py.split(" ")
    seg, i = [], 0
    for c in text:
        if is_cjk(c):
            seg.append([c, toks[i]]); i += 1
        else:
            seg.append([c, ""])
    assert i == len(toks), "pinyin/text mismatch: %s | %s" % (text, py)
    return seg

def origin_for(ch, en, drec):
    if ch in ORIGIN_FIX:
        return ORIGIN_FIX[ch]
    ety = (drec or {}).get("etymology") or {}
    t = ety.get("type")
    hint = (ety.get("hint") or "").strip().replace("pronuncation", "pronunciation")
    if t == "pictographic" and hint:
        return sentence_case("A little picture: " + hint[0].lower() + hint[1:])
    if t == "ideographic" and hint:
        return sentence_case("Picture it: " + hint[0].lower() + hint[1:])
    if t == "pictophonetic":
        sem, ph = ety.get("semantic"), ety.get("phonetic")
        if sem and ph:
            h = (" (" + hint + ")") if hint else ""
            return sem + h + " hints at the meaning, and " + ph + " lends its sound — together they make " + ch + "."
        if ph:
            return "The sound comes from " + ph + " — listen for it when you say " + ch + "."
    rad = (drec or {}).get("radical", "")
    if rad and rad in RAD_EN:
        return "Spot the " + rad + " (" + RAD_EN[rad] + ") radical tucked inside — a clue to what it means."
    return "One of the very first characters children learn — watch the strokes and trace it in the air."

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--graphics")
    ap.add_argument("--dict", dest="dict_")
    args = ap.parse_args()

    gfx = load_jsonl(fetch("graphics.txt", args.graphics))
    dic = load_jsonl(fetch("dictionary.txt", args.dict_))

    flat, seen = [], set()
    for group, entries in GROUPS:
        for e in entries:
            assert e[0] not in seen, "duplicate character: " + e[0]
            seen.add(e[0])
            flat.append((group,) + e)
    assert len(flat) == 300, "expected 300 characters, got %d" % len(flat)

    data, problems = [], []
    for group, ch, py, en, word, wordpy, worden, sen, senpy, senen in flat:
        g, drec = gfx.get(ch), dic.get(ch)
        if not g:
            problems.append("no graphics for " + ch); continue
        if not drec:
            problems.append("no dictionary entry for " + ch)
        # sanity-check curated pinyin against the dictionary
        dpys = [strip_tones(p) for p in (drec or {}).get("pinyin", [])]
        if dpys and ch not in PY_OK and strip_tones(py) not in dpys:
            problems.append("pinyin mismatch %s: %s not in %s" % (ch, py, dpys))
        rad = (drec or {}).get("radical", "")
        if rad and rad not in RAD_EN:
            problems.append("no English name for radical %s (in %s)" % (rad, ch))
        origin = OVERRIDES[ch]["origin"] if ch in OVERRIDES else origin_for(ch, en, drec)
        wd = {"seg": seg_from(word, wordpy), "en": worden}
        if sen is None:
            ex = OVERRIDES[ch]["ex"]
        else:
            ex = {"seg": seg_from(sen, senpy), "en": senen}
        data.append({
            "ch": ch, "py": py, "en": en,
            "strokes": len(g["strokes"]),
            "radical": rad or ch, "radEn": RAD_EN.get(rad, ""),
            "group": group, "origin": origin, "word": wd, "ex": ex,
            "s": g["strokes"],
            "m": [[[int(x), int(y)] for x, y in m] for m in g["medians"]],
        })

    if problems:
        print("\n".join(problems), file=sys.stderr)
        sys.exit(1)

    header = (
"/* characters data — Casey Chinese School character explorer.\n"
"   GENERATED by scripts/build-char-data.py — edit the table there, not this file.\n"
"   300 common characters in themed groups; glosses, common words, example\n"
"   sentences and origin notes curated for the school. Stroke paths/medians:\n"
"   makemeahanzi (https://github.com/skishore/makemeahanzi, Arphic Public\n"
"   License), 1024 Y-up space. Self-contained / evergreen. */\n")
    body = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(header + "window.CHAR_DATA = " + body + ";\n")
    print("wrote %s: %d characters, %d groups, %.0f KB" %
          (os.path.relpath(OUT, ROOT), len(data), len(GROUPS), len(body) / 1024))

if __name__ == "__main__":
    main()
