setx DOCKER_BUILDKIT 1
setx COMPOSE_DOCKER_CLI_BUILD 1
docker-compose -f .\docker-compose.yml up -d --build
