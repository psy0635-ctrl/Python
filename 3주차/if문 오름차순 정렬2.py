a = int(input("정수 a : "))
b = int(input("정수 b : "))
c = int(input("정수 c : "))

if a > b:
    a, b = b, a

if a > c:
    a, c = c, a

if b > c:
    b, c = c, b

print("a < b < c로 정렬했습니다.")
print("정수 a의 값은", a, "입니다")
print("정수 b의 값은", b, "입니다")
print("정수 c의 값은", c, "입니다")
