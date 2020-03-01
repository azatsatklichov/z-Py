 

#see how we flipped the keys with values

class mydict(dict):
	def flip(self):
		res = mydict()
		for k in self:
			v = self[k]
			if not v in res:
				res[v] = set()
			res[v].add(k)
		return res

x = mydict({1:'a', 2:'b', 3:'a'})
print(x)
y = x.flip()
print(y)

