# on another CPU machine
from bert_serving.client import BertClient

bc = BertClient(ip='86.17.97.132')  # ip address of the GPU machine
results = bc.encode(['First do it', 'then do it right', 'then do it better'])

print(results)