# {{PROJECT_NAME}}

Welcome to the {{PROJECT_NAME}}!

## Setup

Make sure you have the right version of python and all the dependencies
required. Install the npm modules for using the tailwind post processor.
Install [flyctl](https://fly.io/docs/hands-on/install-flyctl/) which is the
[fly.io](https://fly.io/) cli that is used to deploy the app. Setup your
`environment.sh` file with new values using the sample file as the guide.

```shell
> python --version
Python 3.9.6
> pip install -r requirements.txt
> node --version
v18.9.1
> npm --version
9.6.4
> npm install -g localtunnel
> lt --version
2.0.2
> npm i
> curl -L https://fly.io/install.sh | sh
> cp environment.sh.sample environment.sh
> vim environment.sh
> source environment.sh
```

## Run Development Server

The dev server is auto loading when a file is changed.

```
> make dev
```

## Deploy the Server to Production

```
> make deploy
```

## Add a secret to fly.io

```
> fly secrets set KEY=VALUE
```
