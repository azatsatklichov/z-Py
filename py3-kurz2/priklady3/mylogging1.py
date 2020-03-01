import logging
logging.basicConfig(level = logging.INFO)
def mirror(lst):
  ret = []
  for i in range(len(lst)):
    ret.append(lst[-i - 1])
    logging.debug("list for i={0}: {1} ".format(i, lst[-i - 1]))
  return lst + ret

mirror([1,4,5])
