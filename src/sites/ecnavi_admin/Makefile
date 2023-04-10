.PHONY: help clean cc test phpmd phpcs phpcbf cibuild cicov phpstan install build/prod build/dev watch kill/watch lint/css fix/css

PROJECT_ROOT:=$(shell dirname $(realpath $(lastword $(MAKEFILE_LIST))))
VENDOR_DIR:=$(realpath $(PROJECT_ROOT)/../../vendor)
REPORT_DIR:=$(PROJECT_ROOT)/build/reports
PHPUNIT:=$(VENDOR_DIR)/bin/phpunit
PHPUNIT_CONF:=phpunit.xml
PHPMD_FORMAT:=text
PHP:=php
PHPSTAN_VERSION=0.11.19
PHPSTAN_LEVEL=2

help:
	@cat Makefile

clean:
	rm -rf build

cc:
	php apps/lib/common/bin/cc.php

test: cc
	$(PHPUNIT) -c $(PHPUNIT_CONF) $(TARGET) || true

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
	yarn webpack --config webpack.prod.js

build/dev: install
	yarn webpack --config webpack.dev.js

watch: kill/watch install
	yarn webpack --config webpack.dev.js --watch

kill/watch:
	ps u | grep -v grep | grep $(PROJECT_ROOT)/ | grep webpack | grep watch | awk '{ print "kill",$$2}' | sh

lint/css: install
	yarn stylelint $(TARGET)

fix/css: install
	yarn stylelint $(TARGET) --fix
