# Project Specification

## Product Backlog
I've broken down the functionality of my project based off the two roles availble to users, administrators (Admin) and general users (Players) and also backend server jobs.

### Players
- Upon visiting the homepage, new players can register for the site and will receive an email to verify their account similar to my social network.
- Once registered, players will have access to an editable profile page that will display personal info including their phone number and email to allow an easy way to share contact information with other players to schedule games.
- A player's profile page will also display their personal statistics across all match and teams played on.
- All players can view a list of every player on a seperate page, and also view those players' profiles.
- All players can view a global scoreboard showing the rating of all players determined by the [TrueSkill Ranking System](http://research.microsoft.com/en-us/projects/trueskill/)
- Users can opt-in or out of receiving a weekly email of their standing in the league.
- All users can view a page displaying recent match results from teams across the league.
- Players can dispute match results from matches they participated in by clicking a dispute button shown next to the match result.
- If granted permission by an admin, they can report game outcomes by entering the teams that played, the outcome, and set any statistics fields related to the match.

### Admin
- Admin have all the functionality defined in the Players section above along with the following points.
- The first person to register for the site becomes an admin.
- Admin have the ability to designate others as admin by viewing their profile page and clicking a button.
- Admin are able to grant permission to report games to any user by viewing their profile page and clicking a button.
- Before anyone can report games however, an admin must define aspects of the game on a league management page such as team size and add any desired team or player statistics to keep track of when reporting a match.
- Admin can edit and delete match results shown on the recent match results page.
- All admin have access to a page showing disputed match results reported by players and can either edit the result or ignore the dispute as they see fit.

### Backend
- I will write a custom django admin command to send weekly report emails that can be run by the Heroku schedueler.
- I initally intend to have a player's TrueSkill rating recalculated immediately upon the server receiving a new match result, however I will test the average response time for this and if it is too slow I will need to seperate this function out into another custom admin command to be ran on a scheduled basis. 

## Sprint 1 Backlog
- New users can register for the site, and receive an email verification to verify their account
- Verified players can view and edit their personal profile page
- All players can view a list of every player on a players page, and also view other players' profiles.
- Players can opt-in or out of receiving a weekly email of their standing in the league.
- The first person to register for the site will become an admin.
- Admin have the ability to designate others as admin by viewing their profile page and clicking a "Make Admin" button.
- Admin will be able to set a name for their league, and upload a picture to use as an icon to represent the game or sport, and designate the size of teams in the league.

## Data Models
I've implemented my data models as Django models in [models.py](models.py)
