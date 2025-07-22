curl -SL https://github.com/docker/compose/releases/download/v2.37.3/docker-compose-linux-x86_64 -o /usr/local/bin/docker-compose

 Start-BitsTransfer -Source "https://github.com/docker/compose/releases/download/v2.37.3/docker-compose-windows-x86_64.exe" -Destination $Env:ProgramFiles\Docker\docker-compose.exe

 composer create-project hunwalk/yii2-basic-firestarter <project_pilot_AI> --prefer-dist

 php yii migrate-user
 php yii migrate-rbac
 php yii migrate

 cp .env.example .env

npm install --save-dev @commitlint/config-conventional @commitlint/cli
echo "export default {extends: ['@commitlint/config-conventional']};" > commitlint.config.js

npm install commitizen -g

npm
commitizen init cz-conventional-changelog --save-dev --save-exact

# yarn
commitizen init cz-conventional-changelog --yarn --dev --exact

# pnpm
commitizen init cz-conventional-changelog --pnpm --save-dev --save-exact

npx commitizen init cz-conventional-changelog --save-dev --save-exact


npm install --save-dev @commitlint/config-conventional @commitlint/cli
echo "export default {extends: ['@commitlint/config-conventional']};" > commitlint.config.js

npm install commitizen -g

npm
commitizen init cz-conventional-changelog --save-dev --save-exact

# yarn
commitizen init cz-conventional-changelog --yarn --dev --exact

# pnpm
commitizen init cz-conventional-changelog --pnpm --save-dev --save-exact

npx commitizen init cz-conventional-changelog --save-dev --save-exact

cd ./bizz
yarn create semantic-module

# 1) Clone and enter the project
$ git clone https://github.com/Web4application/Bizz.git
$ cd Bizz

# 2) Python deps – create & activate venv
$ python -m venv .venv && source .venv/bin/activate
$ pip install -U pip
$ pip install -r requirements.txt  # or `poetry install`

# 3) Node/TS deps (if package.json exists)
$ npm ci

# Python API service (FastAPI / Flask)
$ uvicorn app.main:app --reload --port 8000

# TypeScript micro‑service
$ npm run dev

# Unified task runner
$ make dev  # wire both in tmux

# Build image
$ docker build -t web4app/bizz:dev .

# Run container
$ docker run -p 8000:8000 --env-file .env web4app/bizz:dev
