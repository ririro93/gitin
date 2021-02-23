# Github_SNS

## Goals
`[ririro93]`
- try django-allauth
- keep to git commit conventions
- get used to CBV
- try Typescript
- study datetime objects, timezones(naive)

<br>

`[sean]`
- get used to git, django
- research github api

<br>

## Todos
- [ ] front-end
    - [ ] navbar
    - [ ] django messages
    - [ ] signup page
        - [ ] add interests tags
    - [ ] login page
        - [ ] form validation -> use bootstrap? or django.contrib.auth.authenticate?
        - [ ] consider github as the only main socials login
        - [ ] reset password page
    - [ ] profile page
        - [ ] Items
            - [ ] gihub.io link
            - [ ] bio
            - [ ] interests
            - [ ] follwers / following
        - [ ] Research other services
    - [ ] home page
    - [ ] feeds
    - [ ] repo view
        - [x] basic view
    - [ ] file view
        - [ ] commenting section
            - [ ] comments for every file
            - [ ] pressing comment can highlights specific section
            - [x] sticky-top not working
            - [ ] 1 min ago facebook like timestamp
                - [stackoverflow](https://stackoverflow.com/questions/3177836/how-to-format-time-since-xxx-e-g-4-minutes-ago-similar-to-stack-exchange-site/23259289#23259289)
        - [ ] contents section
            - [ ] markdown is highlighted like a python file for some reason
            - [x] html tags are shown like processed markdown file -> fixed
        - [ ] explorer
            - [x] tree view
            - [ ] fold all feature
            - [x] independent scrollbar

- [ ] back-end
    - [x] get repo data from github API
    - [ ] socials login using allauth
        - [x] google
        - [x] github
        - [ ] facebook
        - [x] twitter
    - [ ] if user tries to sign in using a username that already exists on Github -> ask if same person
        - yes -> would you like to sign in using your github account?
        - no -> please choose a different username. 
    - [x] logout redirect to previous page
    - [ ] show logged out message
    - [ ] using github API's search might be better than using PyGithub get_user() and get_repo() methods
        -[ ] this feature existed on PyGithub too.. -> update using this

- [ ] db
    - [ ] migrate to postgres
    - [ ] button on RepoDetailView page to update db

- [ ] features
    - [ ] follow other people
    - [ ] when mutually following -> relation : friend (is this needed for github?)
    - [ ] show repos in a friendlier way
    - [ ] comments + likes
        - [ ] threads -> main comment on the side
    - [ ] suggestions -> repos with similar projects, languages
    - [ ] repo : auto-tag difficulty
    - [ ] repo : different visuals according to # of commits
    - [ ] repo : see all liked repos all organized in one page
    - [ ] feeds : when new repo created
    - [ ] starter guide for ppl new to programming
        - [ ] make guide interactive (embedded live code editors & terminals)
    - [ ] comments section that moves around

- [ ] etc
    - [ ] add license

<br>

## Today
### (02-14) 
`[ririro93]`

Tasks
- started working on login page
    - implemented google login (1) with icons (2)

Problems
- [x] logout redirect does not take user back to login page 
    - intended : redirect to `accounts/login`
    - instead redirects to `accounts/logout/accounts/login`
    - -> `fixed by using {% url 'login' %} and likewise`
- [x] navbar doesn't work correctly when not starting from root url
    - > `also fixed by using {% url 'login' %} and likewise`
- [ ] login with google makes username ririro931 instead of ririro93 because it already exists
    - [ ] let new username be ririro93@gmail.com instead
    - [ ] logout also doesn't logout from google
        - [ ] next login attempt just lets you go right through
- [ ] django message 'successfully signed in' stays forever

<br>

### (02-15)

`[ririro93]`
 
 Tasks
 - [x] accounts
    - [x] implement github, twitter login
    - [x] signup_page
 - [x] gitAPI
    - [x] recieve repo data according to requested username   

<br>

### (02-16)

`[ririro93]`

Tasks
- [x] gitAPI
    - [x] create models for users and repos
    - [x] added view for Creating and Updating these models
    - [x] entering an Github username in the navbar input activates the Creating and Updating

Learned
- there might be an easier way but for now I can get a list of all field names of a model by using <br>
`list(map(lambda x: x.name, <ModelName>._meta.fields))`

Problem
- [ ] repos with same names from different Github users 
- [ ] inputting same username twice should only update the datetime fields of the GithubRepo model

<br>

### (02-17)

`[ririro93]`

Learned
- (3) adding ImageField to a model requires the following
    - adding MEDIA_URL, MEDIA_ROOT to settings
    - adding `static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)` to urlpatterns
    - calling image via url `src="{{ user.gitinuser.profile_img.url }}"`

<br>

### (02-17)

`[ririro93]`

Problem
- [x]: GET request to github's API for commits only gives 30 recent commits -> find way to get all commits -> used Pygithub
- [x]: found out that there is a 5000 API request limit per hour per ip address -> adding all 30 most recent commits per repo maybe too costly -> 5000 was enough was only using 60 because of no authentication -> used access token to raise limit

### (02-22)
`[ririro]`

Learned
- [CSS] use `white-space: nowrap` with `overflow-x: scroll` to get horizontal scrollbar

<br>

## References
(1) [medium post](https://whizzoe.medium.com/in-5-mins-set-up-google-login-to-sign-up-users-on-django-e71d5c38f5d5) : google login <br>
(2) [iconfinder](https://www.iconfinder.com/social-media-icons) : sns icons <br>
(3) [ImageField](https://studygyaan.com/django/how-to-upload-and-display-image-in-django) : profile image
(4) [dev.to](https://dev.to/radualexandrub/how-to-create-a-comment-section-for-your-django-blog-3egp)