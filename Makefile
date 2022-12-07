help:
	@echo "Makefile commands:"
	@echo "build"
	@echo "stop"
	@echo "restart"
	@echo "destroy"
build:
	docker-compose -f docker-compose.yml build -d $(c)
	docker-compose -f docker-compose.yml up -d $(c)
stop:
	docker-compose -f docker-compose.yml stop $(c)
restart:
	docker-compose -f docker-compose.yml stop $(c)
	docker-compose -f docker-compose.yml up -d $(c)
destroy:
	docker system prune -f --volumes $(c)
