image:
	docker build -t galadriel . -f Dockerfiles/Dockerfile

export:
	docker save galadriel -o galadriel.container
