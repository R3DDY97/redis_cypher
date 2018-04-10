# redis-cypher
OpenCypher language implementation to store data in Redis through Python3

## Usage:-

Executes cypher QL in python and stores the Graph data in Redis DB

Still in development

### **Requires Redis-server installed in the system**

```
$ git https://github.com/R3DDY97/redis-cypher

$ cd redis-cypher && pip3 install -r requirements.txt

$ sudo apt install redis-server redis-tools

```

Run redis-server and then Enter python console

```
$ cd src/parsers && ipython3 || python3

>> import query_parser

>> rc = query_parser.CypherGraph()

>> rc.execute_query("CREATE (node:User" {name: 'User_name', type: 'R00T'})
    ```



### ToDo:-

    *  Make it pip package in the end
    *  Finish Implementing  basic cypher cluases
