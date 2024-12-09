# coup
An online platform to play a variation of Chinese Chess (Cờ Úp). This is a webgame where you can play to earn points and coins.

# Public deployment
The project is deployed here:
[https://npham-coup.netlify.app/](https://npham-coup.netlify.app/)

# Available features
Right now, you can create an account, login, view the shop and play matches online through the matchmaking system.

# Guide to use
Since there's no tutorial available for the game yet. Please contact me for instruction how to play.


# Local development
To run the project locally, follow these steps.

## Frontend
For running front end, Nodejs v18 or higher is required. First, navigate to the `frontend` folder.

Then install the dependencies by:

```bash
npm i
```

Finally run development server:

```bash
npm run dev
```

## Backend
For back end, it is more complicated to setup and run. The recommended way is to use docker and docker compose. You can find the guide to install docker [here](https://docs.docker.com/desktop/)

To run a development server, simply navigate to the `backend` folder and run:

```bash
docker compose --env-file .test.env -f ./deploy/common.yml up -d
```

