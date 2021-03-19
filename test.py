from syllables import into_syllables, scan

text = input("phantas kka syunta?: ")
print("atta syunta: ", text)
print(into_syllables(text, encoded=False))
print(scan(text))
