create-pipeline:
	sam pipeline init --bootstrap
validate:
	sam validate
remote-invoke:
	sam sync --stack-name dream-bot --watch
local-invoke:
	sam local invoke --event tests/events/event.json
test:
	cd dream-bot/tests && pytest
sync:
	sam sync --stack-name dream-bot --watch --profile dream-bot