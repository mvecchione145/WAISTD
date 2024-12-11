set dotenv-load


format-tf:
	@terraform fmt -recursive

plan env:
	@cd terraform && terraform init -reconfigure --backend-config env/{{ env }}.tfbackend && terraform plan --var-file env/{{ env }}.tfvars

apply env:
	@cd terraform && terraform init -reconfigure --backend-config env/{{ env }}.tfbackend && terraform apply --var-file env/{{ env }}.tfvars

format-py:
	@black src
	@isort src --profile black
	@mypy src --raise-exceptions

format: format-py format-tf

unittest:
	@pytest -vv

reqs:
	@poetry export --format requirements.txt --without-hashes --output requirements.txt

build env:
	@docker build -t ${IMAGE_NAME}-{{ env }} .

tag env:
	@aws ecr get-login-password --region ${REGION} | docker login --username AWS --password-stdin ${AWS_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com
	@docker tag ${IMAGE_NAME}-{{ env }} ${AWS_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${IMAGE_NAME}-{{ env }}
	@docker push ${AWS_ACCOUNT_ID}.dkr.ecr.${REGION}.amazonaws.com/${IMAGE_NAME}-{{ env }}

done env: format unittest reqs
	@just build {{ env }}
	@just tag {{ env }}
	@just apply {{ env }}

destroy env:
	@cd terraform && terraform init -reconfigure --backend-config env/{{ env }}.tfbackend && terraform destroy --var-file env/{{ env }}.tfvars