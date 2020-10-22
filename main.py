import ipfshttpclient



# Share TCP connections using a context manager
with ipfshttpclient.connect('/ip4/127.0.0.1/tcp/5001') as client:
	hash = client.add('test.txt')['Hash']
	print(client.stat(hash))

# Share TCP connections until the client session is closed
class SomeObject:
	def __init__(self):
		self._client = ipfshttpclient.connect(session=True)

	def do_something(self):
		hash = self._client.add('test.txt')['Hash']
		print(self._client.stat(hash))

	def close(self):  # Call this when your done
		self._client.close()
