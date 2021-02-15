# Github_SNS

## Goals
`[ririro93]`
- try django-allauth
- keep to git commit conventions

<br>

`[sean]`
- get used to git, django
- research github api


<br>

## Todos
- [ ] front-end
    - [ ] navbar
    - [ ] django messages
    - [ ] register page
    - [ ] login page
        - [ ] form validation -> use bootstrap?
    - [ ] profile page
    - [ ] home page
    - [ ] feeds

- [ ] back-end
    - [ ] crawling github repos
    - [ ] socials login using allauth
        - [x] google
        - [ ] github
        - [ ] facebook
        - [ ] twitter
    - [ ] logout redirect to login page
        - [ ] show logged out message

- [ ] db
    - [ ] migrate to postgres

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

- [ ] etc
    - [ ] add license

<br>

## Today
### (02-14) 
`[ririro93]`

Task
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

## Reference
(1) [medium post](https://whizzoe.medium.com/in-5-mins-set-up-google-login-to-sign-up-users-on-django-e71d5c38f5d5) : google login <br>
(2) [iconfinder](https://www.iconfinder.com/social-media-icons) : sns icons