[tool.poetry]
name = "bizz"
version = "0.1.0"
description = "Business automation toolkit with AI assistant, data upload, and deployable UI"
authors = ["Web4application <your@email.com>"]
license = "MIT"
readme = "README.md"
packages = [{ include = "scripts" }, { include = "tests" }]

[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.110.0"
uvicorn = { extras = ["standard"], version = "^0.27.1" }
pydantic = "^2.6"
requests = "^2.32.0"
python-dotenv = "^1.0.1"

[tool.poetry.group.dev.dependencies]
pytest = "^8.2.0"
httpx = "^0.27.0"
pre-commit = "^3.7.0"

[tool.poetry.scripts]
bizz = "scripts.bizz_cli:main"

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"
