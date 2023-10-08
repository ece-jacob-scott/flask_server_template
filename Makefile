PROJECT_NAME={{PROJECT_NAME}}
SOURCE_FILES={{PROJECT_NAME}}/*.py

.PHONY: build
build: $(SOURCE_FILES)
	@npm run build-tailwind
	@echo "built!"

.PHONY: create_database
create_database:
	@echo "Creating database..."
	flask --app {{PROJECT_NAME}} create_database

.PHONY: run
run: build create_database
	flask --app {{PROJECT_NAME}} run

.PHONY: dev
dev: build create_database
	flask --app {{PROJECT_NAME}} run --debug

.PHONY: deploy
deploy: build
	fly deploy

.PHONY: localtunnel
localtunnel:
	@echo "make sure you are running the server locally in another terminal"
	@echo "Your public IP address is:"
	curl ipv4.icanhazip.com
	lt --port ${FLASK_RUN_PORT}
