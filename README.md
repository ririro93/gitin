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
    - [ ] logout redirect to login page

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
- started working on login page
    - implemented google login (1) with icons (2)

problems
- logout redirect does not take user back to login page 
- -> intended : redirect to `accounts/login`
- -> instead redirects to `accounts/logout/accounts/login`



<br>

## Reference
(1) [medium post](https://whizzoe.medium.com/in-5-mins-set-up-google-login-to-sign-up-users-on-django-e71d5c38f5d5) : google login <br>
(2) [iconfinder](https://www.iconfinder.com/social-media-icons) : sns icons