import random

pokemon_db = [['Flamepup', 5, 7, 2, 'Fire', 120],
 ['Rockfist', 22, 8, 1, 'Earth', 120],
 ['Iceshade', 30, 7, 3, 'Water', 120],
 ['Windhover', 35, 7, 2, 'Wind', 120],
 ['Aquatail', 8, 8, 2, 'Water', 120],
 ['Grasswhisk', 12, 6, 2, 'Earth', 120],
 ['Electrospark', 15, 9, 5, 'Wind', 120],
 ['Mudslide', 40, 8, 2, 'Earth', 120],
 ['Psychmind', 45, 9, 4, 'Fire', 120],
 ['Ironclad', 50, 10, 2, 'Earth', 120],
 ['Venomlash', 55, 7, 4, 'Water', 120],
 ['Shadowgleam', 60, 8, 5, 'Fire', 120],
 ['Dragonflame', 65, 10, 3, 'Fire', 120],
 ['Fairydust', 70, 6, 4, 'Wind', 120],
 ['Ghostwhisper', 75, 7, 2, 'Fire', 120]]

types = {'Fire': {'strong_against': ['Wind'], 'weak_against': ['Water']},
         'Water': {'strong_against': ['Fire'], 'weak_against': ['Earth']},
         'Earth': {'strong_against': ['Water'], 'weak_against': ['Fire']},
         'Wind': {'strong_against': ['Earth'], 'weak_against': ['Fire']}}

class Pokemon:
    def __init__(self, pokemon_data):
        if not pokemon_data or len(pokemon_data) != 6:
            raise ValueError('Pokemon data is required')
        if not pokemon_data[0]:
            raise ValueError('Name is required')
        if not pokemon_data[1]:
            raise ValueError('Level is required and must be a number')
        if not pokemon_data[2] or not 10 >= pokemon_data[2] >= 1:
            raise ValueError('Strength is required and must be a number between 1 and 10')
        if not pokemon_data[3] or not 5 >= pokemon_data[3] >= 1:
            raise ValueError('Speed is required and must be a number between 1 and 5')
        if not pokemon_data[4]:
            raise ValueError('Type is required')
        if not pokemon_data[5] or not 120 >= pokemon_data[5] >= 1:
            raise ValueError('Life is required and must be a number between 1 and 120')

        self.name = pokemon_data[0]
        self.level = pokemon_data[1]
        self.strength = pokemon_data[2]
        self.speed = pokemon_data[3]
        self.type = pokemon_data[4]
        self.life = pokemon_data[5]
    
    def __str__(self):
        return f'{self.name} (lvl {self.level})'
    
    def stats(self):
        return f'{self.name} (lvl {self.level}) - Strength: {self.strength}, Speed: {self.speed}, Type: {self.type}, Life: {self.life}'

    def attack(self, enemy):
        if not enemy or not isinstance(enemy, Pokemon):
            raise ValueError('Enemy is required and must be a Pokemon')
        if enemy.life <= 0:
            raise ValueError('Enemy is already dead')
        if self.life <= 0:
            raise ValueError('Pokemon is already dead')
        if self.type == enemy.type:
            damage = 1 *(random.randint(1,20) + self.strength)
            enemy.life -= damage
#             `{pokemon 1} attacks {pokemon 2}. deals {x} damage. {Pokemon 2} now has {X} amount of life after the attack.`
            print(f'{self.name} attacks {enemy.name}. deals {damage} damage. {enemy.name} now has {enemy.life} amount of life after the attack.')
        elif enemy.type in types[self.type]['strong_against']:
            damage = 2 * (random.randint(1,20) + self.strength)
            enemy.life -= damage
            print(f'{self.name} attacks {enemy.name}. deals {damage} damage. {enemy.name} now has {enemy.life} amount of life after the attack.')
        elif enemy.type in types[self.type]['weak_against']:
            damage = 0.5 * (random.randint(1,20) + self.strength)
            enemy.life -= damage
            print(f'{self.name} attacks {enemy.name}. deals {damage} damage. {enemy.name} now has {enemy.life} amount of life after the attack.')
        else:
            damage = random.randint(1,20) + self.strength
            enemy.life -= damage
            print(f'{self.name} attacks {enemy.name}. deals {damage} damage. {enemy.name} now has {enemy.life} amount of life after the attack.')
        return

    def isDead(self):
        return self.life <= 0


    

class Player:
    def __init__(self, name, pokemons):
        if not name:
            raise ValueError('Name is required')
        if not pokemons or len(pokemons) < 1:
            raise ValueError('At least one pokemon is required')
        self.name = name
        self.pokemons = pokemons
    
    def __str__(self):
        return f'Player {self.name} with {len(self.pokemons)} pokemons'
    
    def select_pokemon(self):
        healthy_pokemons = [pokemon for pokemon in self.pokemons if pokemon.life > 0]
        if len(healthy_pokemons) == 0:
            return None
        else:
            #`{pokemon name} has joined the fight`
            chosen_pokemons = random.choice(healthy_pokemons)
            print(f'{chosen_pokemons.name} has joined the fight')
            return chosen_pokemons

class Fight:
    def __init__(self, player1, player2):
        if not player1 or not player2 or not isinstance(player1, Player) or not isinstance(player2, Player):
            raise ValueError('Two players are required')
        self.player1 = player1
        self.player2 = player2

    def __choose_first_attacker(self, pokemon1, pokemon2):
        rand = random.randint(1,20)
        pokemon1_speed = pokemon1.speed + rand
        pokemon2_speed = pokemon2.speed + rand
        if pokemon1_speed >= pokemon2_speed:
            return 1
        else:
            return 2
    
    def start(self):
        print(f'{self.player1.name} vs {self.player2.name}')
        while True:
            pokemon1 = self.player1.select_pokemon()
            pokemon2 = self.player2.select_pokemon()
            if pokemon1 is None and pokemon2 is None:
                print('It is a draw!')
                break
            elif pokemon1 is None:
                print(f'{self.player2.name} wins!')
                break
            elif pokemon2 is None:
                print(f'{self.player1.name} wins!')
                break
            else:

                print(f'{pokemon1.name} vs {pokemon2.name}')
                first_attacker = self.__choose_first_attacker(pokemon1, pokemon2)
                first_attack = True
                timer_pokemon1 = 0
                timer_pokemon2 = 0
                while True:
                    if first_attack==True:
                        if first_attacker == 1:
                            pokemon1.attack(pokemon2)
                            if pokemon2.isDead():
                                print(f'{pokemon1} wins!')
                                break
                            first_attack = False
                        else:
                            pokemon2.attack(pokemon1)
                            if pokemon1.isDead():
                                print(f'{pokemon2} wins!')
                                break
                            first_attack = False
                    else:
                        if timer_pokemon1 == pokemon1.speed:
                            pokemon1.attack(pokemon2)
                            if pokemon2.isDead():
                                print(f'{pokemon1} wins!')
                                break
                            timer_pokemon1 = 0
                        if timer_pokemon2 == pokemon2.speed:
                            pokemon2.attack(pokemon1)
                            if pokemon1.isDead():
                                print(f'{pokemon2} wins!')
                                break
                            timer_pokemon2 = 0
                    timer_pokemon1 += 1
                    timer_pokemon2 += 1
    
    
# give player1 first 5 pokemons and player 2 the next 5 
player1 = Player('Player 1', [Pokemon(pokemon) for pokemon in pokemon_db[:5]])
player2 = Player('Player 2', [Pokemon(pokemon) for pokemon in pokemon_db[5:]])
fight = Fight(player1, player2)
fight.start()