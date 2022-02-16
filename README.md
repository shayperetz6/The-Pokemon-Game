
# Ex4 - The Finel One , AKA The Pokemon Game

in this project we were asked to make an algorithem for the pokemon game, and also make a simple GUI.

the pokemon game is simple! you you have agents,nodes,edges and of course pokemons, 
each pokemon have a value and in the end you need to have as much points as you can by catching them(in this case move near them on the edge) in the time given,
also each pokemon is seating on an edge and each agent is seating on node(at the start at least)
the algorithem shood tell the brave agents how to move to max the amount of points. 
## Authors

- [@oa1321](https://www.github.com/oa1321) 213101637
- [@shayperetz6](https://github.com/shayperetz6) 203464870


## The Problem Space
the point of the game as described above is to gather as much points as possible, 
and how to do this is the problem we need to solve.
first we need to handle few things, the first is were each agent need to start
and the second is on what edge each pokemon seats on.
after we solve this two problems we can move to how to move on the graph(the gameboard)
and collect as much points as possibale
## The Algorithmem

so like we used the first two problems is were the pokemons are and what is the starting node,
to solve them we used this two Algorithmems

first, to find eace pokemons edge we can get is x,y cordinets and go through each edge and choose the clossest one 
and this part happens by calc the dist src->pokemon->dst and src->dst and then saving the differnce between the two
after we finished all the edges we need the fined the minimal and this is the edge of the pokemon
finnaly the type of the pokemon will tell us were the pokemons is on the edge(up the edge or down the edge)


second one, we just simple put each agent next to a pokemon 

after this two solved we can move to the path Algorithmem-

we used for this part our graph imlamentsion from EX3 [--more on that in this link--](https://github.com/oa1321/Ex3_oop.git)


the Algorithmem calc the path from our agent src to each node and choose the path
with the most value to "distance" ratio alse the Algorithmem will prefere paths that will
make the agent get furter away from the agents in the game 

the Algorithmem runs each time they get to a new node 

the reasoning for the Algorithmem is simple we want an Algorithmem that will get us as much value as we can
but wont give us a long fixed trip because maybe someone took that pokemon or maybe there is a new and better way
now, we do the social distancing part of the Algorithmem(the part that trys to seprate the agents from each outer) not just because we need them tp spread on the graph so the Algorithmem will work better but also 
sometimes they get stuck in each other(not fun for them or for us) and this is not good because they now go togthear but this part of the Algorithmem will try to solve it

## Classes 
### the classes we used from ex3 (link in the algorithm part)

GraphAlgo implaments GraphAlgoInterface

GraphGui is the class of the GUI appliction , we used tkinter for the gui

Node is class to save node data in 

### fields and methods of each class we created

#### GuiStuff

this class handels all the Gui part of the game (as asked) and also runs the game loop

    WIDTH, HEIGHT = 1080, 720 is the size of the screen 
    radius = the radius for some circles 
    pokemons = the current pokemons
    agents = the current agents
    algo_s: AlgoStuff = a reffrence to the algo class sp we can choose a next node and were to start ....

the init func requres thoose values

    client - the client of the game(a class that was given to us)
    net_graph: DiGraph() - a graph to work on,
    graph_info - the graph info,
    info - the game info

#### AlgoStuff

this one is to handle the algorithms we have

    self.client = the client
    self.my_graph: DiGraph = the graph to work on
    self.game_info = the game info string 
    self.agents_path = the agents curr path - used for algo
    self.agents_prev = the agents prev path - used for algo
## GUI

### About
we used pygame for the GUI 
### How to download 

download the github repostery and folow the how to use instructions.

### How to use 

simpale makes better is was our line f thought to build this GUI 
to use it just check that you have python3 and java and all the libaries installed to your comuter, 
choose the IDE you want or run it from command line, 
to you need to run first the java jar server with a case 0-15 and then just run the python main.py file

if at any point you feal like you want to stop the game just press the red circle in the left up corner 

if you are stuck on doctor oak screen press enter 

you will have the points and moves amount and also the time left shown also in the left up corner

![plot](https://github.com/oa1321/oop_last/blob/2c767d6a66543f99d31d058cd333abf31e03f57f/gui1.png)

## Tests and tests and tests

### the best preformance are !!

case 0 - 

    {"GameServer":{"pokemons":1,"is_logged_in":
    false,"moves":299,"grade":115,"game_level":
    0,"max_user_level":-1,"id":0,"graph":"data/
    A0","agents":1}}

case 1 - 

    {"GameServer":{"pokemons":2,"is_logged_in":
    false,"moves":598,"grade":490,"game_level":
    1,"max_user_level":-1,"id":0,"graph":"data/
    A0","agents":1}}

case 2 -

    {"GameServer":{"pokemons":3,"is_logged_in":
    false,"moves":299,"grade":242,"game_level":
    2,"max_user_level":-1,"id":0,"graph":"data/
    A0","agents":1}}

case 3 - 

    {"GameServer":{"pokemons":4,"is_logged_in":
    false,"moves":587,"grade":629,"game_level":
    3,"max_user_level":-1,"id":0,"graph":"data/
    A0","agents":1}}

case 4 -

    {"GameServer":{"pokemons":5,"is_logged_in":
    false,"moves":299,"grade":188,"game_level":
    4,"max_user_level":-1,"id":0,"graph":"data/
    A1","agents":1}}

case 5 - 

    {"GameServer":{"pokemons":6,"is_logged_in":
    false,"moves":598,"grade":474,"game_level":
    5,"max_user_level":-1,"id":0,"graph":"data/
    A1","agents":1}}

case 6 -

    {"GameServer":{"pokemons":1,"is_logged_in":
    false,"moves":299,"grade":79,"game_level":6
    ,"max_user_level":-1,"id":0,"graph":"data/A
    1","agents":1}}

case 7 - 

    {"GameServer":{"pokemons":2,"is_logged_in":
    false,"moves":598,"grade":300,"game_level":
    7,"max_user_level":-1,"id":0,"graph":"data/
    A1","agents":1}}

case 8 - 

    {"GameServer":{"pokemons":3,"is_logged_in":
    false,"moves":299,"grade":73,"game_level":8
    ,"max_user_level":-1,"id":0,"graph":"data/A
    2","agents":1}}

case 9 =

    {"GameServer":{"pokemons":4,"is_logged_in":
    false,"moves":598,"grade":383,"game_level":
    9,"max_user_level":-1,"id":0,"graph":"data/
    A2","agents":1}}

case 10 - 

    {"GameServer":{"pokemons":5,"is_logged_in":
    false,"moves":299,"grade":159,"game_level":
    10,"max_user_level":-1,"id":0,"graph":"data
    /A2","agents":1}}

case 11 - 

    {"GameServer":{"pokemons":6,"is_logged_in":
    false,"moves":598,"grade":1797,"game_level"
    :11,"max_user_level":-1,"id":0,"graph":"dat
    a/A2","agents":3}}

case 12 - 

    {"GameServer":{"pokemons":1,"is_logged_in":
    false,"moves":299,"grade":40,"game_level":1
    2,"max_user_level":-1,"id":0,"graph":"data/
    A3","agents":1}}

case 13 - 

    {"GameServer":{"pokemons":2,"is_logged_in":
    false,"moves":598,"grade":300,"game_level":
    13,"max_user_level":-1,"id":0,"graph":"data
    /A3","agents":2}}

case 14 - 

    {"GameServer":{"pokemons":3,"is_logged_in":
    false,"moves":299,"grade":236,"game_level":
    14,"max_user_level":-1,"id":0,"graph":"data
    /A3","agents":3}}

case 15 - 

    {"GameServer":{"pokemons":4,"is_logged_in":
    false,"moves":598,"grade":300,"game_level":
    15,"max_user_level":-1,"id":0,"graph":"data
    /A3","agents":1}}



### Digram
![image](https://user-images.githubusercontent.com/73098848/148686122-30ebc207-e29e-4cb9-ae39-578dadcba684.png)







