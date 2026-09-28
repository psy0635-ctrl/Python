# Module1.py

def func1():
    print("Module1.func1() 함수 출력")

def func2():
    print("Module1.func2() 함수 출력")

def func3():
    print("Module1.func3() 함수 출력")


print("모듈1 전역 부분 출력")
print(__name__)

if __name__ == '__main__' :
    print("모듈1 메인함수 내 출력")
    func1()
    print(__name__)
    
