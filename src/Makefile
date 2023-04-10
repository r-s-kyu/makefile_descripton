# 命名規則 [a/b] aに対するbを実行する
# 誤実行がまずいものは先頭に__(アンダーバー2つ)をつけるようにする


.PHONY: init
init: flyway/baseline

##
# docker 関連
#
.PHONY: docker/inspect
docker/inspect:
	docker inspect --format='{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $(s)

##
# docker compose 関連
#
.PHONY: docker-compose/build
docker-compose/build:
	docker compose build

.PHONY: docker-compose/up
docker-compose/up:
	docker compose up

.PHONY: docker-compose/up-d
docker-compose/up-d:
	docker compose up -d

.PHONY: docker-compose/down
docker-compose/down:
	docker compose down

s :=
.PHONY: docker-compose/exec
docker-compose/exec:
	docker compose exec $(s) bash

.PHONY: docker-compose/logs
docker-compose/logs:
	docker compose logs $(s)

.PHONY: docker-compose/logs-f
docker-compose/logs-f:
	docker compose logs $(s) -f

.PHONY: docker-compose/ps
docker-compose/ps:
	docker compose ps

.PHONY: __docker-compose/down-rm
__docker-compose/down-rm:
	docker compose down --rmi all --remove-orphans -v

##
# db 関連
#
DBNAME := guild-hack
.PHONY: db/exec
db/exec:
	docker compose exec db mysql -u guild-hack -pguild-hack

.PHONY: __db/drop
__db/drop:
	docker compose exec db mysql -u guild-hack -pguild-hack -e'drop databases $(DBNAME)'

.PHONY: __db/data-rm
__db/data-rm:
	rm -rf database/data/*

##
# flyway 関連
#
.PHONY: flyway/info
flyway/info:
	docker compose run --rm flyway info

.PHONY: flyway/validate
flyway/validate:
	docker compose run --rm flyway validate

.PHONY: flyway/migrate
flyway/migrate:
	docker compose run --rm flyway migrate

.PHONY: flyway/repair
flyway/repair:
	docker compose run --rm flyway repair

.PHONY: flyway/baseline
flyway/baseline:
	docker compose run --rm flyway baseline -baselineVersion=1 -baselineDescription="default tables"

.PHONY: flyway/clean
__flyway/clean:
	docker compose run --rm flyway clean

##
# go 関連
#
.PHONY: go/fmt
go/fmt:
	gofmt -l -s -w

.PHONY: go/vet
go/vet:
	go vet ./...

.PHONY: go/get
go/get:
	go get -v ./...

.PHONY: go/install
go/install:
	go install github.com/go-swagger/go-swagger/cmd/swagger@latest

.PHONY: go/gen
go/gen:
	swagger generate model -f swagger.yaml -m generated_swagger -t ./swagger