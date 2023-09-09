.DEFAULT_GOAL := help

.PHONY:

SHELL=bash
export DIFF_PROGRAM:=vimdiff

generate_%:
	./maqamat.py -E -i $*

generate_by_ratios:
	./maqamat.py -R

generate_all: ## generate all equally tempered chromatic scales, by ratios
	@$(MAKE) --silent generate_7; echo;
	@$(MAKE) --silent generate_12;echo;
	@$(MAKE) --silent generate_17;echo;
	@$(MAKE) --silent generate_24;echo;
	@$(MAKE) --silent generate_31;echo;
	@$(MAKE) --silent generate_53;echo;
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
