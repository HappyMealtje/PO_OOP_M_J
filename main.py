import random

class Player:
  level = 1
  xp = 0
  next_level_xp = 500
  hp = 50
  max_hp = 50

  def __init__(self, name):
    self.name = name
    
    self.weapon = Weapon(1)
    self.armor = Armor(1)

    self.inventory = [self.weapon, self.armor]
  
  def attack(self):
    damage = self.level + random.randint(self.weapon.min_damage, self.weapon.max_damage)
    print(self.name, 'attacks with a ', self.weapon.weapon_type, ' for ', damage, ' damage.')
    return damage

  def take_hit(self, damage):
    final_damage = damage - self.armor.defence
    if final_damage > 0:
      self.hp -= final_damage
    
      if self.hp <= 0:
        #je bent dood!
        print('AAAARGH! you died!')
      else:
        print('Ouch! you take ', final_damage, 'damage!')
        print('You have ', self.hp, ' hp left.')

    else:
      print('Your shiny armor protects you, you take 0 damage.')
    

  def heal(self, heal_amount):
    self.hp += heal_amount

    #check of je over het max gaat
    if self.hp > self.max_hp:
      self.hp = self.max_hp

    print('You healed for ', heal_amount, 'hp.')
    print('You currently have ', self.hp, '/', self.max_hp,  'hp.')

  def xp_gain(self, xp_amount):
    self.xp += xp_amount
    print('You have gained ', xp_amount, 'xp!')

    #level up?
    if self.xp >= self.next_level_xp:
      self.level += 1
      self.xp -= self.next_level_xp

      self.next_level_xp = int(self.next_level_xp * 1.25)
      self.max_hp = int(self.max_hp * 1.2)
      self.hp = self.max_hp

      print('YAY! You have reached level ', self.level, '!')

      self.print_stats()

  def equip_item(self, item):

    if item.item_type == 'Weapon':
      self.weapon = item
    elif item.item_type == 'Armor':
      self.armor = item

    #laat even zien hoe de player
    self.print_stats()

  def print_stats(self):
    print()
    print('Player stats:')
    print(' - Name: ', self.name)
    print(' - Level: ', self.level)
    print(' - HP: ', self.hp, '/', self.max_hp)
    print(' - XP: ', self.xp, '/', self.next_level_xp)
    self.weapon.print_stats()
    self.armor.print_stats()
    print()

  def addtoInventory(self, item):
    self.inventory.append(item)

class World:
   def __init__(self):
       places = {
         'Grassfield': {
           'directions' : {
             'left' : 'Shed',
             'right' : 'Pier',
             'up' : 'Townsquare'
           }
         },
         'Shed': {
           'directions' : {
             'right' : 'Grassfield',
             'up' : 'Forest'
           }
         },
         'Forest': {
           'directions' : {
             'right' : 'Townsquare',
             'down' : 'Shed'
           }
         },
         'Pier': {
           'directions' : {
             'left' : 'Grassfield'
           }
         },
         'Townsquare': {
           'directions' : {
             'left' : 'Forest',
             'right' : 'Bakery',
             'up' : 'Townhall',
             'down' : 'Grassfield'
           }
         },
         'Townhall': {
           'directions' : {
             'down' : 'Townsquare'
           }
         },
         'Bakery': {
           'directions' : {
             'left' : 'Townsquare',
             'up' : 'Shop'
           }
         },
         'Shop': {
           'directions' : {
             'down' : 'Bakery'
           }
         }
       }

       self.world = {place_name: Place(place_name, place_data['directions']) for place_name, place_data in places.items()}
       self.current_place = self.world['Grassfield']


class Place:

  def __init__(self, name, directions = None ):
    self.name = name
    self.directions = directions if directions is not None else {}

  def print_stats(self):
    print(world.current_place.name)
  
    if self.directions:
      for direction, place_name in self.directions.items():
        print(f"{direction}: {place_name}")


world = World()

world.current_place = world.current_place


class Item:
  item_type = None

  def __init__(self, item_level):
    self.item_level = item_level

  def print_stats(self):
    print(self.item_type, '- level: ', self.item_level)


class Weapon(Item):

  def __init__(self, item_level):
    Item.__init__(self, item_level)

    self.item_type = 'weapon'

    weapon_list = ['Sword', 'Axe']
    self.weapon_type = random.choice(weapon_list)

    if self.weapon_type == 'Sword':
      self.min_damage = self.item_level * 2
      self.max_damage = self.item_level * 3

    elif self.weapon_type == 'Axe':
      self.min_damage = 1
      self.max_damage = self.item_level * 4

  def print_stats(self):
    Item.print_stats(self)
    print(self.weapon_type, ' damage: ', self.min_damage, ' - ', self.max_damage)


class Armor(Item):

  def __init__(self, item_level):
    Item.__init__(self, item_level)
    self.item_type = 'armor'
    self.defence = self.item_level * 2

  def print_stats(self):
    Item.print_stats(self)
    print('Defence: ', self.defence)
    

class Monster:
  
  hp = 1
  max_hp = 1
  min_damage = 1
  max_damage = 1

  monster_type = None

  xp_value = 1

  def __init__(self, level):
    self.level = level

  def attack(self):
    damage = random.randint(self.min_damage, self.max_damage)
    print(self.monster_type, ' attacks for ', damage, ' damage.')
    return damage

  def take_hit(self, damage):
    self.hp -= damage

    if self.hp > 0:
      #monster leeft nog
      print(self.monster_type, ' has ', self.hp, ' hp left.')
    else:
      # moster is dood
      print(self.monster_type, ' was slain.')

  def print_stats(self):
    print(self.monster_type, ' - level', self.level)
    if self.hp > 0:
      print('HP: ', self.hp, ' / ', self.max_hp)
    else:
      print('*Dead*')


  def befriend(self, player):
    if random.randint(1,10) >= 7:
      print("You befriended a monster!")
      self.xp_value = 20 + self.level * 20 
      player.xp_gain(self.xp_value)
      return True
    elif random.randint(1,10) <= 6:
      print("The monster doesn't like you...")
      player.take_hit( self.attack() )
      print("the monster attacks")
      return False


class Skeleton(Monster):

  def __init__(self, level):
    Monster.__init__(self, level)
    
    self.monster_type = 'Skeleton'

    self.hp = self.max_hp = self.level * 15
    self.min_damage = self.level + 1
    self.max_damage = self.level * 3

    self.xp_value = 100 + self.level * 20


class Troll(Monster):

  def __init__(self, level):
    Monster.__init__(self, level)
    
    self.monster_type = 'Troll'

    self.hp = self.max_hp = self.level * 20
    self.min_damage = 1
    self.max_damage = self.level * 4

    self.xp_value = 100 + self.level * 20

    self.crit_chance = max(30, level * 10)

  def attack(self):
    damage = random.randint(self.min_damage, self.max_damage)

    #cratical hit
    if random.randint(1, 100) <= self.crit_chance:
      print(self.monster_type, ' makes a critical hit!')
      damage *= 2

    print(self.monster_type, ' attacks for ', damage, ' damage.')
    return damage


class Dragon(Monster):
  catchable = True

  def __init__(self, level):
    Monster.__init__(self, level)
  
    self.monster_type = 'Dragon'
  
    self.hp = self.max_hp = self.level * 25
    self.min_damage = self.level + 2
    self.max_damage = self.level * 5
  
    self.xp_value = 100 + self.level * 20

  def befriend(self, player):
    if self.catchable:
        print("You can't befriend a Dragon, but you can try to catch it!")
        return False
    else:
        print()


class Battle:

  def __init__(self, player):
    self.player = player #link naar de player

    self.difficulty = random.randint(1,3)

    self.monster_list = []

    self.xp_value = 0

    self.world = world #link naar de wereld

    monster_types = ['Skeleton', 'Troll', 'Dragon']

    for i in range(self.difficulty):
      monster_choice = random.choice(monster_types)

      if monster_choice == 'Skeleton':
        self.monster_list.append(Skeleton(self.player.level))
      elif monster_choice == 'Troll':
        self.monster_list.append(Troll(self.player.level))
      elif monster_choice == 'Dragon':
        self.monster_list.append(Dragon(self.player.level))
     

      self.xp_value += self.monster_list[i].xp_value

  def battle_stats(self):
    print('You are fighting:')

    for i in range(len(self.monster_list)):
        print('Enemy', i+1)
        self.monster_list[i].print_stats()
    
        print()

    print('-----------------------------')
    print()

  def generate_loot(self):
    #genereert nieuwe items als het gevecht is afgelopen

    loot = False
    if self.difficulty == 1:
      if random.randint(1,100) <= 25: #25%
        loot = True
    elif self.difficulty == 2:
      if random.randint(1,100) <= 40: #40%
        loot = True
    elif self.difficulty == 3:
      if random.randint(1,100) <= 60: #60%
        loot = True

    if loot == True:
      #genereer een item voor de player

      #kies of het een weapon of armor is
      loot_list = ['Weapon', 'Armor']
      loot_type = random.choice(loot_list)

      if loot_type == 'Weapon':
        item = Weapon(random.randint(self.player.level, self.player.level+1))
        print('Yay, the monsters dropped a new weapon!')
      elif loot_type == 'Armor':
        item = Armor(random.randint(self.player.level, self.player.level+1))
        print('Shiny! The monsters dropped an armor!')
      else:
        raise Exception('programming error')

      item.print_stats() #laat het item zien
      print()
      print('Your current stats are:')
      self.player.print_stats()
      print()

      choice = input('Do you want to equip the new item? (Y/N)')
      choice = choice.lower()

      if choice == 'n':
        answer = input('Do you at least want to take it with you? (Y/N)')
        answer = answer.lower()
        if answer == 'y':
          player.addtoInventory(item)
        else:
          print('Now you defenitely leave it behind, to be gone forever!')
      else:
        self.player.equip_item(item)
        print('You equip the new item.')
    else:
      #geen loot
      print('you look real hard, but the monsters dropped no items.')


  def monster_attack(self):
    #monsters vallen de speler aan
    for monster in self.monster_list:
      if monster.hp > 0:
        #leeft het monster nog?
        monster_damage = monster.attack()
        self.player.take_hit(monster_damage)

  def choose_monster(self):
    if len(self.monster_list) > 1:
      max_target = len(self.monster_list)
      target = -1
      while target < 1 or target > max_target:
        target = int(input('Which monster would you like to befriend? (1 - '+ str(max_target) +  ')'))
      target -= 1
    else:
      #er is maar 1 monster
      target = 0
    return self.monster_list[target]
    
  def catch_dragon(self):
        # speler wil een draak vangen
        for monster in self.monster_list:
            if isinstance(monster, Dragon) and monster.hp > 0:
                # check of het monster een draak is en of het leeft
                catch_chance = random.randint(1, 100)
                if catch_chance >= 85:
                    print("You successfully caught the Dragon!")
                    self.player.xp_gain(monster.xp_value)
                    self.monster_list.remove(monster)
                    return True
                else:
                    print("You failed to catch the Dragon.")
                    return False
        print("There are no Dragons to catch.")
        return False
    
  def player_attack(self):
    #de player valt de monsters aan

    #zijn er meerdere monsters
    monster = self.choose_monster()
    
    #damage aan de monster geven
    player_damage = self.player.attack()
    if monster.hp > 0:
      monster.take_hit(player_damage)
    else:
      print('You hit a dead monster. it is still dead...')

  def player_heal(self):
    #speler probeert een healing spel te doen
    if random.randint(1,100) <= 40:
      heal_amount = random.randint(self.player.max_hp// 4, self.player.max_hp // 3)
      self.player.heal(heal_amount)
    else:
      print('You tried to heal yourself, but failed...')

  def player_run(self):
    #de speler probeert te vluchten
    if random.randint(1,100) <= 25:
      print('You ran away as fast as you could, and lost the fight.')
      return True
    else:
      print('You tried to run away, but the monster will not let you...')
      return False

  def player_quit(self):
    print('You give up.')
    self.player.hp = 0

  def walk(self, direction):
     if direction in self.current_place.directions:
       self.current_place = self.current_place.directions[direction]
       print('You walk to the ' + self.current_place)
     else:
       print('You cannot go there')

  def equip(self):
    print('So you want to equip something from your inventory?')
    print('Then this is the right address.')
    print('You have these items')
    for item in player.inventory:
      print(item)

    choice_item = int(input('Which one? (1, 2, 3 ...'))
    if choice_item > len(player.inventory):
      item = player.inventory[choice_item - 1] #om de juiste plek in de lijst te krijgen
      self.player.equip(item)
      player.inventory.remove(item)
  
  
  def fight_battle(self):
    print()
    print('You encounter some monsters')

    #de loop die gevechtsrondes organiseert
    while True:

      print()
      try:
        print('You are at the ' + world.current_place.name)
      except:
        print('You are at the ' + world.current_place)
      print()
      for i in world.current_place.directions:
        print(i + ' : ' + world.current_place.directions[i])
      print()
      print('#### BATTLE ROUND ####')
      self.battle_stats()
        
      player_action = ''
      
      while player_action not in [ 'S', 'F', 'H', 'R', "B", 'C', 'Q', 'W', 'E' ]:
        player_action = input('What will you do? (S)ats, (F)ight, (H)eal, (R)un,(B)efriend, (C)atch, (Q)uit, (W)alk direction, (E)quip').upper()
        player_action = player_action.split(' ', 2)

      if player_action[0] == 'S':
        self.player.print_stats()
        input('Press enter to continue to fight')
      
      elif player_action[0] == 'F':
        #speler wil aanvallen
        self.player_attack()

        monsters_alive = 0
        for monster in self.monster_list:
          if monster.hp > 0:
            monsters_alive += 1

        #zijn er nog monsters over?
        if monsters_alive > 0:
          self.monster_attack()
        else:
          #alle monsters zijn dood. hoera
          print('-------------------------')
          print('YOU WON THE BATTLE!!')
          print('-------------------------')

          #geeft de speler experience
          self.player.xp_gain(self.xp_value)

          #kijk of er loot gegenereerd wordt
          self.generate_loot()

          #onderbreek het gevecht
          break

      elif player_action[0] == 'H':
        self.player_heal()
        print()
        self.monster_attack()

      elif player_action[0] == 'R':
        #player probeert weg te rennen
        if self.player_run() == True:
          #het is gelukt
          break #het gevecht is afgelopen

        else:
          self.monster_attack()

      elif player_action[0] == "B":
        #speler wil een monster bevrienden
        monster = self.choose_monster()
        if monster.befriend(player) == True:
          monsters_alive = 0
          self.monster_list.remove(monster)
          for monster in self.monster_list:
            if monster.hp > 0:
              monsters_alive += 1

          #zijn er nog monsters over?
          if monsters_alive > 0:
            self.monster_attack()
          else:
            #alle monsters zijn dood. hoera
            print('-------------------------')
            print('YOU WON THE BATTLE!!')
            print('-------------------------')
            break
        else:
          print('You could not befriend the monster.')

      elif player_action[0] == 'C':
      # speler wil een draak vangen
        if not self.catch_dragon():
          # Batlle gaat door als de draak niet gevangen is
          self.monster_attack()

      elif player_action[0] == 'Q': 
        #speler geeft het op
        self.player_quit()
        break #gevecht is voorbij

      elif player_action[0] == 'W':
        #je wilt naar een andere plek lopen
        self.walk(player_action[1])
        print('a')
        try:
          print('You are at the ' + world.current_place.name)
        except:
          print('You are at the ' + world.current_place)

      elif player_action[0] == 'E':
        self.equip()
      
      #is de player dood?
      if self.player.hp <= 0:
        print('YOU HAVE DIED!!')

        break #gevecht is voorbij

  




player_name = input('What is your name, noble hero?')

player = Player(player_name)

print()
print('Good luck noble', player_name, '. Everyone is counting on you!')
print("Ready for the fight?")

input('Press enter to enter the dungeon.')

battle_count = 0 #tel de gevechten

while player.hp > 0:
  print()
  print('----')
  print()
  battle_count += 1
  print('Battle ', battle_count)

  #maak een nieuw gevecht:
  battle = Battle(player)

  #start het gevecht:
  battle.fight_battle()
          
      
#spel voorbij
print()
print('You have fought ', battle_count, ' battles.')
print('Your final stats are:')
player.print_stats()
print('Thanks for playing!')


