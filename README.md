# Game Shelf
### View the live project [here.](https://nick-game-shelf.herokuapp.com/)

Game Shelf is a site that hopes to provide easily accessible reviews and details of tabletop board games. The site will be targeted towards existing tabletop board game players and collectors who are looking for new games to play and collect, but also aimed at new gamers who may not know where to start. Game Shelf will be useful for gamers to find detailed reviews of games they may be interested in, and allow them to find all the necessary details of games.


## Table of Contents

> -	[Overview](#overview)
> -	[Description](#description)
> -	[UX](#ux)
> -	[Features](#features)
> -	[Technologies Used](#technologies-used)
> -	[Testing](#testing)
> -	[Project bugs and solutions](#project-bugs-and-solutions)
> - [Deployment](#deployment)
> -	[Credits](#credits)
> - [Acknowledgements](#acknowledgements)

## Overview
Tabletop gaming is taking the world by storm right now, and the board games industry is booming. There are now literally hundreds of games being published every year, and there has never been a better time to be a gamer, or to get involved. But it can be a minefield to negotiate and find the *right* games, whether you're a seasoned board gamer or complete newcomer. **_Game Shelf_** aims to provide accurate and comprehensive board game information and reviews that are easily accessible to everyone, and make choosing your next (or first!) board game as straightforward as possible.


## Description
**_Game Shelf_** is a board games review site built with a mobile-first design, but intended to be accessible on all devices. My aim with the project is to present the most relevant information alongside easily digestible reviews to enable users to quickly and easily decide which games to play next.

## User Experience (UX)

-   ### User stories

    -   #### First Time Visitor Goals

        1. As a First Time Visitor, I want to easily understand the main purpose of the site and learn more about board games.
        2. As a First Time Visitor, I want to be able to easily navigate the site to find content.
                       
    -   #### Returning Visitor Goals

        1. As a Returning Visitor, I want to find information about games I may want to play
        2. As a Returning Visitor, I want to share my reviews of games I have played     

    -   #### Frequent User Goals

        1. As a Frequent User, I want to check to see if there are any new reviews or new games added.
        2. As a Frequent User, I want to organise the games I own on my profile.

    -   #### Site Owner Goals

        1. As a Site Owner, I want to earn money on games purchased through affiliate links  

 
## Scope

## Structure

## Skeleton

## Surface

### Images
### Colours
### Typography
### Icons


## Features

### Existing Features


### Features Left to Implement


## Technologies Used

#### Languages:
* [HTML](https://en.wikipedia.org/wiki/HTML)
* [CSS](https://en.wikipedia.org/wiki/CSS)
* [JavaScript](https://en.wikipedia.org/wiki/JavaScript)
* [Python](https://en.wikipedia.org/wiki/Python_(programming_language))


#### Libraries:
* [Balsamiq](https://balsamiq.com/) - used for the creation of wireframes.

#### Version Control:
* [Github](https://github.com/) - Used to store the code 
* [Gitpod](https://gitpod.io/) - Used as the primary version control IDE for development to further push and commit code to GitHub.
* [Heroku](https://www.heroku.com/home) - Used to deploy the live site

#### Other:
* [Code Institute Course Content](https://courses.codeinstitute.net/) - Primary source of learning code.
* [Stack Overflow](https://stackoverflow.com/) - Used for general troubleshooting and examples.
* [W3Schools](https://www.w3schools.com/) - Used for examples and tutorials.
* [ChromeDevTools](https://developers.google.com/web/tools/chrome-devtools) - Used frequently to detect any issues/bugs or layout differences.

---

## Testing

#### Validation

#### Project Bugs and Solutions
* CSS for page overflow and x-scrolling meant the games catalogue table was cutting off anything that went beyond the edge of the screen on mobile devices; removing overflow:hidden meant that any horizontal scrolling moved the whole page (leaving ugly whitespace on the righthand side of the page). In order to add x-scrolling to the catalogue table only, I found and used an answer from [Serge Stroobandt](https://stackoverflow.com/a/30423904) on Stack Overflow which meant users are able to scroll horizontally in the table only without compromising the layout of the table itself, or adding any whitespace to other elements on the page.

#### Testing User Stories

## Deployment

### GitHub

* Go to [GitHub](https://github.com/) and sign in, or sign up for an account.
* Once a Github account was created, I opened a new repository by clicking the green button "new". To create this project, I used the Code Institute's student 
[template](https://github.com/Code-Institute-Org/gitpod-full-template).
* Click on the green "gitpod" button to open [Gitpod](https://gitpod.io/), a cloud-based version control software or IDE, which was used to write all code for this project.
* It was then pushed or saved in the terminal to Github where it is stored in a [repository](https://github.com/NickChapman1988/game-shelf)

### Heroku

The project was deployed to Heroku using the following steps:

1. Create a "requirements.txt" file using the `pip3 freeze --local > requirements.txt` command.
2. Create a Profile using the `echo web: python app.py > Procfile` command.
3. Delete the blank line at the bottom of the Procfile, as this can sometimes cause problems when running the app on Heroku.
4. Add, commit and push these new files to GitHub.
5. Navigate to [Heroku](https://www.heroku.com/home) and log in to the dashboard.
6. Click "Create a New App".
7. Enter a unique app name and select the closest region ('Europe' in my case).
8. Click "Create App".
9. Under 'Deployment Method' click GitHub.
10. Once the GitHub profile is displayed, add the GitHub repository name then click "Search".
11. Once the repository is found, click to connect to the app.
12. As the environment variables are hidden in an env.py file, these need to be added to the Config Vars in Heroku
13. Go to the 'Settings' tab for the app, then click on "Reveal Config Vars" and enter the key:value pairs from the env.py file. 
14. Back in the 'Deploy' tab, click "Enable Automatic Deployment" then below that, make sure the main branch is selected and click "Deploy Branch" 
15. Once the app has successfully deployed, click "View" to launch the app.

### Forking the GitHub Repository

Forking the GitHub repository creates a copy of the original repository on your own GitHub account to view and/or make changes without affecting the original repository; use the following steps to fork:

1. Log in to GitHub and locate the GitHub [repository](https://github.com/NickChapman1988/game-shelf)
2. At the top of the repository above the "Settings" button on the menu, locate the "Fork" button.
3. You should now have a copy of the repository in your own GitHub account.

### Making a local Clone

1. Log in to GitHub and locate the GitHub [repository](https://github.com/NickChapman1988/game-shelf)
2. At the top of the repository, click the "Code" button (next to the green "Gitpod" button)
3. Under "Clone with HTTPS", copy the URL provided
4. Open Git Bash
5. Change the current working directory to the location where you want the cloned directory
6. Type `git clone`, and then paste the URL you copied in Step 3.

```
$ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
```

7. Press Enter. Your local clone will be created.

```
$ git clone https://github.com/YOUR-USERNAME/YOUR-REPOSITORY
> Cloning into `CI-Clone`...
> remote: Counting objects: 10, done.
> remote: Compressing objects: 100% (8/8), done.
> remove: Total 10 (delta 1), reused 10 (delta 1)
> Unpacking objects: 100% (10/10), done.
```

Click [here](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository#cloning-a-repository-to-github-desktop) to retrieve pictures for some of the buttons and more detailed explanations of the above process.

## Credits
* Horizontal scrolling added to games catalogue table thanks to [this answer](https://stackoverflow.com/a/30423904) from Serge Stroobandt on Stack Overflow.

## Acknowledgements

