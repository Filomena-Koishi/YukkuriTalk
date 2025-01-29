import subprocess
import os
from pypinyin import lazy_pinyin
from englishToKanaConverter import EnglishToKanaConverter

# 拼音转日语发音
jp_pnca={"a":"あ", "o":"おお","e":"え",
         "ba":"ば","bo":"ぼ","bi":"び","bu":"ぶ","biao":"ばお","bian":"べん",
         "pa":"ぱ","po":"ぽ","pi":"ぴ","pu":"ぷ","piao":"ぱお","pian":"べん",
         "ma":"ま","mo":"も","me":"め","mi":"み","mu":"む","miao":"みお","mian":"みえ",
         "fa":"ふあ","fo":"ふお","fu":"ふ",
         "da":"だ","de":"で","di":"で","du":"つう","dia":"だ","diao":"であお","dian":"でい","duo":"ど","duan":"であん",
         "ta":"た","te":"て","ti":"ち","tu":"つう","tiao":"てあお","tian":"てん","tuo":"と","tuan":"てあん",
         "na":"な","ne":"ね","ni":"に","nu":"ぬ","nv":"り","niao":"にあお","nian":"にん","niang":"にあん","nuo":"の","nuan":"ぬあん",
         "la":"ら","lo":"ろ","le":"れ","li":"り","lu":"る","lv":"り","lia":"りあ","liao":"りあお","lian":"りん","liang":"りあん",
         "luo":"ろ","luan":"れあん",
         "ga":"が","ge":"げ","gu":"ぐ","gua":"ぐあ","guo":"ぐお","guai":"ぐい","guan":"ぐあん","guang":"ぐあん",
         "ka":"か","ke":"け","ku":"く","kua":"か","kuo":"こ","kuai":"くあい","kuan":"くあん","kuang":"くあん",
         "ha":"は","he":"へ","hu":"ふ","hua":"ふあ","huo":"ほ","huai":"ふい","huan":"ふあん","huang":"ふあん",
         "ji":"じ","ju":"じゆ","jia":"じゃ","jiao":"じゃお","jian":"じえん","jiang":"じゃん","jiong":"じょ","juan":"じえん",
         "qi":"ち","qu":"ちゆ","qia":"ちあ","qiao":"ちあお","qian":"ちえ","qiang":"ちあん","qiong":"ちおん","quan":"ちゆえ",
         "xi":"し","xu":"しゆ","xia":"しあ","xiao":"しあお","xian":"しえん","xiang":"しあん","xiong":"しおん","xuan":"しゆえん",
         "zha":"ざ","zhe":"ぜ","zhi":"つ","zhu":"つう","zhua":"つうあ","zhuo":"つうお","zhuai":"つうえ","zhuan":"つうあん","zhuang":"つうあん",
         "cha":"ちあ","che":"ちえ","chi":"ち","chu":"ちゅ","chua":"ちあ","chuo":"ちお","chuai":"ちうえ","chuan":"ちうあん","chuang":"ちうあん",
         "sha":"すあ","she":"すえ","shi":"す","shu":"すう","shua":"すうあ","shuo":"すうお","shuai":"すうあい","shuan":"すうあん","shuang":"すうあん",
         "ra":"ら","re":"や","ri":"い","ru":"る","rua":"るあ","ruo":"るお","ruan":"るあん",
         "za":"ざ","ze":"ぜ","zi":"じ","zu":"ちゆ","zuo":"じお","zuan":"じあん",
         "ca":"つあ","ce":"つえ","ci":"つ","cu":"つう","cuo":"つお","cuan":"つあん",
         "sa":"さ","se":"せ","si":"す","su":"すう","suo":"すお","suan":"すあん",
         "ya":"や","yo":"よ","ye":"いえ","yi":"い","yu":"ゆ","yuan":"ゆあん",
         "wa":"わ","wo":"を","wu":"う",
         "ai":"あい","ei":"えい","ao":"あお","ou":"おう","er":"え","an":"あん","n":"えん","ang":"あん","eng":"えん",
         "bai":"ばい","bei":"べい","bao":"ばお","bie":"びえ","ban":"ばん","ben":"べん","bin":"びん","bang":"ばあん","beng":"べえん","bing":"びいん",
         "pai":"ぱい","pei":"ぺい","pao":"ぱお","pou":"ぽ","pie":"ぺ","pan":"ぱん","pen":"ぺん","pin":"ぴん","pang":"ぱん","peng":"ぺん","ping":"ぴん",
         "mai":"まい","mei":"めい","mao":"まお","mou":"もう","miu":"みう","mie":"め","man":"まん","men":"めん","min":"みん",
         "mang":"まん","meng":"めん","ming":"みん",
         "fei":"ふえ","fou":"ふお","fan":"ふあ","fen":"ふえん","fang":"ふあん","feng":"ふえん",
         "dai":"だい","dei":"でい","dui":"でうい","dao":"だお","dou":"でう","diu":"でいう","die":"でい","dan":"だん","den":"でん",
         "dun":"でん","dang":"だん","deng":"でん","ding":"でいん","dong":"でおん",
         "tai":"たい","tei":"てい","tui":"てい","tao":"たお","tou":"とう","tie":"てえ","tan":"たん","tun":"でうん",
         "tang":"たん","teng":"てん","ting":"でいん","tong":"どん",
         "nai":"ない","nei":"ねい","nao":"なお","nou":"ねおう","niu":"にう","nie":"にえ","nan":"なん","nen":"ねん","nin":"にん","nun":"ぬん",
         "nang":"なん","neng":"ねん","ning":"にん","nong":"のん",
         "lai":"らい","lei":"れい","lao":"らお","lou":"ろう","liu":"れゆ","lie":"れ","lan":"らん","lin":"りん","lun":"る",
         "lang":"らん","leng":"れん","ling":"れん","long":"ろん",
         "gai":"がい","gei":"げい","gui":"ぐい","gao":"がお","gou":"ごう","gan":"がん","gen":"げん","gun":"ぐん",
         "gang":"がん","geng":"げん","gong":"ごん",
         "kai":"かい","kei":"けい","kui":"くい","kao":"かお","kou":"こう","kan":"かん","ken":"けん","kun":"くん",
         "kang":"かん","keng":"けん","kong":"こん",
         "hai":"はい","hei":"へい","hui":"ふい","hao":"はお","hou":"ほう","han":"はん","hen":"へん","hun":"ふん",
         "hang":"はん","heng":"へん","hong":"ほん",
         "jiu":"じいう","jie":"じいえ","jue":"じうえ","jin":"じん","jun":"じゆん","jing":"じいん",
         "qiu":"くゆ","qie":"くえ","que":"くゆえ","qin":"くいん","qun":"くゆん","qing":"くいん",
         "xiu":"しゆ","xie":"しえ","xue":"しゆえ","xin":"しん","xun":"しゆん","xing":"しん",
         "zhai":"つあい","zhei":"つえい","zhui":"つえ","zhao":"つあお","zhou":"つおう",
         "zhan":"つあん","zhen":"つえん","zhun":"つうん","zhang":"つあん","zheng":"つえん","zhong":"つおん",
         "chai":"ちあい","chui":"ちうえ","chao":"ちあお","chou":"ちおう","chan":"ちあん","chen":"ちえん","chun":"ちうん",
         "chang":"ちあん","cheng":"ちえん","chong":"ちおん",
         "shai":"すあい","shei":"すえい","shui":"すい","shao":"すあお","shou":"しおう","shan":"すあん",
         "shen":"すえん","shun":"すん","shang":"すあん","sheng":"すえん",
         "rui":"いえ","rao":"いあう","rou":"いおう","ran":"いあん","ren":"いえん","run":"えうん","rang":"いあん","reng":"いえん","rong":"いおん",
         "zai":"ざい","zei":"ぜい","zui":"つい","zao":"ざお","zou":"つおう","zan":"つあん","zen":"つえん","zun":"つうん",
         "zang":"つあん","zeng":"つえん","zong":"つおん",
         "cai":"つあい","cei":"つえい","cui":"つえい","cao":"つあお","cou":"つおう","can":"つあん","cen":"つえん","cun":"つうん",
         "cang":"つあん","ceng":"つえん","cong":"つおん",
         "sai":"すえい","sui":"すえい","sao":"すあお","sou":"すおう","san":"さん","sen":"せん","sun":"すうん",
         "sang":"すあん","seng":"すえん","song":"すおん",
         "yao":"やお","you":"ゆ","yue":"ゆえ","yan":"いあん","yin":"いん","yun":"ゆん","yang":"やあん","ying":"いん","yong":"いおん",
         "wai":"わい","wei":"うえい","wan":"わん","wen":"うえん","wang":"うあん","weng":"うえん",
         "，":",","。":"。","！":",","？":",","、":",",
         ",":",",".":"。","!":",","?":","
         }

arabic={"1":"一","2":"二","3":"三","4":"四","5":"五","6":"六","7":"七","8":"八","9":"九","0":"零"}

# 忽略句号、逗号等不发音的符号
symb={"@":"爱特","#":"井","%":"百分比","&":"与","*":"乘","-":"减","=":"等于","+":"加","/":"除以","<":"小于",">":"大于","~":"到",
      # 停顿
      ",":"、",".":"。","，":"、","。":"。","?":"？","？":"？",":":";","：":";",
      # 以下忽略
      "\"":"","“":"","”":"","!":"","！":"","$":"","^":"","(":"","（":"",";":";","；":";",
      ")":"","）":"","_":"","——":""}

# AquesTalk无法处理的日文字符
aquestalk_replace={"ぁ":"あ","ぃ":"い","ぅ":"う","ぇ":"え","ぉ":"お","ゎ":"わ","ヶ":"け","〃":"","ゞ":"","ゝ":"","ヾ":"",
              "ヽ":"","〻":"","ゐ":"い","ゑ":"え","ヴ":"ぶ"," ":""}

# AquesTalk试用版发音限制的替换
aquestrail_replace={"ま":"ば","み":"び","む":"ぶ","め":"れ","も":"ぼ","な":"だ","に":"れい","ね":"れ","の":"ろ",
                    "マ":"ば","ミ":"び","ム":"ぶ","メ":"れ","モ":"ぼ","ナ":"だ","ニ":"れい","ネ":"れ","ノ":"ろ"}

# 声音预设，0是油库里
phont={0:"aq_yukkuri",1:"aq_f1c",2:"aq_f3a",3:"aq_huskey",4:"aq_m4b",5:"aq_mf1",6:"aq_rb2",
       7:"aq_rb3",8:"aq_rm",9:"aq_robo",10:"ar_f4",11:"ar_m5",12:"ar_mf2",13:"ar_rm3"}

EngToKana = EnglishToKanaConverter(False, os.path.join(os.path.dirname(__file__), "englishToKanaConverter.log"))

# 写入日语字符串
def WriteString(jp_string):
    file=open(".\\input.txt","w",encoding="utf-8")
    file.write(jp_string)
    file.close()

# 通过exe调用AquesTalk2生成语音
# 仅接受日文字符串
def AquesTalk(jp_string,voice_speed,file_name,phont_num):
    # 替换掉AquesTalk无法处理的日文字符
    for char in aquestalk_replace:
        jp_string=jp_string.replace(char,aquestalk_replace[char])
    # 替换掉AquesTalk试用版发音受限的字符
    for char in aquestrail_replace:
        jp_string=jp_string.replace(char,aquestrail_replace[char])
    WriteString(jp_string)
    subprocess.call(".\\CallAquesTalk.exe "+str(voice_speed)+" "+str(len(jp_string))
                    +" "+phont[phont_num]+" "+file_name, shell=True)

# 用中文、英文、数字、日语字符串生成语音，默认预设是油库里
# 字符串内不要出现symb中未定义的符号，否则会出错
def YukkuriTalk(cn_string,voice_speed=110,file_name="output",phont_num=0):
    # 替换数字为中文
    for i in range(0,10,1):
        cn_string=cn_string.replace(str(i), arabic[str(i)])
    # 替换符号为中文，删除不发音的符号
    for char in symb:
            cn_string = cn_string.replace(char, symb[char])
    # 生成拼音列表
    pinyin_list = lazy_pinyin(cn_string)
    # 此时，拼音列表内仅有拼音、日文、英语单词
    # 生成日语字符串，将英文单词替换为片假名
    jp_string=""
    for cn_str in pinyin_list:
        if cn_str in jp_pnca:
            jp_string+=jp_pnca[cn_str]
        else:
            jp_string+=EngToKana.process(cn_str)
    # AquesTalk调用
    AquesTalk(jp_string,voice_speed,file_name,phont_num)


# 调用示例
# string=input("输入文字！\n")
# YukkuriTalk(string)