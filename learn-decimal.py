# 如何利用decimal库来处理小数点问题
#  学习如何使用decimal库来处理小数点


# 文档地址: https://docs.python.org/zh-cn/3/library/decimal.html

value1 = 0.0000223233
print(value1)
value2 =str("0.0000223233")
print(value2)

## 四则运算


from decimal import Decimal, ROUND_UP, ROUND_DOWN

a = Decimal(10)
print(a, type(a))

b = Decimal(10.12) # 二进制方式存储的
print(b)

c = Decimal(str(10.12))
print(c)
#
# # 注意事项: Decimal对象不能跟其他进行数字类型进行运算，要把它们转成同类型的数据
#
# c1 = c + 11.2
# print(c1)

c1 = c + Decimal(str(11.2))
print(c1)


## 价格精度的问题

# btc, 38450.1, 38450.1234, 2500.12


price1 =  Decimal(str(38450.15676))

d = price1.quantize(Decimal("0.1"))
print(d)


price2 =  Decimal(str(2560.24567))

price2 = price2.quantize(Decimal("0.01"))
print(price2)

## round_up, round_down

price3 =  Decimal(str(2560.24867))

price3 = price3.quantize(Decimal("0.01"), rounding=ROUND_DOWN)
print(price3)


price4 =  Decimal(str(2560.241224))

price4 = price4.quantize(Decimal("0.01"), rounding=ROUND_UP)
print(price4)

