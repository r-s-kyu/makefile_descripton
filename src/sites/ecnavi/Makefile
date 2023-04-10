.PHONY: help clean cc test test/js phpcs phpcbf cibuild cicov phpstan install build/prod build/dev watch kill/watch lint/js fix/js fix/js/eslint fix/js/prettier lint/css fix/css storybook next/dev next/build next/build/dev

PROJECT_ROOT:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
VENDOR_DIR:=$(realpath $(PROJECT_ROOT)/../../vendor)
REPORT_DIR:=$(PROJECT_ROOT)/build/reports
PHPUNIT:=$(VENDOR_DIR)/bin/phpunit
PHPUNIT_CONF:=phpunit.xml
PHPMD_FORMAT:=text
PHP:=php
PHPSTAN_VERSION=0.11.19
PHPSTAN_LEVEL=2
FILES_PER_BUILD=2
DIRS='' # カンマ区切りでassets/(js|css)/以下のディレクトリ名を指定する。例: DIRS=top,m/top
USER=$(shell whoami)
PRODUCT_ENV=dev
PERSONAL_ENV=
NEXT_OUTDIR=apps/view/out/
NEXT_PUBLIC_API_MOCKING=disabled
CURRENT_COMMIT_HASH=$(shell git show --format='%H' --no-patch)

help:
	@cat Makefile

clean:
	rm -rf build

cc:
	php apps/lib/common/bin/cc.php

test: cc
	$(PHPUNIT) -c $(PHPUNIT_CONF) $(TARGET) || true

test/js: install
	yarn jest --runInBand

test/js/updateSnapshot: install
	yarn jest --updateSnapshot

phpmd.phar:
	curl -SsOL http://static.phpmd.org/php/latest/phpmd.phar && chmod +x phpmd.phar

phpmd: phpmd.phar
	php -d memory_limit=-1 phpmd.phar $(PHPMD_OPTS) $(or $(TARGET),.) $(PHPMD_FORMAT) phpmd-ruleset.xml || true

phpcs.phar:
	curl -SsOL https://squizlabs.github.io/PHP_CodeSniffer/phpcs.phar && chmod +x phpcs.phar

phpcs: phpcs.phar
	php -d memory_limit=-1 phpcs.phar --standard=phpcs.xml $(PHPCS_OPTS) $(TARGET)

phpcbf.phar:
	curl -SsOL https://squizlabs.github.io/PHP_CodeSniffer/phpcbf.phar && chmod +x phpcbf.phar

phpcbf: phpcbf.phar
	php -d memory_limit=-1 phpcbf.phar --standard=phpcs.xml $(PHPCBF_OPTS) $(TARGET)

cibuild:
	$(MAKE) test PHPUNIT_CONF=phpunit.xml.cibuild TARGET=$(TARGET)

cicov:
	$(MAKE) test PHPUNIT_CONF=phpunit.xml.cicov
	$(MAKE) phpmd PHPMD_FORMAT=xml PHPMD_OPTS='--reportfile $(REPORT_DIR)/phpmd.xml'

phpstan.phar:
	curl -SsOL https://github.com/phpstan/phpstan/releases/download/$(PHPSTAN_VERSION)/phpstan.phar && chmod +x phpstan.phar

phpstan: phpstan.phar
	$(PHP) -d memory_limit=-1 phpstan.phar analyse --no-progress -l $(PHPSTAN_LEVEL) apps src

install:
	yarn install --immutable

build/prod: install
	$(MAKE) webpack/build/prod PRODUCT_ENV=$(PRODUCT_ENV)
	$(MAKE) next/publish PRODUCT_ENV=$(PRODUCT_ENV)

build/dev: install
	$(MAKE) webpack/build/dev
	$(MAKE) next/publish

webpack/build/prod: install
	$(CURDIR)/script/webpack build_prod $(DIRS) $(PRODUCT_ENV)

webpack/build/dev: install
	$(CURDIR)/script/webpack build_dev $(DIRS) dev

watch: kill/watch install
	$(CURDIR)/script/webpack watch $(DIRS) $(PRODUCT_ENV)

kill/watch:
	ps u | grep -v grep | grep $(PROJECT_ROOT)/ | grep webpack | grep watch | awk '{ print "kill",$$2}' | sh

lint/js: install
	yarn eslint "**/*.{ts,tsx}"
	yarn tsc --noEmit -p ./tsconfig.webpack.json
	yarn tsc --noEmit -p ./tsconfig.json

fix/js: install
	$(MAKE) fix/js/prettier
	$(MAKE) fix/js/eslint

fix/js/eslint: install
	yarn eslint "**/*.{ts,tsx}" --fix

fix/js/prettier: install
	yarn prettier --check --write "**/*.{ts,tsx}"

lint/css: install
	yarn stylelint "$(TARGET)"

fix/css: install
	yarn stylelint "$(TARGET)" --fix

storybook: install
	yarn start-storybook -p 9009 --static-dir 'public_html'

next/dev: install
	USER=$(USER) PRODUCT_ENV=$(PRODUCT_ENV) PERSONAL_ENV=$(USER) CURRENT_COMMIT_HASH=$(CURRENT_COMMIT_HASH) yarn node server.js

next/build: install
	PRODUCT_ENV=$(PRODUCT_ENV) PERSONAL_ENV=$(PERSONAL_ENV) NEXT_PUBLIC_API_MOCKING=$(NEXT_PUBLIC_API_MOCKING) CURRENT_COMMIT_HASH=$(CURRENT_COMMIT_HASH) yarn next build && yarn next export -o $(NEXT_OUTDIR)

next/publish:
	$(MAKE) next/build PRODUCT_ENV=$(PRODUCT_ENV) PERSONAL_ENV=$(PERSONAL_ENV) CURRENT_COMMIT_HASH=$(CURRENT_COMMIT_HASH)

next/publish/personal:
	$(MAKE) next/publish PERSONAL_ENV=$(USER) CURRENT_COMMIT_HASH=$(CURRENT_COMMIT_HASH)