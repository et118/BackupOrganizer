#Nice trick from https://stackoverflow.com/questions/5618615/check-if-a-program-exists-from-a-makefile
DOCKER_CMD := $(if $(shell command -v podman), podman, docker)

run:
	$(DOCKER_CMD)ghfcompose -f docker-compose.yaml -p backuporganizer_dev up

test:
	$(DOCKER_CMD) compose -f docker-compose-test.yaml -p backuporganizer_test up

production:
	$(DOCKER_CMD) compose -f docker-compose-production.yaml -p backuporganizer_prod up --build --no-deps --force-recreate

clean:
	$(DOCKER_CMD) rmi -f backuporganizer_app:dev backuporganizer_app:prod backuporganizer_app:test
