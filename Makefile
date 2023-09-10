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

just_intervals        ='[1/1,   16/15, 10/9,   6/5,   5/4, 4/3,   45/32,    64/45, 3/2,    8/5,   5/3,  9/5,    15/8, 2/1]'
pythagorean_intervals ='[1/1, 256/243,  9/8, 32/27, 81/64, 4/3, 729/512, 1024/729, 3/2, 128/81, 27/16, 16/9, 243/128, 2/1]'
pythagorean_intervals_in_turkish_music ='[1/1, 253/243, 2187/2048, 65536/59049, 9/8, 32/27, 19683/16384, 8192/6561, 81/64, 4/3, 177147/131072, 1024/729, 729/512, 262144/177147, 3/2, 128/81, 6561/4096, 32768/19683, 27/16, 16/9, 59049/32768, 4096/2187, 243/128, 1048576/531441, 2/1]'

generate_by_ratios:
	./maqamat.py -R -r $(just_intervals)

generate_by_ratios2:
	./maqamat.py -R -r $(pythagorean_intervals)

generate_by_ratios3:
	./maqamat.py -R -r $(pythagorean_intervals_in_turkish_music)

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
