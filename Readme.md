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

  Command | Description
  --- | ---
  'forward' | Takes one step forward in currently facing direction
  'rotCW' | Rotates 90 degrees clockwise
  'rotCCW' | Rotates 90 degrees counter-clockwise

(Things are rather simple at the moment!)

To influence these moves, each bot is given particular information each round from the server. All this information is saved in the bot CBot class and can be accessed via attributes. Information available at the moment includes:

  Attribute | Description
  --- | ---
  .playercount | Returns current number of bots still in the round
  .spearcount | Returns the number of spears you currently have. **Not yet implemented!**
  .vision | A list of number values 'seen' by your bot in the direction in is facing. More details below

#### Bot Vision
The .vision attribute will return a list of values depicting everything your bot see's in the direction it is looking. *This list will always begin with your bot itself!* The server keeps track of the map in the following fashion:
  * 0 - Nothing is here
  * 1 - There is a wall here
  * 2 digit number - Bot Identification number, there is a bot here
    * Bots will also have a decimal trailing after them which shows what direction they are facing. .0 is straight up, .1 is to the right, .2 is downwards, and .3 is to the left
  * 2 - Will be a spear once implemented, and will have traveling direction like bots

## Running the Server
The server is run from a command prompt or shell following normal python conventions. Bots to compete are added to the prompt following a -i option. For example, to run a competition between the Randomman.py and Simpleman.py, you'd write:
```
python server.py -i Randomman.py Simpleman.py
```
