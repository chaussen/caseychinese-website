#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Build learn/char-data.js for the Character Explorer (characters.html).

Merges the curated 300-character content table below (pinyin, kid-friendly
gloss, theme group, example word) with stroke paths + medians from the
makemeahanzi project (https://github.com/skishore/makemeahanzi).

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
# Entry: (char, pinyin, gloss, example word, per-char pinyin, word gloss)
# The example fields are None for the original twelve characters, whose
# hand-written origin stories and full example sentences (OVERRIDES below)
# are kept as-is.
# ---------------------------------------------------------------------------
GROUPS = [
("Me & my body", [
  ("人","rén","person",None,None,None),
  ("大","dà","big",None,None,None),
  ("小","xiǎo","small",None,None,None),
  ("口","kǒu","mouth",None,None,None),
  ("手","shǒu","hand","拍手","pāi shǒu","clap your hands"),
  ("心","xīn","heart","小心","xiǎo xīn","be careful"),
  ("头","tóu","head","头发","tóu fa","hair"),
  ("目","mù","eye","目光","mù guāng","a look, a gaze"),
  ("耳","ěr","ear","耳朵","ěr duo","ear"),
  ("眼","yǎn","eye","眼睛","yǎn jing","eyes"),
  ("身","shēn","body","身体","shēn tǐ","body, health"),
  ("体","tǐ","body","体育","tǐ yù","sport, PE"),
  ("自","zì","self","自己","zì jǐ","oneself"),
  ("己","jǐ","oneself","自己","zì jǐ","oneself"),
  ("力","lì","strength","用力","yòng lì","use your strength"),
  ("声","shēng","sound, voice","大声","dà shēng","loudly"),
]),
("Family & people", [
  ("你","nǐ","you",None,None,None),
  ("我","wǒ","I, me","我们","wǒ men","we, us"),
  ("他","tā","he","他们","tā men","they"),
  ("她","tā","she","她们","tā men","they (girls and women)"),
  ("它","tā","it","它们","tā men","they (animals and things)"),
  ("们","men","(makes words plural)","我们","wǒ men","we, us"),
  ("好","hǎo","good",None,None,None),
  ("妈","mā","mum","妈妈","mā ma","Mum"),
  ("爸","bà","dad","爸爸","bà ba","Dad"),
  ("子","zǐ","child","孩子","hái zi","child"),
  ("女","nǚ","woman, girl","女儿","nǚ ér","daughter"),
  ("男","nán","man, boy","男孩","nán hái","boy"),
  ("孩","hái","child","女孩","nǚ hái","girl"),
  ("儿","ér","child, son","儿子","ér zi","son"),
  ("家","jiā","family, home",None,None,None),
  ("朋","péng","friend","朋友","péng you","friend"),
  ("友","yǒu","friend","好友","hǎo yǒu","good friend"),
  ("老","lǎo","old","老师","lǎo shī","teacher"),
  ("师","shī","teacher","老师","lǎo shī","teacher"),
  ("生","shēng","to be born; student","学生","xué sheng","student"),
  ("名","míng","name","名字","míng zi","name"),
  ("王","wáng","king","国王","guó wáng","king"),
]),
("Numbers & counting", [
  ("一","yī","one","一百","yì bǎi","one hundred"),
  ("二","èr","two","二月","èr yuè","February"),
  ("三","sān","three","三个","sān gè","three of them"),
  ("四","sì","four","四季","sì jì","the four seasons"),
  ("五","wǔ","five","五星","wǔ xīng","five stars"),
  ("六","liù","six","六岁","liù suì","six years old"),
  ("七","qī","seven","七天","qī tiān","seven days — a week"),
  ("八","bā","eight","八点","bā diǎn","eight o'clock"),
  ("九","jiǔ","nine","九月","jiǔ yuè","September"),
  ("十","shí","ten","十分","shí fēn","completely — ten parts full"),
  ("百","bǎi","hundred","百花","bǎi huā","a hundred flowers"),
  ("千","qiān","thousand","一千","yì qiān","one thousand"),
  ("万","wàn","ten thousand","一万","yí wàn","ten thousand"),
  ("两","liǎng","two (of something)","两个","liǎng gè","two of them"),
  ("几","jǐ","how many","几个","jǐ gè","how many?"),
  ("个","gè","(counting word)","一个","yí gè","one of them"),
  ("半","bàn","half","一半","yí bàn","half"),
  ("第","dì","(makes 'first, second…')","第一","dì yī","number one, first"),
  ("数","shù","number","数学","shù xué","maths"),
  ("多","duō","many","很多","hěn duō","lots"),
  ("少","shǎo","few","多少","duō shǎo","how many?"),
]),
("Time & days", [
  ("天","tiān","sky; day","今天","jīn tiān","today"),
  ("日","rì","sun; day","生日","shēng rì","birthday"),
  ("月","yuè","moon; month","月亮","yuè liang","the moon"),
  ("年","nián","year","新年","xīn nián","New Year"),
  ("时","shí","time; hour","时间","shí jiān","time"),
  ("候","hòu","time, moment","时候","shí hou","a time, a moment"),
  ("分","fēn","minute; to divide","分钟","fēn zhōng","minute"),
  ("点","diǎn","o'clock; dot","三点","sān diǎn","three o'clock"),
  ("现","xiàn","now; to appear","现在","xiàn zài","now"),
  ("今","jīn","now, this","今年","jīn nián","this year"),
  ("明","míng","bright; next","明天","míng tiān","tomorrow"),
  ("昨","zuó","yesterday","昨天","zuó tiān","yesterday"),
  ("早","zǎo","early; morning","早上","zǎo shang","morning"),
  ("晚","wǎn","late; evening","晚上","wǎn shang","evening"),
  ("期","qī","period of time","星期","xīng qī","week"),
  ("常","cháng","often","常常","cháng cháng","often"),
  ("再","zài","again","再见","zài jiàn","goodbye — see you again"),
]),
("Nature & weather", [
  ("水","shuǐ","water",None,None,None),
  ("火","huǒ","fire","火车","huǒ chē","train"),
  ("山","shān","mountain","爬山","pá shān","climb a mountain"),
  ("田","tián","field","田野","tián yě","open fields"),
  ("土","tǔ","earth, soil","土地","tǔ dì","land"),
  ("木","mù","wood; tree","木头","mù tou","wood"),
  ("树","shù","tree","大树","dà shù","a big tree"),
  ("花","huā","flower","开花","kāi huā","to bloom"),
  ("草","cǎo","grass","小草","xiǎo cǎo","little grass"),
  ("风","fēng","wind","大风","dà fēng","a strong wind"),
  ("雨","yǔ","rain","下雨","xià yǔ","to rain"),
  ("雪","xuě","snow","下雪","xià xuě","to snow"),
  ("云","yún","cloud","白云","bái yún","white clouds"),
  ("气","qì","air; breath","天气","tiān qì","weather"),
  ("阳","yáng","sun, sunshine","太阳","tài yáng","the sun"),
  ("光","guāng","light","阳光","yáng guāng","sunshine"),
  ("星","xīng","star","星星","xīng xing","stars"),
  ("海","hǎi","sea","大海","dà hǎi","the sea"),
  ("河","hé","river","小河","xiǎo hé","a stream"),
  ("地","dì","ground, earth","草地","cǎo dì","grassy lawn"),
]),
("Animals", [
  ("鱼","yú","fish",None,None,None),
  ("马","mǎ","horse",None,None,None),
  ("鸟","niǎo","bird","小鸟","xiǎo niǎo","little bird"),
  ("鸡","jī","chicken","小鸡","xiǎo jī","chick"),
  ("牛","niú","cow, ox","奶牛","nǎi niú","dairy cow"),
  ("羊","yáng","sheep","山羊","shān yáng","goat"),
  ("狗","gǒu","dog","小狗","xiǎo gǒu","puppy"),
  ("猫","māo","cat","小猫","xiǎo māo","kitten"),
  ("龙","lóng","dragon","恐龙","kǒng lóng","dinosaur"),
]),
("Food & drink", [
  ("吃","chī","to eat",None,None,None),
  ("喝","hē","to drink","喝水","hē shuǐ","drink water"),
  ("饭","fàn","rice; a meal","吃饭","chī fàn","have a meal"),
  ("菜","cài","vegetables; a dish","青菜","qīng cài","green veggies"),
  ("米","mǐ","rice (grains)","米饭","mǐ fàn","cooked rice"),
  ("肉","ròu","meat","牛肉","niú ròu","beef"),
  ("果","guǒ","fruit","苹果","píng guǒ","apple"),
  ("蛋","dàn","egg","鸡蛋","jī dàn","egg"),
  ("奶","nǎi","milk","牛奶","niú nǎi","milk"),
  ("包","bāo","bun; bag","面包","miàn bāo","bread"),
  ("糖","táng","sugar; sweets","糖果","táng guǒ","sweets"),
]),
("Colours & describing", [
  ("红","hóng","red","红色","hóng sè","red"),
  ("黄","huáng","yellow","黄色","huáng sè","yellow"),
  ("蓝","lán","blue","蓝天","lán tiān","blue sky"),
  ("绿","lǜ","green","绿色","lǜ sè","green"),
  ("白","bái","white","白色","bái sè","white"),
  ("黑","hēi","black","黑色","hēi sè","black"),
  ("色","sè","colour","彩色","cǎi sè","colourful"),
  ("新","xīn","new","新书","xīn shū","a new book"),
  ("高","gāo","tall, high","高山","gāo shān","high mountains"),
  ("长","cháng","long; (zhǎng) to grow","长城","cháng chéng","the Great Wall"),
  ("真","zhēn","real; really","真好","zhēn hǎo","really good!"),
  ("美","měi","beautiful","美丽","měi lì","beautiful"),
  ("快","kuài","fast","快乐","kuài lè","happy"),
  ("慢","màn","slow","慢慢","màn màn","slowly"),
  ("冷","lěng","cold","很冷","hěn lěng","very cold"),
  ("热","rè","hot","热水","rè shuǐ","hot water"),
  ("亮","liàng","bright","月亮","yuè liang","the moon"),
]),
("Come & go", [
  ("来","lái","to come","过来","guò lái","come over"),
  ("去","qù","to go","去学校","qù xué xiào","go to school"),
  ("走","zǒu","to walk","走路","zǒu lù","to walk"),
  ("跑","pǎo","to run","跑步","pǎo bù","to go running"),
  ("飞","fēi","to fly","起飞","qǐ fēi","to take off"),
  ("坐","zuò","to sit","坐下","zuò xià","sit down"),
  ("站","zhàn","to stand; station","车站","chē zhàn","bus stop, station"),
  ("进","jìn","to go in","进来","jìn lái","come in"),
  ("出","chū","to go out","出去","chū qù","go out"),
  ("回","huí","to return","回家","huí jiā","go home"),
  ("起","qǐ","to get up, to rise","起床","qǐ chuáng","get out of bed"),
  ("开","kāi","to open","开门","kāi mén","open the door"),
  ("关","guān","to close","关门","guān mén","close the door"),
  ("到","dào","to arrive","到家","dào jiā","arrive home"),
]),
("Everyday actions", [
  ("看","kàn","to look, to read",None,None,None),
  ("听","tīng","to listen","听见","tīng jiàn","to hear"),
  ("说","shuō","to speak","说话","shuō huà","to talk"),
  ("话","huà","words, speech","电话","diàn huà","telephone"),
  ("读","dú","to read","读书","dú shū","to read books"),
  ("写","xiě","to write","写字","xiě zì","write characters"),
  ("睡","shuì","to sleep","睡觉","shuì jiào","go to sleep"),
  ("觉","jiào","a sleep; (jué) to feel","睡觉","shuì jiào","go to sleep"),
  ("做","zuò","to do, to make","做饭","zuò fàn","to cook"),
  ("作","zuò","to do (work)","作业","zuò yè","homework"),
  ("用","yòng","to use","不用","bú yòng","no need"),
  ("打","dǎ","to hit; to play","打球","dǎ qiú","play ball"),
  ("找","zhǎo","to look for","找到","zhǎo dào","to find"),
  ("叫","jiào","to call, to shout","大叫","dà jiào","to shout"),
  ("问","wèn","to ask","问题","wèn tí","a question"),
  ("给","gěi","to give","送给","sòng gěi","to give (someone something)"),
  ("送","sòng","to give, to send","送礼物","sòng lǐ wù","give a present"),
  ("放","fàng","to put; to let go","放学","fàng xué","school's out"),
  ("帮","bāng","to help","帮忙","bāng máng","to help out"),
  ("住","zhù","to live (somewhere)","住在","zhù zài","to live in"),
  ("买","mǎi","to buy","买菜","mǎi cài","buy groceries"),
  ("洗","xǐ","to wash","洗手","xǐ shǒu","wash your hands"),
]),
("Songs, games & stories", [
  ("唱","chàng","to sing","唱歌","chàng gē","sing songs"),
  ("歌","gē","song","儿歌","ér gē","nursery rhyme"),
  ("音","yīn","sound","音乐","yīn yuè","music"),
  ("乐","lè","happy; (yuè) music","快乐","kuài lè","happy"),
  ("玩","wán","to play","好玩","hǎo wán","fun"),
  ("跳","tiào","to jump","跳舞","tiào wǔ","to dance"),
  ("游","yóu","to swim","游泳","yóu yǒng","to swim"),
  ("事","shì","matter, thing","故事","gù shi","story"),
  ("故","gù","old; reason","故事","gù shi","story"),
]),
("Think & feel", [
  ("想","xiǎng","to think; to miss","想家","xiǎng jiā","to miss home"),
  ("知","zhī","to know","知道","zhī dào","to know"),
  ("道","dào","way, path","知道","zhī dào","to know"),
  ("认","rèn","to recognise","认字","rèn zì","recognise characters"),
  ("识","shí","to know","认识","rèn shi","to know (someone)"),
  ("怕","pà","to fear","害怕","hài pà","scared"),
  ("爱","ài","to love","我爱你","wǒ ài nǐ","I love you"),
  ("喜","xǐ","to like; joy","喜欢","xǐ huan","to like"),
  ("欢","huān","happy, merry","欢迎","huān yíng","welcome!"),
  ("笑","xiào","to laugh, to smile","微笑","wēi xiào","a smile"),
  ("哭","kū","to cry","大哭","dà kū","to cry loudly"),
  ("兴","xìng","excitement","高兴","gāo xìng","happy"),
  ("谢","xiè","to thank","谢谢","xiè xie","thank you"),
  ("请","qǐng","please; to invite","请坐","qǐng zuò","please sit"),
]),
("School & learning", [
  ("学","xué","to learn","上学","shàng xué","go to school"),
  ("习","xí","to practise","学习","xué xí","to study"),
  ("校","xiào","school","学校","xué xiào","school"),
  ("书","shū","book","看书","kàn shū","read a book"),
  ("本","běn","(counting books); root","课本","kè běn","textbook"),
  ("课","kè","lesson","上课","shàng kè","class time"),
  ("同","tóng","same","同学","tóng xué","classmate"),
  ("字","zì","character, word","汉字","hàn zì","Chinese characters"),
  ("文","wén","writing","中文","zhōng wén","Chinese"),
  ("语","yǔ","language","汉语","hàn yǔ","the Chinese language"),
  ("笔","bǐ","pen","毛笔","máo bǐ","brush pen"),
  ("画","huà","to draw; a painting","画画","huà huà","draw pictures"),
  ("考","kǎo","to take a test","考试","kǎo shì","exam"),
  ("试","shì","to try; a test","试试","shì shi","have a try"),
  ("教","jiāo","to teach","教书","jiāo shū","to teach"),
  ("汉","hàn","Chinese (Han)","汉字","hàn zì","Chinese characters"),
]),
("Position & direction", [
  ("上","shàng","up; on","上面","shàng miàn","on top"),
  ("下","xià","down; under","下面","xià miàn","underneath"),
  ("中","zhōng","middle","中间","zhōng jiān","in the middle"),
  ("里","lǐ","inside","里面","lǐ miàn","inside"),
  ("外","wài","outside","外面","wài miàn","outside"),
  ("面","miàn","side; face","前面","qián miàn","in front"),
  ("前","qián","front; before","以前","yǐ qián","before"),
  ("后","hòu","back; after","后面","hòu miàn","behind"),
  ("左","zuǒ","left","左手","zuǒ shǒu","left hand"),
  ("右","yòu","right","右手","yòu shǒu","right hand"),
  ("东","dōng","east","东西","dōng xi","a thing"),
  ("西","xī","west","西瓜","xī guā","watermelon"),
  ("南","nán","south","南方","nán fāng","the south"),
  ("北","běi","north","北京","běi jīng","Beijing"),
  ("边","biān","side","旁边","páng biān","beside"),
  ("方","fāng","direction; square","地方","dì fang","a place"),
  ("远","yuǎn","far","不远","bù yuǎn","not far"),
  ("近","jìn","near","附近","fù jìn","nearby"),
]),
("Out & about", [
  ("国","guó","country","中国","zhōng guó","China"),
  ("城","chéng","city; wall","城市","chéng shì","city"),
  ("房","fáng","house","房子","fáng zi","a house"),
  ("门","mén","door","大门","dà mén","the gate"),
  ("车","chē","car","汽车","qì chē","car"),
  ("路","lù","road","马路","mǎ lù","the road"),
  ("机","jī","machine","手机","shǒu jī","mobile phone"),
  ("电","diàn","electricity","电灯","diàn dēng","electric light"),
  ("视","shì","to look at","电视","diàn shì","television"),
  ("脑","nǎo","brain","电脑","diàn nǎo","computer"),
  ("医","yī","doctor; medicine","医生","yī shēng","doctor"),
  ("园","yuán","garden","公园","gōng yuán","park"),
  ("公","gōng","public","公鸡","gōng jī","rooster"),
  ("衣","yī","clothes","衣服","yī fu","clothes"),
  ("服","fú","clothes; to serve","舒服","shū fu","comfortable"),
  ("钱","qián","money","花钱","huā qián","spend money"),
]),
("Question words", [
  ("什","shén","what (in 什么)","什么","shén me","what?"),
  ("么","me","(in 什么)","什么","shén me","what?"),
  ("谁","shéi","who","是谁","shì shéi","who is it?"),
  ("哪","nǎ","which","哪里","nǎ lǐ","where?"),
  ("怎","zěn","how","怎么","zěn me","how?"),
  ("样","yàng","kind; way","一样","yí yàng","the same"),
  ("吗","ma","(turns it into a question)","好吗","hǎo ma","okay?"),
  ("呢","ne","(bounces a question back)","你呢","nǐ ne","and you?"),
  ("吧","ba","(a gentle suggestion)","走吧","zǒu ba","let's go!"),
  ("啊","a","(adds feeling)","好啊","hǎo a","sure!"),
  ("为","wèi","for; for the sake of","为什么","wèi shén me","why?"),
  ("因","yīn","because; cause","因为","yīn wèi","because"),
  ("所","suǒ","(in 所以); place","所以","suǒ yǐ","so, therefore"),
  ("以","yǐ","(in 可以 and 所以)","可以","kě yǐ","may, can"),
  ("如","rú","if; like","如果","rú guǒ","if"),
]),
("Little glue words", [
  ("的","de","(links describing words)","我的","wǒ de","my, mine"),
  ("了","le","(something happened)","下雨了","xià yǔ le","it's raining!"),
  ("是","shì","to be","是的","shì de","yes"),
  ("不","bù","not","不是","bú shì","is not"),
  ("没","méi","not have","没有","méi yǒu","there isn't"),
  ("有","yǒu","to have","有用","yǒu yòng","useful"),
  ("着","zhe","(happening right now)","看着","kàn zhe","watching"),
  ("过","guò","to pass; (done before)","过年","guò nián","Chinese New Year"),
  ("得","de","(links action and how)","跑得快","pǎo de kuài","runs fast"),
  ("和","hé","and","我和你","wǒ hé nǐ","you and me"),
  ("也","yě","also","我也是","wǒ yě shì","me too"),
  ("都","dōu","all","都是","dōu shì","all are"),
  ("还","hái","still; also","还有","hái yǒu","and also"),
  ("就","jiù","right away; then","就是","jiù shì","exactly"),
  ("只","zhǐ","only","只有","zhǐ yǒu","only"),
  ("很","hěn","very","很好","hěn hǎo","very good"),
  ("太","tài","too (much)","太好了","tài hǎo le","wonderful!"),
  ("最","zuì","the most","最好","zuì hǎo","the best"),
  ("更","gèng","even more","更大","gèng dà","even bigger"),
  ("又","yòu","again","又来了","yòu lái le","here we go again"),
  ("对","duì","right, correct","对不起","duì bu qǐ","sorry"),
]),
("This & that", [
  ("在","zài","at, in","在家","zài jiā","at home"),
  ("这","zhè","this","这里","zhè lǐ","here"),
  ("那","nà","that","那里","nà lǐ","there"),
  ("每","měi","every","每天","měi tiān","every day"),
  ("把","bǎ","handle; (grammar helper)","把手","bǎ shǒu","a handle"),
  ("被","bèi","quilt; (by)","被子","bèi zi","a quilt"),
  ("比","bǐ","to compare","比一比","bǐ yi bǐ","compare them!"),
  ("跟","gēn","with; to follow","跟我学","gēn wǒ xué","learn with me"),
  ("从","cóng","from","从小","cóng xiǎo","ever since little"),
]),
("Can & must", [
  ("会","huì","can (know how to)","会写字","huì xiě zì","can write characters"),
  ("能","néng","can (be able to)","不能","bù néng","can't"),
  ("要","yào","to want; must","想要","xiǎng yào","to want"),
  ("让","ràng","to let","让一让","ràng yi ràng","excuse me — make way"),
  ("别","bié","don't","别哭","bié kū","don't cry"),
  ("可","kě","can; (but)","可是","kě shì","but"),
  ("应","yīng","should","应该","yīng gāi","should"),
  ("该","gāi","should","应该","yīng gāi","should"),
  ("成","chéng","to become","完成","wán chéng","to finish"),
  ("完","wán","to finish","吃完","chī wán","eat it all up"),
  ("经","jīng","to pass through","已经","yǐ jīng","already"),
  ("已","yǐ","already","已经","yǐ jīng","already"),
  ("正","zhèng","just now; upright","正在","zhèng zài","right now"),
]),
]

# ---------------------------------------------------------------------------
# The original twelve hand-written entries (origin story + full example
# sentence) — preserved verbatim from the first edition of char-data.js.
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
"而":"and","页":"head","羊":"sheep","⺶":"sheep","羽":"feather","西":"west",
"覀":"cover","角":"horn","谷":"valley","豕":"pig","豸":"badger","赤":"red",
"辛":"bitter","辰":"dawn","酉":"wine jar","里":"village","青":"green",
"非":"not","面":"face","革":"leather","音":"sound","骨":"bone","鬼":"ghost",
"麻":"hemp","黄":"yellow","鼓":"drum","齐":"even","龺":"sunrise","止":"stop",
"牜":"cow","𥫗":"bamboo","龰":"stop","攴":"tap","殳":"club","欠":"yawn",
"斗":"dipper","片":"slice","爿":"split wood","疋":"bolt of cloth","疒":"sickness",
"癶":"footsteps","皿":"dish","矛":"spear","矢":"arrow","禸":"track","穴":"cave",
"网":"net","罒":"net","缶":"jar","耒":"plough","臣":"minister","舟":"boat",
"艮":"mountain ridge","虍":"tiger","血":"blood","襾":"cover","豆":"bean",
"貝":"shell","釆":"distinguish","長":"long","長":"long","韦":"leather",
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
    for group, ch, py, en, word, wordpy, worden in flat:
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
        if ch in OVERRIDES:
            origin, ex = OVERRIDES[ch]["origin"], OVERRIDES[ch]["ex"]
        else:
            origin = origin_for(ch, en, drec)
            pys = wordpy.split(" ")
            assert len(pys) == len(word), "pinyin/word length mismatch: " + word
            ex = {"seg": [[c, p] for c, p in zip(word, pys)], "en": worden, "phrase": True}
        data.append({
            "ch": ch, "py": py, "en": en,
            "strokes": len(g["strokes"]),
            "radical": rad or ch, "radEn": RAD_EN.get(rad, ""),
            "group": group, "origin": origin, "ex": ex,
            "s": g["strokes"],
            "m": [[[int(x), int(y)] for x, y in m] for m in g["medians"]],
        })

    if problems:
        print("\n".join(problems), file=sys.stderr)
        sys.exit(1)

    header = (
"/* characters data — Casey Chinese School character explorer.\n"
"   GENERATED by scripts/build-char-data.py — edit the table there, not this file.\n"
"   300 common characters in themed groups; glosses, example words and origin\n"
"   notes curated for the school. Stroke paths/medians: makemeahanzi\n"
"   (https://github.com/skishore/makemeahanzi, Arphic Public License),\n"
"   1024 Y-up space. Self-contained / evergreen. */\n")
    body = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    with open(OUT, "w", encoding="utf-8") as f:
        f.write(header + "window.CHAR_DATA = " + body + ";\n")
    print("wrote %s: %d characters, %d groups, %.0f KB" %
          (os.path.relpath(OUT, ROOT), len(data), len(GROUPS), len(body) / 1024))

if __name__ == "__main__":
    main()
