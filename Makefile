setup:
	mkdir -p ./config ./dags ./logs ./plugins ./tests

up:
	docker compose up -d

down:
	docker compose down

clean:
	docker compose down -v

restart: down up

reset: down clean up
