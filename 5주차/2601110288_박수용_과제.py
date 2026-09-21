verse = """If you can keep your head when all about you
 Are losing theirs
and blaming it on you,
If you can trust yourself when all men doubt you,
 But make allowance for their doubting too;
If you can wait and not be tired by waiting,
 Or being lied about, don’t deal in lies,
Or being hated, don’t give way to hating,
 And yet don’t look too good, nor talk too wise:"""

inStr = input("검색하고자하는 단어를 입력하세요:")

count = verse.count(inStr)
changed_verse = verse.replace(inStr, inStr.upper())

print('검색 단어는 "{}"'.format(inStr))
print("입니다")
print("문장내 검색된 횟수는 총 {}회 입니다.".format(count))
print("변경된 문장은")
print("---------------------------------------")
print(changed_verse)

