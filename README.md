# Redis Cluster

## How to install

1. Clone the repository
2. Run `docker compose up -d`
3. Run `docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' redis-node-1` to get the IP address of the first node
4. Repeat the previous step for the other nodes
5.

Run `docker exec -it redis-node-1 redis-cli --cluster create <ip1>:6379 <ip2>:6379 <ip3>:6379 <ip4>:6379 <ip5>:6379 <ip6>:6379 --cluster-replicas 1`

## Testing the cluster

1. Run `docker exec -it redis-node-1 redis-cli -c` to connect to the first node
2. Run `cluster info` to get information about the cluster
3. Run `cluster nodes` to get information about the nodes

### Trying redis

1. Run `set key value` to set a key
2. Run `get key` to get the value of the key
3. Run `keys *` to get all the keys
4. Run `del key` to delete a key
5. Run `flushall` to delete all keys
6. Run `exit` to exit the redis-cli

Create a key in one node and try to get it from another node. You will see that the key is available in all nodes.

### Hashes

- Run `hset user:1 name "John Doe"` to set a hash
- Run `hget user:1 name` to get the value of the hash
- Run `hgetall user:1` to get all the values of the hash
- Run `hmset user:1 name "John Doe" age 30` to set multiple values in a hash
- Run `hmget user:1 name age` to get multiple values of the hash
- Run `hdel user:1 age` to delete a value of the hash

### Lists

- Run `lpush list 1 2 3 4 5` to create a list
- Run `lrange list 0 -1` to get all the values of the list
- Run `lpop list` to remove the first element of the list
- Run `rpop list` to remove the last element of the list
- Run `ltrim list 0 2` to remove all elements of the list except the first three

### Sets

- Run `sadd set 1 2 3 4 5` to create a set
- Run `smembers set` to get all the values of the set
- Run `srem set 1` to remove a value of the set

### Sorted Sets

- Run `zadd sorted-set 1 one 2 two 3 three 4 four 5 five` to create a sorted set
- Run `zrange sorted-set 0 -1` to get all the values of the sorted set
- Run `zrange sorted-set 0 -1 withscores` to get all the values of the sorted set with the scores
- Run `zrem sorted-set one` to remove a value of the sorted set

### Expiring keys

- Run `set key value` to set a key
- Run `expire key 10` to set the key to expire in 10 seconds
- Run `ttl key` to get the time to live of the key
  Wait 10 seconds and run `get key` to see that the key is no longer available
- Run `setex key 10 value` to set a key with an expiration time

## Using Redis in a project

In this repository, you have a `index.py` file that shows how to connect to the Redis cluster using the `redis` library.
Run `docker compose --profile testing up -d` to start the testing environment, it will add a new container that will run the `index.py`
file.
See the logs of the container to see the output of the script using `docker logs -f python-project`.

### An existing project

I have this project `https://github.com/Ayfri/UF_Project_B3` which is my end of year project for my third year at Ynov.
We have to make BigQuery requests to get data of `GDELT` project and then use this data to make predictions.
But each request takes a lot of time, around 30 seconds, so I thought about using Redis to cache the results of the requests.

So in this commit : [3c8aa9](`https://github.com/Ayfri/UF_Project_B3/commit/3c8aa93d802ee9d17b844b0b6748f0f67fb5a3b5`) I added a Redis
instance in a Docker container and I used it to cache the results of the requests.

I used the `redis` library to connect to the Redis instance and I used the `set` and `get` methods to cache the results, also using JSON
serialization to store complex data.

## Redis integration introspection

Redis is great for caching and simple key-value storage thanks to its speed, scalability, and ease of use.

#### Pros

- Blazingly fast thanks to in-memory data storage and efficient data structures.
- Highly scalable with sharding and replication strategies.
- Simple data model and minimalistic commands make it easy to learn and integrate.
- Excellent for caching to improve application performance.
- Rich set of data structures like strings, hashes, lists, sets, etc.

#### Cons

- Data persistence requires configuration and can be challenging for high-write scenarios.
- Limited query capabilities compared to traditional databases or data warehouses.
- Memory usage can grow quickly with large datasets or memory-intensive data structures.
- Not well-suited for complex relational data or join operations.
- Limited transaction support may not meet strong consistency requirements.

I actually use [Redis Stack Server](https://redis.io/insight/) in a private project for storing a large amount of complex data, and it works
perfectly.
It also gives us `RedisSearch` and `RedisTimeSeries` modules that we use for more advanced data management and querying.
Before that, we were using local files, and that was a mess to manage and query. Redis was much faster.

One good tool present in the Redis environment is [Redis Insight](https://redis.io/insight/), a graphical user interface that gives Redis
users a powerful way to visualize and interact with their data. Redis Insight allows viewing databases, querying keys and values, and
executing common Redis commands through an intuitive interface. It also integrates tightly with Redis, enabling real-time monitoring and
command inspection capabilities.

While Redis has limitations, it shines for use cases like caching, session management, real-time messaging, and scenarios needing
high-performance data access with simple data structures. For more complex requirements, it's often combined with other solutions or Redis
Stack Server for enhanced data management and querying capabilities.
