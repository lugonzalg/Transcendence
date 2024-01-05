NAME=trans
PWD= /Users/edurne/Desktop/trans/Services/BBDD/login
CONTAINER=bbdd_login
IMAGE=bbdd_login_image



all: $(NAME)

$(NAME):
	docker compose -f $(PWD)/docker-compose.yml up -d

clean:
	docker compose -f $(PWD)/docker-compose.yml down --volumes
	docker system prune -f

fclean: clean
	-docker rmi postgres_login

re:	fclean all

.phony: clean fclean all re