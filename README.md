Simulate the game [Werewolves](https://en.wikipedia.org/wiki/The_Werewolves_of_Millers_Hollow) using either a population or an agent based model. 

## About the game

Werewolves is a social deduction game that involves a group of players trying to identify and eliminate werewolves among them.The game is typically set in a village or town where players are assigned secret roles as either villagers or werewolves. The game consists of alternating day and night phases, with specific actions and rules for each. 

### First day

During the first days players get to know their role and wolves get to know eachother. This is followed by the election of a mayor. 

### Night phase

The werewolves choose a villager to eliminate from the game. Wolves will not kill another wolf and also will not choose to not kill.

### Day phase

After group discussions and deliberations the player lynch another player by voting. All players must vote and players cannot vote for themselves. Voting is simultaneous and open. In case of a tie, the mayor's vote tells as 1.5. In case the mayor's vote wasn't involved in the tie, the mayor chooses.

### Special roles

There are many special roles on both sides which are not considered at the moment.

## Models

### Popluation based model

This model considers two populations: civilians and wolves as a number of players. After each night, the number of civilians is reduced by one. After each day a civilian or wolf is removed based on chance. Note that the mayor plays no role in this implementation. 

The population based model cannot be used for any special role. Moreover, it is inaccurate because it does not consider the rule that players cannot vote for themselves. For example, in case of 3 players with 1 wolf and 2 civilians. The population based model would give a 1 in 3 chance of lynching the wolf. However, in reality the wolf will never vote for the wolf and both civilians have a fifty-fifty chance of hitting a wolf. So the chance of lynching a wolf is 1 in 4 instead of 1 in 3.

### Agent based model

In the agent based model each player is represented. TODO: finish this.

## TODO

* Add pipelines to run tests and flake on push
* Add mypy
* Improve ABM implementation
* Visualization
