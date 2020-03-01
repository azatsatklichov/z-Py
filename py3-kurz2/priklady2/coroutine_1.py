from types import coroutine


@coroutine
def sleep(seconds):
  yield ('sleep', seconds)


async def sleepy(seconds):
  print('Yawn. Getting sleepy.')
  await sleep(seconds)
  print('Awake at last!')


c = sleepy(10)
request = c.send(None)
request
try:
  request = c.send(None)
except StopIteration:
  print('Done with coroutine.')
