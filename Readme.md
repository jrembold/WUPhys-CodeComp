# Stabby Bot!

Things are finally reasonably functional! Much more work will be added and tweaked over the coming days, but for now the core code functions properly and bots can be coded.

## Coding Bots
Bots are written as simple python scripts and should reside in the same folder as server.py. Two example bots are provided for reference. Each bot should always include several things:
  1. Importing the library module
  2. Initialize the bot as the CBot class, giving in a fun name 
  3. For as long as the bot is active:
     * Get the current state of the map from the server
	 * Send a response for what action the bot should take for that round

And that's it! Bot moves are sent as a string, and currently include:
  * 'forward' - To take one step forward
  * 'rotCW' - To rotate clockwise 90 degrees
  * 'rotCCW' - To rotate counterclockwise 90 degrees
(Things are rather simple at the moment!)

To influence these moves, each bot is given particular information each round from the server. All this information is saved in the bot CBot class and can be accessed via attributes. Information available at the moment includes:
  * .playercount - The current number of bots still in the round
  * .spearcount - Not yet utilized, but coming soon!
  * .vision - A list of the number values "seen" by your bot in the direction it is facing. More details below.

### Bot Vision
The .vision attribute will return a list of values depicting everything your bot see's in the direction it is looking. *This list will always begin with your bot itself!* The server keeps track of the map in the following fashion:
  * 0 - Nothing is here
  * 1 - There is a wall here
  * 2 digit number - Bot Identification number, there is a bot here
    * Bots will also have a decimal trailing after them which shows what direction they are facing. .0 is straight up, .1 is to the right, .2 is downwards, and .3 is to the left
  * 2 - Will be a spear once implemented, and will have traveling direction like bots
