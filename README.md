Simulate the game [Werewolves](https://en.wikipedia.org/wiki/The_Werewolves_of_Millers_Hollow) using an agent based model. 

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

## Model

The simulations use an agent based model because a population based model cannot reflect the knowledge each player has. A population based model was part of this project and can still be found in older commits.

TODO: finish this description

## TODO

* Add mypy
* Improve ABM implementation
* Visualization
