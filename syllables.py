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
    text = text.\
        strip().\
        replace(".","").\
        replace(",", ".").\
        replace("'", "")
    for k in two_ktt:
        text = text.replace(k[0], k[1])
    cvted = ""
    for i in range(len(text)):
        to_add = ""
        if text[i] == " ":
            if text[i-1] in fecher_mgt and \
                text[i+1] in fecher_mgt:
                to_add = ","
        else:
            to_add = text[i]
        cvted += to_add
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

def decompose(syl):
    cnt_vowel = count_vowels(syl)
    if syl[0] in get_ktt():
        head_c = syl[0]
        vowel = syl[1:1+cnt_vowel]
        if len(syl) > 1 + cnt_vowel:
            foot_c = syl[1+cnt_vowel:]
        else:
            foot_c = ""
    else:
        head_c = ""
        vowel = syl[:cnt_vowel]
        if len(syl) > cnt_vowel:
            foot_c = syl[cnt_vowel:]
        else:
            foot_c = ""
    return head_c, vowel, foot_c

def get_ktt():
    ktt = one_ktt
    for k in two_ktt:
        ktt.append(k[1])
    return ktt

def _into_syllables(text):
    mgt = fecher_mgt
    ktt = get_ktt()
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
        syl = text[s:e].strip()
        syls += [syl]
    syls_ = []
    for s in syls:
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
            if s[0] in ktt:
                head_c = s[0]
            else:
                head_c = ""
            start = len(head_c)
            if s[start:start+2] in istugoa_mgt + kokia_mgt:
                syls_.append(head_c + s[start:])
            else:
                if s[-1] in ktt:
                    syls_.append(head_c + s[start:start+1])
                    syls_.append(s[start+1:])
                else:
                    syls_.append(head_c + s[start:])
        else:
            syls_.append(s)
    return syls_
    
def into_syllables(text):
    text = text.lower()
    text = encode(text)
    text = text.split(",")
    syls = []
    for t in text:
        syls += _into_syllables(t)
    return syls

def scan(text):
    syls = into_syllables(text)
    mark = ""
    for i in range(len(syls)):
        head_c, vowel, foot_c = decompose(syls[i])
        if foot_c != "":
            mark += "-"
        elif len(vowel) > 1:
            mark += "-"
        else:
            mark += "^"
    return mark
