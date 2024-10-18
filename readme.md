# FastAPI GitHub OAuth2 Example

This is a sample FastAPI application that demonstrates how to implement GitHub sign-in using OAuth2.

## How it works

The app allows users to sign in with their GitHub account via OAuth2. Once authenticated, it retrieves the user's GitHub profile information and displays it on a profile page.

## Key Features
- Sign in with GitHub using OAuth2
- Fetch and display GitHub user information (username, email)
- Uses FastAPI and the `authlib` library to manage OAuth2 flow

### Dependencies
The required dependencies are listed in the `requirements.txt` file. </br>
Also, create an `.env` file similar to the `.env.example` file for configuration.

### GitHub OAuth2 Documentation
For more information on building GitHub OAuth2 apps, refer to the [GitHub OAuth Apps documentation](https://docs.github.com/en/apps/oauth-apps/building-oauth-apps/authorizing-oauth-apps).