#https://www.w3schools.com/python/python_pip.asp
import camelcase

print('-- piip --')
c = camelcase.CamelCase()

txt = "hello world"

print(c.hump(txt))