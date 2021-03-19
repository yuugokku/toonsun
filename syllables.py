import re

# ユーゴック語の音素情報
# 短母音
fecher_mgt = ["a", "i", "u", "e", "o"]
# 長母音、イストゥゴア母音 -> 常に二重母音・同一音節となる。
kokia_mgt = ["aa", "ii", "uu", "ee", "oo"]
istugoa_mgt = ["ai", "ui", "ei", "oi"]
# 一文字の子音
one_ktt = [
    "f", "p", "b", "m",
    "z","r", 
    "t", "d", "s", "n",
    "k", "g",
    "v", "h",
    "w", "r",
]
# 二文字の子音：扱いにくいので雑に置き換える
two_ktt = [
    ("fy", "1"), ("py", "2"), ("by", "3"), ("ph", "4"), ("phy", "5"), ("bw", "6"), ("my", "7"),
    ("th", "l"), ("zy", "8"), ("ry", "9"),
    ("ty", "!"), ("dy", "#"), ("ts", "@"),
    ("ch", "c"), ("sy", "$"), ("ny", "="),
    ("ky", "-"), ("gy", "^"), ("hy", "~"),
]

def encode(text):
    cvted = text.\
        replace(".","").\
        replace(",", ".").\
        replace("'", "")
    for k in two_ktt:
        cvted = cvted.replace(k[0], k[1])
    return cvted 
    
def decode(text):
    cvted = text
    for k in two_ktt:
        cvted = cvted.replace(k[1], k[0])
    return cvted
    
def count_vowels(text):
    cnt = 0
    for c in text:
        if c in fecher_mgt:
            cnt += 1
    return cnt

def get_ktt():
    ktt = one_ktt
    for k in two_ktt:
        ktt.append(k[1])
    return ktt

def into_syllables(text, encoded=True):
    text = text.lower()
    text = encode(text)
    mgt = fecher_mgt
    ktt = one_ktt
    for k in two_ktt:
        ktt.append(k[1])
    loc = []
    ktt_count = 0
    mgt_count = 0
    ktt_pre = True
    for i, ch in enumerate(text):
        if ch in mgt:
            if ktt_pre:
                loc.append(i - int(ktt_count>0))
            ktt_pre = False
            mgt_count += 1
            ktt_count = 0
        elif ch in ktt:
            ktt_pre = True
            mgt_count = 0
            ktt_count += 1
    loc.append(len(text))
    syls = []
    for i in range(len(loc) - 1):
        s, e = loc[i], loc[i+1]
        syl = text[s:e]
        syls += [syl]
    syls_ = []
    for syl in syls:
        joint = [syl]
        if " " in syl:
            joint = []
            start = 0
            for i in range(1, len(syl)-1):
                if syl[i-1] in mgt and syl[i] == " " and syl[i+1] in mgt:
                    joint.append(syl[start:i])
                    start = i + 1
            joint.append(syl[start:-1])
        for s in joint:
            if count_vowels(s) >= 3:
                i = 1
                while len(s) - 2 < i:
                    if s[i:i+2] in kokia_mgt:
                        break
                    if s[i:i+2] in istugoa_mgt:
                        break
                    if s[i] in mgt and s[i+1] in ktt:
                        break
                    i += 1
                head_c = s[0]
                parts = (s[1:i], s[i:i+2], s[i+2:])
                for part in parts:
                    if part != "":
                        syls_.append(head_c + part)
                        head_c = ""
            elif count_vowels(s) == 2:
                head_c = s[0]
                if s[-1] in ktt and s[1:3] not in kokia_mgt + istugoa_mgt:
                    syls_.append(s[0:2])
                    syls_.append(s[2:])
                else:
                    syls_.append(s)
            else:
                syls_.append(s)
    if encoded:
        return syls_
    else:
        return [decode(s) for s in syls_]
    
def scan(text):
    syls = into_syllables(text)
    mark = ""
    for i in range(len(syls)):
        if len(syls[i]) >= 3:
            mark += "-"
        elif syls[i][-1] in get_ktt():
            mark += "-"
        else:
            mark += "^"
    return mark
