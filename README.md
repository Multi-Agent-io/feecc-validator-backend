# Feecc Validator Backend

Feecc Validator Backend is a microservice, designed to handle validating certificates and getting data associated with
the unit provided user has only one of the data pieces.

It provides a simple REST API interface to validate certificates issued by Feecc.

Feecc Validator Backend comes as a part of the Feecc, a Web3 enabled production tracking system.

Validator Backend is a microservice that is written in asynchronous Python using FastAPI framework.

## Deployment

The app is supposed to be run in a Docker container and can be configured by setting several environment variables.

> Note, that we assume a Linux host in this guide, however you can also run Validator Backend on any other OS, but be warned: timezone is defined by mounting host `/etc/timezone` and `/etc/localtime` files inside the container, which are not present on Windows machines, so you might end up with UTC time inside your container.

Start by cloning the git repository onto your machine:
```
git clone https://github.com/Multi-Agent-io/feecc-validator-backend.git
```

Enter the app directory and modify the `docker-compose.yml` file to your needs by changing the environment variables (discussed in the configuration part).

```
cd feecc-validator-backend
vim docker-compose.yml
```

When you are done configuring your installation, build and start the container using docker-compose:
```
sudo docker-compose up --build
```

Verify your deployment by going to http://127.0.0.1:8084/docs in your browser. You should see the SwaggerUI API specification page. Continue from there.

## Configuration

To configure your Validator Backend deployment edit the environment variables, provided in `docker-compose.yml` file.

Environment variables:

- `MONGO_CONNECTION_URL` — your MongoDB connection URI ending with `/db-name`;
- `IPFS_DISPLAY_GATEWAY_LINK` — IPFS web gateway base for end user access URL. Defaults
  to `https://gateway.ipfs.io/ipfs`.
- `IPFS_PARSING_GATEWAY_LINK` — IPFS web gateway base URL for parsing files. Defaults
  to `https://multiagent.mypinata.cloud/ipfs`.
- `BLOCK_EXPLORER_LINK` — Block explorer base URL. Defaults to `https://robonomics.subscan.io/extrinsic`
