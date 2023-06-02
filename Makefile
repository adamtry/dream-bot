create-pipeline:
	sam pipeline init --bootstrap
validate:
	sam validate
remote-invoke:
	sam sync --stack-name dream-bot --watch
local-invoke:
	make build && sam local invoke --event events/telegram_webhook_event.json
test:
	cd dream-bot/tests && pytest
build:
	sam build --use-container --template-file template.yaml
deploy:
	sam deploy --stack-name dream-bot --profile dream-bot
update-deps:
	make build && sam deploy --stack-name dream-bot --profile dream-bot --capabilities CAPABILITY_IAM
stream-logs:
	aws logs tail "/aws/lambda/dream-bot" --follow --profile dream-bot --format short
sync:
	sam sync --stack-name dream-bot --watch --profile dream-bot