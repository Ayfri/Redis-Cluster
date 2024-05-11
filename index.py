from dataclasses import dataclass

from redis.cluster import ClusterNode, RedisCluster


@dataclass
class Profile:
	age: int
	email: str
	first_name: str
	last_name: str

	@property
	def full_name(self) -> str:
		return f'{self.first_name} {self.last_name}'

	def save(self, rc: RedisCluster) -> None:
		print(f"Saving 'user:profile:{self.full_name}'")
		rc.hset(f'user:profile:{self.full_name}', mapping=self.__dict__)

	@classmethod
	def load(cls, rc: RedisCluster, first_name: str, last_name: str) -> 'Profile':
		print(f"Loading 'user:profile:{first_name} {last_name}'")
		data = rc.hgetall(f'user:profile:{first_name} {last_name}')
		return cls(**data)

	@classmethod
	def delete(cls, rc: RedisCluster, first_name: str, last_name: str) -> None:
		print(f"Deleting 'user:profile:{first_name} {last_name}'")
		rc.delete(f'user:profile:{first_name} {last_name}')

	@classmethod
	def exists(cls, rc: RedisCluster, first_name: str, last_name: str) -> bool:
		print(f"Checking if 'user:profile:{first_name} {last_name}' exists")
		return rc.exists(f'user:profile:{first_name} {last_name}')


def bool_as_str(value: bool) -> str:
	return 'Yes' if value else 'No'


def main() -> None:
	nodes = [
		ClusterNode('172.19.0.4', 6379), ClusterNode('172.19.0.3', 6379), ClusterNode('172.19.0.2', 6379),
		ClusterNode('172.19.0.6', 6379), ClusterNode('172.19.0.5', 6379), ClusterNode('172.19.0.7', 6379),
	]
	rc = RedisCluster(startup_nodes=nodes, read_from_replicas=True, decode_responses=True)

	ayfri = Profile(age=21, first_name='Pierre', last_name='Roy', email='pierre.ayfri@gmail.com')
	print("Profile 'ayfri':", ayfri)
	print()

	ayfri.save(rc)

	print("Does 'ayfri' exists ? :", bool_as_str(Profile.exists(rc, 'Pierre', 'Roy')))
	print()

	ayfri2 = Profile.load(rc, 'Pierre', 'Roy')
	ayfri2.age = 30
	ayfri2.last_name = 'Dupont'
	ayfri2.save(rc)
	print("Profile 'ayfri2':", ayfri2)
	print()

	Profile.delete(rc, 'Pierre', 'Dupont')
	print()
	print("Does 'ayfri' exists now ? :", bool_as_str(Profile.exists(rc, 'Pierre', 'Dupont')))


if __name__ == "__main__":
	main()
