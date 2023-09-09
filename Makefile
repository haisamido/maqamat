.DEFAULT_GOAL := help

.PHONY:

SHELL=bash
export DIFF_PROGRAM:=vimdiff

TET_INTERVALS=5 7 9 10 12 17 19 22 24 31 34 41 53 60 72 79

generate_%:
	./maqamat.py -E -i $*; echo

generate_by_ratios:
	./maqamat.py -R

generate_all: ## generate all equally tempered chromatic scales, by ratios
	@$(MAKE) --silent generate_5
	@$(MAKE) --silent generate_7
	@$(MAKE) --silent generate_9
	@$(MAKE) --silent generate_10
	@$(MAKE) --silent generate_12
	@$(MAKE) --silent generate_17
	@$(MAKE) --silent generate_19
	@$(MAKE) --silent generate_22
	@$(MAKE) --silent generate_24
	@$(MAKE) --silent generate_31
	@$(MAKE) --silent generate_34
	@$(MAKE) --silent generate_41
	@$(MAKE) --silent generate_53
	@$(MAKE) --silent generate_60
	@$(MAKE) --silent generate_72
	@$(MAKE) --silent generate_79
	@$(MAKE) --silent generate_by_ratios

print-%: ## print a variable and its value, e.g. print the value of variable PROVIDER: make print-PROVIDER
	@echo $* = $($*)

define print-help
$(call print-target-header,"Makefile Help")
	echo
	printf "%s\n" "Illustrates how to use IaC tools by example. It will be different in operations"
	echo
$(call print-target-header,"target                         description")
	grep -E '^([a-zA-Z_-]).+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS=":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}' | grep $(or $1,".*")
	echo
endef

help:
	@$(call print-help)

help-%: ## Filtered help, e.g.: make help-terraform
	@$(call print-help,$*)

print-%:
	@echo $*=$($*)
