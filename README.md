# Redis-cypher
OpenCypher language implementation to store data in Redis through Python3

## Usage:-

Executes cypher QL in python and stores the Graph data in Redis DB

Still in development


 Requires **redis-server** installed in the system

```bash
$ git https://github.com/R3DDY97/redis-cypher

$ cd redis-cypher && pip3 install -r requirements.txt

$ sudo apt install redis-server redis-tools

```

Run redis-server and then Enter python console

```bash
$ cd src && ipython3 || python3
```



```python
from graph import Graph
import redis

r = redis.StrictRedis()

query = "CREATE (node:User" {name: 'User_name', type: 'R00T'})"

cypher = Graph()

result = cypher.execute_cypher(query)
```




######  To do:-
- Make it pip package in the end
- Finish Implementing  basic cypher cluases
