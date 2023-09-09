.DEFAULT_GOAL := help

.PHONY:

SHELL=bash
export DIFF_PROGRAM:=vimdiff

TET_INTERVALS =5 7 9 10 12 17 19 22 24 31 34 41 53 60 72 79

TET_INTERVAL  =12

generate_all: ## generate all equally tempered chromatic scales, and by ratios
	@$(MAKE) --silent generate_all_by_ets;
	@$(MAKE) --silent generate_all_by_ratios

generate_all_by_ets: ## generate all defined equally tempered chromatic scales
	@$(foreach TET_INTERVAL, $(TET_INTERVALS), \
		$(MAKE) --silent generate_by_et TET_INTERVAL=$(TET_INTERVAL);)

generate_all_by_ratios:
	@$(MAKE) --silent generate_by_ratios

generate_by_et: ## generate chromatic scale of TET_INTERVAL, e.g. make generate TET_INTERVAL=24
	./maqamat.py -E -i $(TET_INTERVAL); echo

generate_by_ratios:
	./maqamat.py -R

print-%: ## print a variable and its value, e.g. print the value of variable PROVIDER: make print-PROVIDER
	@echo $* = $($*)

define print-help
$(call print-target-header,"Makefile Help")
	echo
	printf "%s\n" "Illustrates how to use Maqamat.py"
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
