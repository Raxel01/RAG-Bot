
COMPOSEFILE = /goinfre/abait-ta/RAG-Bot/docker-compose.yml


up: 
	docker compose -f ${COMPOSEFILE} up --detach

stop:
	docker compose -f ${COMPOSEFILE} stop

start:
	docker compose -f ${COMPOSEFILE} start

down:
	docker compose -f ${COMPOSEFILE} down --rmi all -v

fclean: down
	docker system prune -af

global: stop fclean up