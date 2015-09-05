## About

This is a server which allows player to play Kabou via a REST API.


## Rules

Kabou is a game which can be played by 2-8 players. It is played with a
french deck with jokers (54 cards: 4x(Ace, 2-10, Jack, Queen, King), 2xJoker).
Each game consists of rounds in which you make points. The objective is to
get as little points as possible. A game of Kabou has arbitrary many rounds. In each round, each player gets an integer amount of points (which might be negative). The less points, the better.

### One round

Each player gets 4 cards (hidden) in front of him. The order may not be
switched. There is a order among players in which they get to play their turns.
Each turn consists of:

* (a) Drawing a card or (b) taking the top most card of the stack or (c) saying "Kabou"
* If you drew a card, you may either (a) play it (put it open on the stack) or
  (b) exchange it with one of the cards in front of you.
  * When you exchange it, you put the exchanged card open on the stack.
  * When you play it some effect happens, depending on the card (see below)
* When the card is put on the stack, the turn of one player ends and the next begins.

In every situation, players may put a card they know (from the ones lying in
front of all players) on the stack, if the value (ace, 2-10, jack,queen king,
joker) is the same. If they put it on the stack from another players cards,
they can give that player one of their cards. If they make a mistake, they have
to draw another card. Each player gets to see what they wanted to put on the
stack. More details in the section "Revealing cards"

When a player thinks he is in a good situation, he can say "Kabou" right before
he does anything in his turn. He skips his turn, the game goes on until he
would get his turn again. Other players may not exchange cards from him, but
besides that the turns are just normal.

### Card effects

* 7, 8: take a look at one of your cards
* 9, 10: take a look at another players cards
* Jack, Queen: Exchange 1 card from another player with 1 of your cards. Don't
  look at any of them.
* heart king: Take a look at one card of another player. Then decide if you
  want to exchange that card with one of your cards.

### Card values

Higher is worse

* Joker: -1
* Black king: 0
* Ace: 1
* 2 - 10: Card value (2 - 10)
* Jack: 11
* Queen: 12
* Red king: 13


### Revealing cards

When a card is placed on the stack, this is the order in which players may
reveal a card:

1. All players may put one of their own cards on the stack.
2. In the order in which the next players rounds are, the players can turn up
   other players cards. If they don't want to do it, they have to say they are
   done.

## API

All POST and PUT requests return the created / edited object in JSON format.

* `/player`:
  * PUT: Create a new player (name, password) - gets identifier
  * POST: Edit a player (name, description, repository)
* `/game`:
  * PUT: Create a new game (password (optinally)) - returns game object with identifier
* `/game/ID`:
  * GET: Give current status (player ids, order of players, number of cards in front of each player, whos turn it is, which round it is, current number of points per player)
  * POST: A move
