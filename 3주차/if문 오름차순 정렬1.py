a = int(input("정수 a : "))
b = int(input("정수 b : "))

if a > b:
    a,b = b,a

print("a<b로 정렬했습니다.")
print("정수 a의 값은 %d 입니다."%a)
print("정수 b의 값은 %d 입니다."%b)
