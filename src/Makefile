.PHONY: git_hooks ci
PROJECT_ROOT_DIR := $(dir $(lastword $(MAKEFILE_LIST)))
GIT_HOOKS_DIR=$(PROJECT_ROOT_DIR)/.git/hooks
GIT_HOOKS=pre-commit
SCRIPT_DIR=$(PROJECT_ROOT_DIR)/script
JENKINS_SCRIPT_DIR=$(SCRIPT_DIR)/jenkins_invoker
PHP=php

help:
	cat Makefile

git_hooks: $(GIT_HOOKS)

$(GIT_HOOKS): relpath:=$(shell (echo "import os"; echo "print(os.path.relpath('contrib/git-hooks', '$(GIT_HOOKS_DIR)'))")| python)
$(GIT_HOOKS):
	-ln -sf $(relpath)/$@ $(GIT_HOOKS_DIR)/

ci: ## run ci test on ecnavi-ci.jenkins
	$(JENKINS_SCRIPT_DIR)/ci-ecnavi.sh

setup-draft: ## run setup-draft on ecnavi-ci.jenkins
	$(JENKINS_SCRIPT_DIR)/setup-draft.sh

setup-rc: ## run setup-rc on ecnavi-deploy.jenkins
	$(JENKINS_SCRIPT_DIR)/setup-rc.sh

install:
	$(PHP) -d memory_limit=-1 $(PHP_OPTS) bin/composer.phar install $(COMPOSER_OPTS)
	cd sites/ecnavi && $(MAKE) install
	cd sites/ecnavi_admin && $(MAKE) install
	$(MAKE) patch

patch:
	-cp patches/JUnit.php vendor/phpunit/phpunit/src/Util/Log/JUnit.php
