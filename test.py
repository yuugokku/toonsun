from syllables import into_syllables, scan, decode

text = input("phantas kka syunta?: ")
print("atta syunta:", text)
print([decode(t) for t in into_syllables(text)])
print(scan(text))
