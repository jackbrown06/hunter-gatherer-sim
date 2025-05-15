import random

class SimpleEcosystem:
    def __init__(self):
        # Initial population counts
        self.humans = 10
        self.plants = 100
        self.animals = 50
        
        # Growth and consumption rates (base rates)
        self.plant_growth_rate = 0.2     
        self.animal_reproduction_rate = 0.1
        self.human_reproduction_rate = 0.06
        
        # Consumption needs
        self.human_plant_consumption = 0.35
        self.human_animal_consumption = 0.06
        self.animal_plant_consumption = 0.08
        
        # Human adaptation 
        self.food_storage = 10  # Start with some food storage
        self.max_food_storage = 50  # Increased from 30
        self.farming_efficiency = 1.0
        self.farming_level = 0  # Will increase over time
        self.hunting_skill = 1.0  # Hunting skill improves over time
        
        # Conservation capabilities
        self.animal_conservation_level = 0  # Animal husbandry/protection knowledge
        self.plant_conservation_level = 0   # Plant cultivation/protection knowledge
        self.conservation_active = False    # Tracks if conservation efforts are ongoing
        
        # Seasonal factors
        self.seasons = ["Spring", "Summer", "Fall", "Winter"]
        self.current_season = 0  # Start in spring
        self.days_in_season = 30  # Shortened for more dynamic changes
        self.current_day_in_season = 0
        
        # Season modifiers for plant growth
        self.season_plant_modifiers = {
            "Spring": 2.5,  # Explosive growth
            "Summer": 1.5,  # Good growth
            "Fall": 0.6,    # Significant slowdown
            "Winter": 0.25  # SLIGHTLY IMPROVED winter growth
        }
        
        # Season modifiers for animal reproduction
        self.season_animal_modifiers = {
            "Spring": 2.0,  # Many births
            "Summer": 1.3,  # Good breeding
            "Fall": 0.5,    # Much less breeding
            "Winter": 0.15  # SLIGHTLY IMPROVED winter reproduction
        }
        
        # Rainfall system
        self.rainfall = 50  # 0-100 scale
        self.drought_threshold = 30
        self.flood_threshold = 80
        
        # Days passed
        self.days = 0
        
        # Track history for reporting
        self.history = {
            'humans': [],
            'animals': [],
            'plants': [],
            'rainfall': [],
            'food_storage': []
        }
        
        # Plant reserves - plants that are always protected
        self.plant_reserves = 20  # Minimum number of plants that will always survive
        
        # Animal reserves - protected breeding stock
        self.animal_reserves = 0  # Starts at 0, will increase with conservation efforts
        
        # Trading system
        self.trading_available = True
        self.trading_cooldown = 0
        
        # Knowledge accumulation
        self.survival_knowledge = 0
        
        # Tool development
        self.tools_quality = 1.0
        
        # God Mode - active events
        self.active_events = {
            'plague': 0,            # Duration of active plague (days)
            'drought': 0,           # Duration of active drought (days)
            'blessing': 0,          # Duration of divine blessing (days)
            'animal_disease': 0,    # Duration of animal disease (days)
            'plant_blight': 0       # Duration of plant disease (days)
        }
        
        # Migration tracking
        self.total_migrations = 0
        self.sister_settlements = 0
    
    def update_season(self):
        self.current_day_in_season += 1
        
        if self.current_day_in_season >= self.days_in_season:
            self.current_season = (self.current_season + 1) % 4
            self.current_day_in_season = 0
            print(f"\n=== SEASON CHANGED TO {self.seasons[self.current_season].upper()} ===")
            
            # Seed dispersal during season change
            if self.plants < 30:
                new_seeds = random.randint(5, 15)
                self.plants += new_seeds
                print(f"NATURE EVENT: {new_seeds} new plants sprouted from dormant seeds!")
            
            # Major migration at season changes
            if random.random() < 0.3:
                change = random.randint(-10, 20)
                old_animals = self.animals
                self.animals = max(10, min(200, self.animals + change))
                print(f"MIGRATION EVENT: Animal population changed from {old_animals} to {self.animals}")
            
            # Winter preparation
            if self.seasons[self.current_season] == "Fall" and self.humans >= 5:
                # Humans prepare for winter during fall
                if random.random() < 0.8:  # 80% chance
                    extra_storage = random.randint(5, 10)
                    self.food_storage += extra_storage
                    self.food_storage = min(self.food_storage, self.max_food_storage)
                    print(f"PREPARATION: Humans gathered an extra {extra_storage} food for winter storage!")
            
            # Human farming knowledge increases
            if self.days > 60 and random.random() < 0.2:
                self.farming_level += 1
                self.farming_efficiency = 1.0 + (self.farming_level * 0.15)
                print(f"ADVANCEMENT: Humans improved their farming methods! (Level {self.farming_level}, Efficiency {self.farming_efficiency:.1f}x)")
            
            # Tool improvement
            if self.days > 30 and random.random() < 0.15:
                self.tools_quality += 0.1
                print(f"TECHNOLOGY: Humans improved their tools! (Quality: {self.tools_quality:.1f}x)")
            
            # Knowledge accumulation is more significant at season changes
            self.survival_knowledge += 0.05
            
            # Conservation knowledge increases
            if self.days > 45 and random.random() < 0.25:
                if random.random() < 0.5:
                    self.animal_conservation_level += 1
                    print(f"CONSERVATION: Humans improved their animal husbandry skills! (Level {self.animal_conservation_level})")
                else:
                    self.plant_conservation_level += 1
                    print(f"CONSERVATION: Humans improved their plant cultivation skills! (Level {self.plant_conservation_level})")
            
            # Expand storage capacity with knowledge
            if self.days > 120 and random.random() < 0.3:
                storage_increase = random.randint(5, 10)
                old_capacity = self.max_food_storage
                self.max_food_storage += storage_increase
                print(f"ADVANCEMENT: Humans increased food storage capacity from {old_capacity} to {self.max_food_storage}!")
    
    def update_rainfall(self):
        # Skip natural rainfall update if there's a divine drought active
        if self.active_events['drought'] > 0:
            # Divine drought overrides natural weather
            old_rainfall = self.rainfall
            self.rainfall = max(0, self.rainfall - random.randint(3, 8))
            return
            
        # Dynamic rainfall model
        season_rainfall_base = {
            "Spring": 65,  # Wetter
            "Summer": 40,  # Dry
            "Fall": 60,    # Wet
            "Winter": 30   # Drier
        }
        
        # Target rainfall based on season with high variability
        target = season_rainfall_base[self.seasons[self.current_season]]
        variance = 25
        
        # Move toward seasonal target with randomness
        if self.rainfall < target:
            self.rainfall += random.randint(0, 15)
        else:
            self.rainfall -= random.randint(0, 15)
            
        # Add random fluctuation
        self.rainfall += random.randint(-variance, variance)
        self.rainfall = max(0, min(100, self.rainfall))
        
        # Extreme events - only if no god-triggered events are active
        if not any(duration > 0 for event, duration in self.active_events.items()):
            if random.random() < 0.08:
                event_type = random.choice(["drought", "flood", "ideal"])
                
                if event_type == "drought":
                    self.rainfall = max(0, self.rainfall - 40)
                    print("EXTREME EVENT: A severe drought has struck the region!")
                elif event_type == "flood":
                    self.rainfall = min(100, self.rainfall + 40)
                    print("EXTREME EVENT: Heavy rains have flooded the region!")
                else:
                    self.rainfall = 60  # Perfect conditions
                    print("WEATHER EVENT: Perfect growing conditions have emerged!")
    
    def get_plant_growth_modifier(self):
        # Combine season and rainfall effects
        season_mod = self.season_plant_modifiers[self.seasons[self.current_season]]
        
        # Rainfall effect
        if self.rainfall < self.drought_threshold:
            # Drought conditions - severe impact
            rainfall_mod = 0.3 + (self.rainfall / self.drought_threshold * 0.5)
        elif self.rainfall > self.flood_threshold:
            # Flood conditions
            flood_severity = (self.rainfall - self.flood_threshold) / (100 - self.flood_threshold)
            rainfall_mod = 1.3 - (flood_severity * 0.8)
        else:
            # Ideal conditions
            optimal = 60  # Best rainfall amount
            deviation = abs(self.rainfall - optimal) / 30  # How far from optimal
            rainfall_mod = 1.2 - (deviation * 0.5)
            
        # Apply divine blessing if active
        if self.active_events['blessing'] > 0:
            return season_mod * rainfall_mod * 1.5  # 50% boost to plant growth
            
        # Apply plant blight if active
        if self.active_events['plant_blight'] > 0:
            return season_mod * rainfall_mod * 0.4  # 60% reduction to plant growth
            
        return season_mod * rainfall_mod
    
    def attempt_trading(self):
        # Trading with neighboring groups for emergency food
        if not self.trading_available or self.trading_cooldown > 0:
            if self.trading_cooldown > 0:
                self.trading_cooldown -= 1
            return 0
        
        # Trading chance increases with humans' survival knowledge
        base_trade_chance = 0.4 + (self.survival_knowledge * 0.1)
        
        # Only trade if humans have sufficient population
        if self.humans >= 3:  # Reduced from 5
            # Trading opportunities vary by season
            trade_chance = base_trade_chance
            if self.seasons[self.current_season] == "Winter":
                trade_chance = base_trade_chance * 0.7  # Harder in winter but still possible
            
            if random.random() < trade_chance:
                # More food from trading as humans gain knowledge
                food_received = random.randint(5, 10 + int(self.survival_knowledge * 5))
                self.food_storage += food_received
                # Don't exceed max storage
                self.food_storage = min(self.food_storage, self.max_food_storage)
                self.trading_cooldown = random.randint(5, 15)  # Reduced cooldown
                print(f"TRADING: Humans traded with neighboring groups for {food_received} units of food!")
                return food_received
        
        return 0
    
    # Animal conservation method
    def conserve_animals(self):
        if self.animals < 20 and self.humans >= 3:  # Only try to conserve when population is low and enough humans
            # Effectiveness depends on conservation level and tools
            conservation_power = 1.0 + (self.animal_conservation_level * 0.2) + ((self.tools_quality - 1.0) * 0.3)
            
            # Animal conservation is more effective in spring and summer
            if self.seasons[self.current_season] in ["Spring", "Summer"]:
                conservation_power *= 1.3
            
            # Determine conservation boost based on knowledge and humans committed
            humans_committed = min(int(self.humans * 0.3), max(2, int(self.humans / 5)))
            conservation_boost = int(humans_committed * conservation_power)
            
            # More effective with higher knowledge
            success_chance = 0.3 + (self.animal_conservation_level * 0.1)
            
            if random.random() < success_chance:
                # Animal population boost from conservation efforts
                new_animals = max(1, conservation_boost)
                self.animals += new_animals
                
                # Updates reserves based on conservation level
                self.animal_reserves = min(15, max(self.animal_reserves, int(3 + self.animal_conservation_level)))
                
                print(f"CONSERVATION: Humans successfully protected and raised {new_animals} animals!")
                return True
        
        return False
    
    # Plant conservation method
    def conserve_plants(self):
        if self.plants < 40 and self.humans >= 2:  # Only try to conserve when population is low and enough humans
            # Effectiveness depends on conservation level, farming skills and tools
            conservation_power = 1.0 + (self.plant_conservation_level * 0.25) + (self.farming_level * 0.15) + ((self.tools_quality - 1.0) * 0.2)
            
            # Plant conservation is more effective in spring and fall (planting seasons)
            if self.seasons[self.current_season] in ["Spring", "Fall"]:
                conservation_power *= 1.4
            
            # Determine conservation boost based on knowledge and humans committed
            humans_committed = min(int(self.humans * 0.25), max(1, int(self.humans / 6)))
            conservation_boost = int(humans_committed * conservation_power * 2)  # Plants grow more easily
            
            # More effective with higher knowledge
            success_chance = 0.4 + (self.plant_conservation_level * 0.1)
            
            if random.random() < success_chance:
                # Plant population boost from conservation efforts
                new_plants = max(3, conservation_boost)
                self.plants += new_plants
                
                # Updates reserves based on conservation level
                self.plant_reserves = max(self.plant_reserves, int(20 + self.plant_conservation_level * 2))
                
                print(f"CONSERVATION: Humans successfully planted and protected {new_plants} plants!")
                return True
        
        return False
    
    # Process active god mode events
    def process_active_events(self):
        # Process and reduce duration of all active events
        for event_type, duration in list(self.active_events.items()):
            if duration > 0:
                # Event is active, apply its effects
                if event_type == 'plague':
                    # Human plague reduces population
                    deaths = max(1, int(self.humans * random.uniform(0.02, 0.08)))
                    self.humans = max(0, self.humans - deaths)
                    if deaths > 0:
                        print(f"DIVINE PLAGUE: {deaths} humans died from the plague!")
                
                elif event_type == 'animal_disease':
                    # Animal disease reduces population
                    lost_animals = max(1, int(self.animals * random.uniform(0.05, 0.12)))
                    self.animals = max(0, self.animals - lost_animals)
                    if lost_animals > 0:
                        print(f"DIVINE ANIMAL DISEASE: {lost_animals} animals perished!")
                
                # Reduce the event's remaining duration
                self.active_events[event_type] -= 1
                
                # Announce when an event ends
                if self.active_events[event_type] == 0:
                    event_names = {
                        'plague': 'plague',
                        'drought': 'drought',
                        'blessing': 'divine blessing',
                        'animal_disease': 'animal disease',
                        'plant_blight': 'plant blight'
                    }
                    print(f"DIVINE EVENT ENDED: The {event_names[event_type]} has subsided.")
    
    # Handle migration when human population approaches capacity
    def trigger_migration(self):
        # Only trigger migration if we're near capacity
        if self.humans > 85:  # Approaching the cap of 100
            # Calculate how many will migrate
            migration_percentage = (self.humans - 85) / 15  # Scales from 0 to 1 as population rises from 85 to 100
            migration_chance = 0.5 + (migration_percentage * 0.5)  # Chance increases as population grows
            
            if random.random() < migration_chance:
                # Determine migration size - larger migrations as population approaches cap
                base_migrants = int(self.humans * 0.03)  # Base rate of 3%
                extra_migrants = int((self.humans - 85) * 0.15)  # Additional 15% of population over threshold
                migrants = max(1, base_migrants + extra_migrants)
                
                # Cap to keep a minimum of 85 humans in the tribe
                migrants = min(migrants, self.humans - 85)
                
                if migrants > 0:
                    self.humans -= migrants
                    self.total_migrations += migrants
                    
                    # Update count of sister settlements when a significant group leaves
                    if migrants >= 5:
                        self.sister_settlements += 1
                    
                    # Different messages based on migration size
                    if migrants == 1:
                        print(f"MIGRATION: 1 human has left to establish a new settlement elsewhere.")
                    elif migrants <= 3:
                        print(f"MIGRATION: A small family of {migrants} humans has departed to find new territory.")
                    elif migrants <= 8:
                        print(f"MIGRATION: A group of {migrants} humans has migrated to establish a new settlement.")
                    else:
                        print(f"MAJOR MIGRATION: A large band of {migrants} humans has departed to establish a new colony!")
                        
                    # Chance for knowledge sharing between settlements
                    if random.random() < 0.3 and self.days > 60:
                        knowledge_gain = random.uniform(0.05, 0.2)
                        self.survival_knowledge += knowledge_gain
                        print(f"CULTURAL EXCHANGE: The new settlement maintains contact, increasing knowledge by {knowledge_gain:.2f}!")
                    
                    return migrants
            
            # If no migration happened but we're at capacity, show crowding message
            elif self.humans >= 95:
                print("CROWDING: The settlement is reaching its sustainable capacity - migration may occur soon.")
        
        return 0
    
    # Simulate interactions with sister settlements
    def sister_settlement_interaction(self):
        # Only happens if we have sister settlements
        if self.sister_settlements == 0:
            return
        
        # Interaction chance based on number of sister settlements
        interaction_chance = min(0.15, 0.02 * self.sister_settlements)
        
        # More likely during good weather seasons
        if self.seasons[self.current_season] in ["Spring", "Summer"]:
            interaction_chance *= 1.5
        
        # Less likely during winter
        if self.seasons[self.current_season] == "Winter":
            interaction_chance *= 0.3
        
        if random.random() < interaction_chance:
            interaction_type = random.choices(
                ["trade", "knowledge", "population_return", "food_gift", "hunting_party"],
                weights=[0.4, 0.3, 0.15, 0.1, 0.05],
                k=1
            )[0]
            
            if interaction_type == "trade":
                # Trading goods with sister settlements
                trade_amount = random.randint(2, 6)
                self.food_storage = min(self.max_food_storage, self.food_storage + trade_amount)
                print(f"SETTLEMENT NETWORK: A trading party from a sister settlement brought {trade_amount} units of food!")
                
            elif interaction_type == "knowledge":
                # Knowledge exchange
                knowledge_gain = random.uniform(0.1, 0.3)
                self.survival_knowledge += knowledge_gain
                
                # Chance to gain specialized knowledge
                if random.random() < 0.4:
                    if random.random() < 0.5:
                        self.farming_level += 1
                        self.farming_efficiency = 1.0 + (self.farming_level * 0.15)
                        print(f"CULTURAL EXCHANGE: Visitors from sister settlement shared advanced farming techniques! (Level {self.farming_level})")
                    else:
                        self.tools_quality += 0.1
                        print(f"CULTURAL EXCHANGE: Visitors from sister settlement shared improved tool-making methods! (Quality: {self.tools_quality:.1f}x)")
                else:
                    print(f"CULTURAL EXCHANGE: Contact with sister settlements increased knowledge by {knowledge_gain:.2f}!")
                    
            elif interaction_type == "population_return":
                # Some people return from sister settlements
                returnees = random.randint(1, 3)
                free_capacity = 100 - self.humans
                actual_returnees = min(returnees, free_capacity)
                
                if actual_returnees > 0:
                    self.humans += actual_returnees
                    print(f"POPULATION FLOW: {actual_returnees} humans have returned from sister settlements!")
                    
            elif interaction_type == "food_gift":
                # Emergency food aid during hard times
                if self.food_storage < 10 and (self.plants < 50 or self.animals < 20):
                    aid_amount = random.randint(5, 12)
                    self.food_storage += aid_amount
                    self.food_storage = min(self.max_food_storage, self.food_storage)
                    print(f"COMMUNITY SUPPORT: Sister settlements sent {aid_amount} units of emergency food aid!")
                    
            elif interaction_type == "hunting_party":
                # Joint hunting party increases animal catch
                if self.animals > 30:  # Only if enough animals
                    hunting_bonus = random.randint(2, 5)
                    self.food_storage += hunting_bonus
                    self.food_storage = min(self.max_food_storage, self.food_storage)
                    print(f"JOINT VENTURE: A combined hunting party with sister settlement hunters brought in {hunting_bonus} extra food!")
    
    def update(self):
        # First, process any active god mode events
        self.process_active_events()
        
        # Update season and weather
        self.update_season()
        self.update_rainfall()
        
        # Get environmental modifiers
        plant_growth_modifier = self.get_plant_growth_modifier()
        animal_modifier = self.season_animal_modifiers[self.seasons[self.current_season]]
        
        # Check if conservation is needed
        conservation_active = False
        
        # Try animal conservation if animals are endangered
        if self.animals < 20:
            if self.conserve_animals():
                conservation_active = True
        
        # Try plant conservation if plants are endangered
        if self.plants < 40:
            if self.conserve_plants():
                conservation_active = True
        
        self.conservation_active = conservation_active
        
        # Plants grow based on season and rainfall
        effective_growth_rate = self.plant_growth_rate * plant_growth_modifier
        
        # Calculate available plants (excluding reserves)
        available_plants = max(0, self.plants - self.plant_reserves)
        
        # Growth happens on all plants, including reserves
        new_plants = int(self.plants * effective_growth_rate)
        
        # Animals consume plants and reproduce
        available_animals = max(0, self.animals - self.animal_reserves)  # Respect animal reserves
        plants_consumed_by_animals = min(int(self.animals * self.animal_plant_consumption), available_plants)
        
        # Animals adapt - if food is scarce, they eat less
        if available_plants < self.animals * self.animal_plant_consumption:
            # Animals eat less when plants are scarce
            conservation_factor = available_plants / (self.animals * self.animal_plant_consumption)
            plants_consumed_by_animals = int(plants_consumed_by_animals * (0.7 + 0.3 * conservation_factor))
            
            if plants_consumed_by_animals > 0 and self.animals > 10:
                # Some animals migrate away when food is scarce
                migration_loss = random.randint(1, max(1, int(self.animals * 0.1)))
                self.animals -= migration_loss
                print(f"ADAPTATION: {migration_loss} animals migrated away due to food scarcity")
        
        self.plants = self.plants - plants_consumed_by_animals + new_plants
        
        # IMPROVED HUMAN ADAPTATION: Farming with tools and knowledge
        farming_boost = 1.0
        if self.days > 60:  # Reduced from 90
            farming_boost = self.farming_efficiency * (1.0 + (self.survival_knowledge * 0.1))
            
            # Tools help with farming
            farming_boost *= self.tools_quality
            
            if self.seasons[self.current_season] == "Spring" or self.seasons[self.current_season] == "Summer":
                farming_boost *= 1.2  # Better farming in growing season
            
            # Even in winter, some minimal farming/gathering is possible
            if self.seasons[self.current_season] == "Winter" and self.farming_level >= 2:
                farming_boost = max(0.5, farming_boost * 0.4)  # Preserve some farming ability
        
        # Humans adapt to scarcity
        if available_plants < 30:
            human_plant_consumption_adjusted = self.human_plant_consumption * 0.7
            print("ADAPTATION: Humans are conserving plant resources")
        else:
            human_plant_consumption_adjusted = self.human_plant_consumption
            
        # Animals reproduce based on available plants, season, and current population
        food_ratio_for_animals = min(1.0, plants_consumed_by_animals / max(1, int(self.animals * self.animal_plant_consumption)))
        effective_reproduction_rate = self.animal_reproduction_rate * animal_modifier
        
        # Animal breeding gets boost when conservation is active
        if self.animals < 30 and self.animal_conservation_level > 0:
            conservation_breeding_boost = 1.0 + (self.animal_conservation_level * 0.15)
            effective_reproduction_rate *= conservation_breeding_boost
            food_ratio_for_animals = max(food_ratio_for_animals, 0.5)  # Humans help feed breeding stock
            print(f"CONSERVATION: Humans are assisting animal breeding (Boost: {conservation_breeding_boost:.1f}x)")
        
        # Animal disease reduces reproduction
        if self.active_events['animal_disease'] > 0:
            effective_reproduction_rate *= 0.3  # 70% reduction in reproduction
        
        new_animals = int(self.animals * effective_reproduction_rate * food_ratio_for_animals)
            
        # Humans hunt animals and gather plants
        plants_gathered = min(int(self.humans * human_plant_consumption_adjusted * farming_boost), available_plants)
        
        # Adjust hunting based on animal conservation needs
        hunt_efficiency = min(1.0, self.animals / 30.0) * self.tools_quality * (1.0 + (self.survival_knowledge * 0.1))
        
        # Reduce hunting when animals are endangered
        if self.animals < 25 and self.animal_conservation_level > 0:
            hunt_reduction = 0.5 - (self.animal_conservation_level * 0.08)  # More reduction with higher conservation knowledge
            hunt_efficiency *= max(0.1, hunt_reduction)
            print(f"CONSERVATION: Humans are limiting hunting to protect endangered animals")
        
        # Hunting varies by season but improved with tools and knowledge
        if self.seasons[self.current_season] == "Winter":
            hunt_efficiency *= 0.6  # Improved from 0.5
        elif self.seasons[self.current_season] == "Fall":
            hunt_efficiency *= 1.3  # Fall is hunting season
        
        animals_hunted = min(int(self.humans * self.human_animal_consumption * hunt_efficiency), available_animals)
        
        self.plants -= plants_gathered
        self.animals = self.animals - animals_hunted + new_animals
        
        # Ensure animal reserves are maintained
        if self.animals < self.animal_reserves and self.animal_reserves > 0:
            # Can't maintain full reserves, but save what we can
            self.animal_reserves = self.animals
            print(f"CONSERVATION: Animal reserves reduced to {self.animal_reserves} due to population decline")
        
        # Dormant seeds - if plants get too low, some emergency growth happens
        if self.plants < 20 and random.random() < 0.3:
            emergency_growth = random.randint(3, 10)
            self.plants += emergency_growth
            print(f"RESILIENCE: {emergency_growth} new plants emerged from dormant seeds!")
        
        # Ensure plants never go completely extinct
        if self.plants < self.plant_reserves:
            self.plants = self.plant_reserves
            print("RESILIENCE: Plant reserves are ensuring survival of the species")
        
        # IMPROVED FOOD STORAGE SYSTEM
        # In seasons of plenty, store extra food with improved efficiency
        storage_efficiency = 1.0 + (self.survival_knowledge * 0.2)
        
        if self.seasons[self.current_season] in ["Summer", "Fall"]:
            if plants_gathered > self.humans * human_plant_consumption_adjusted * 0.6:  # Easier threshold
                storage_amount = int((plants_gathered - self.humans * human_plant_consumption_adjusted * 0.6) * 0.6 * storage_efficiency)
                if storage_amount > 0:
                    self.food_storage = min(self.max_food_storage, self.food_storage + storage_amount)
                    print(f"ADAPTATION: Humans stored {storage_amount} units of food! (Storage: {self.food_storage}/{self.max_food_storage})")
        
        # Knowledge accumulation - humans learn survival skills over time
        self.survival_knowledge += 0.002  # Small daily increase
        
        # Calculate food satisfaction including stored food
        food_from_storage = 0
        if self.food_storage > 0:
            # Use stored food when needed, more in winter
            storage_need_factor = 0.3  # Base factor
            if self.seasons[self.current_season] == "Winter":
                storage_need_factor = 0.7  # Higher in winter
            
            needed_food = max(0, self.humans * human_plant_consumption_adjusted * storage_need_factor - plants_gathered)
            food_from_storage = min(needed_food, self.food_storage)
            self.food_storage -= food_from_storage
            if food_from_storage > 0:
                print(f"ADAPTATION: Humans used {food_from_storage} units of stored food! (Remaining: {self.food_storage})")
        
        # Trading system for emergency food - more aggressive trading
        traded_food = 0
        if (plants_gathered + food_from_storage) < (self.humans * human_plant_consumption_adjusted * 0.5):
            # Emergency trading when food is scarce
            traded_food = self.attempt_trading()
        
        # Human population changes based on available food
        total_plant_food = plants_gathered + food_from_storage + traded_food
        food_satisfaction = (total_plant_food / (self.humans * human_plant_consumption_adjusted) * 0.6 + 
                           animals_hunted / max(1, self.humans * self.human_animal_consumption) * 0.4)
        
        # Conservation efforts require human energy
        if conservation_active and self.conservation_active:
            food_satisfaction *= 0.95  # Small penalty for conservation effort
        
        # Winter is less harsh with knowledge and tools
        winter_penalty = 0.7  # Base penalty
        if self.seasons[self.current_season] == "Winter":
            # Knowledge and tools help with winter survival
            winter_adaptation = 0.1 + (self.survival_knowledge * 0.05) + ((self.tools_quality - 1.0) * 0.1)
            winter_penalty = min(0.9, 0.7 + winter_adaptation)  # Can improve up to 0.9
            food_satisfaction *= winter_penalty
            print(f"ADAPTATION: Winter survival efficiency is {winter_penalty:.2f} due to knowledge and tools")
        
        # Emergency measures when food is critically scarce
        if food_satisfaction < 0.3 and self.humans > 5:
            # Desperate measures - hunting or gathering surge
            if random.random() < 0.4:
                emergency_food = random.randint(1, 5)
                food_satisfaction += emergency_food / (self.humans * human_plant_consumption_adjusted) * 0.2
                print(f"EMERGENCY: Humans found {emergency_food} extra units of emergency food!")
        
        # Apply plague effects to food satisfaction if active
        if self.active_events['plague'] > 0:
            food_satisfaction *= 0.7  # Reduced productivity due to illness
        
        # Apply blessing effects if active
        if self.active_events['blessing'] > 0:
            food_satisfaction *= 1.3  # Increased prosperity from divine blessing
        
        # More forgiving thresholds for population changes
        if food_satisfaction >= 0.65 and self.active_events['plague'] == 0:  # Even more forgiving, no growth during plague
            # Calculate potential population growth
            growth = max(1, int(self.humans * self.human_reproduction_rate * 1.5))
            
            # Calculate available capacity
            remaining_capacity = 100 - self.humans
            
            # If we're approaching capacity, some newborns might leave immediately
            if remaining_capacity < growth and remaining_capacity > 0:
                # Some new humans stay, some leave
                staying = remaining_capacity
                leaving = growth - remaining_capacity
                
                self.humans += staying
                self.total_migrations += leaving
                
                # Check if this forms a new settlement
                if leaving >= 5:
                    self.sister_settlements += 1
                
                if leaving > 0:
                    print(f"HUMAN GROWTH: {growth} new humans born due to abundant food!")
                    print(f"IMMEDIATE MIGRATION: {leaving} young adults left to establish new settlements elsewhere.")
            else:
                # Normal growth, all new humans stay
                self.humans += growth
                if growth > 1:
                    print(f"HUMAN GROWTH: {growth} new humans born due to abundant food!")
        elif food_satisfaction < 0.25:  # More forgiving floor
            # Population decreases if hungry - less severe
            decline = max(1, int(self.humans * 0.08))  # Further reduced from 0.1
            # Knowledge reduces death rate
            decline = max(1, int(decline * (1.0 - self.survival_knowledge * 0.2)))
            self.humans = max(0, self.humans - decline)
            if decline > 1:
                print(f"HUMAN DECLINE: {decline} humans died due to food shortage!")
        
        # Migration of excess humans to form new settlements
        self.trigger_migration()
        
        # Chance for interaction with sister settlements
        self.sister_settlement_interaction()
        
        # Natural constraints - carrying capacity
        self.plants = min(500, max(self.plant_reserves, self.plants))
        self.animals = min(200, max(0, self.animals))
        self.humans = min(100, max(0, self.humans))  # This line remains, but the migration logic will usually keep it below 100
        
        # Record history
        self.history['humans'].append(self.humans)
        self.history['animals'].append(self.animals)
        self.history['plants'].append(self.plants)
        self.history['rainfall'].append(self.rainfall)
        self.history['food_storage'].append(self.food_storage)
        
        self.days += 1
        
        # Return whether a season changed this update
        return self.current_day_in_season == 0
    
    # Handle migration when human population approaches capacity
    def trigger_migration(self):
        # Only trigger migration if we're near capacity
        if self.humans > 85:  # Approaching the cap of 100
            # Calculate how many will migrate
            migration_percentage = (self.humans - 85) / 15  # Scales from 0 to 1 as population rises from 85 to 100
            migration_chance = 0.5 + (migration_percentage * 0.5)  # Chance increases as population grows
            
            if random.random() < migration_chance:
                # Determine migration size - larger migrations as population approaches cap
                base_migrants = int(self.humans * 0.03)  # Base rate of 3%
                extra_migrants = int((self.humans - 85) * 0.15)  # Additional 15% of population over threshold
                migrants = max(1, base_migrants + extra_migrants)
                
                # Cap to keep a minimum of 85 humans in the tribe
                migrants = min(migrants, self.humans - 85)
                
                if migrants > 0:
                    self.humans -= migrants
                    self.total_migrations += migrants
                    
                    # Update count of sister settlements when a significant group leaves
                    if migrants >= 5:
                        self.sister_settlements += 1
                    
                    # Different messages based on migration size
                    if migrants == 1:
                        print(f"MIGRATION: 1 human has left to establish a new settlement elsewhere.")
                    elif migrants <= 3:
                        print(f"MIGRATION: A small family of {migrants} humans has departed to find new territory.")
                    elif migrants <= 8:
                        print(f"MIGRATION: A group of {migrants} humans has migrated to establish a new settlement.")
                    else:
                        print(f"MAJOR MIGRATION: A large band of {migrants} humans has departed to establish a new colony!")
                        
                    # Chance for knowledge sharing between settlements
                    if random.random() < 0.3 and self.days > 60:
                        knowledge_gain = random.uniform(0.05, 0.2)
                        self.survival_knowledge += knowledge_gain
                        print(f"CULTURAL EXCHANGE: The new settlement maintains contact, increasing knowledge by {knowledge_gain:.2f}!")
                    
                    return migrants
            
            # If no migration happened but we're at capacity, show crowding message
            elif self.humans >= 95:
                print("CROWDING: The settlement is reaching its sustainable capacity - migration may occur soon.")
        
        return 0
    
    # Simulate interactions with sister settlements
    def sister_settlement_interaction(self):
        # Only happens if we have sister settlements
        if self.sister_settlements == 0:
            return
        
        # Interaction chance based on number of sister settlements
        interaction_chance = min(0.15, 0.02 * self.sister_settlements)
        
        # More likely during good weather seasons
        if self.seasons[self.current_season] in ["Spring", "Summer"]:
            interaction_chance *= 1.5
        
        # Less likely during winter
        if self.seasons[self.current_season] == "Winter":
            interaction_chance *= 0.3
        
        if random.random() < interaction_chance:
            interaction_type = random.choices(
                ["trade", "knowledge", "population_return", "food_gift", "hunting_party"],
                weights=[0.4, 0.3, 0.15, 0.1, 0.05],
                k=1
            )[0]
            
            if interaction_type == "trade":
                # Trading goods with sister settlements
                trade_amount = random.randint(2, 6)
                self.food_storage = min(self.max_food_storage, self.food_storage + trade_amount)
                print(f"SETTLEMENT NETWORK: A trading party from a sister settlement brought {trade_amount} units of food!")
                
            elif interaction_type == "knowledge":
                # Knowledge exchange
                knowledge_gain = random.uniform(0.1, 0.3)
                self.survival_knowledge += knowledge_gain
                
                # Chance to gain specialized knowledge
                if random.random() < 0.4:
                    if random.random() < 0.5:
                        self.farming_level += 1
                        self.farming_efficiency = 1.0 + (self.farming_level * 0.15)
                        print(f"CULTURAL EXCHANGE: Visitors from sister settlement shared advanced farming techniques! (Level {self.farming_level})")
                    else:
                        self.tools_quality += 0.1
                        print(f"CULTURAL EXCHANGE: Visitors from sister settlement shared improved tool-making methods! (Quality: {self.tools_quality:.1f}x)")
                else:
                    print(f"CULTURAL EXCHANGE: Contact with sister settlements increased knowledge by {knowledge_gain:.2f}!")
                    
            elif interaction_type == "population_return":
                # Some people return from sister settlements
                returnees = random.randint(1, 3)
                free_capacity = 100 - self.humans
                actual_returnees = min(returnees, free_capacity)
                
                if actual_returnees > 0:
                    self.humans += actual_returnees
                    print(f"POPULATION FLOW: {actual_returnees} humans have returned from sister settlements!")
                    
            elif interaction_type == "food_gift":
                # Emergency food aid during hard times
                if self.food_storage < 10 and (self.plants < 50 or self.animals < 20):
                    aid_amount = random.randint(5, 12)
                    self.food_storage += aid_amount
                    self.food_storage = min(self.max_food_storage, self.food_storage)
                    print(f"COMMUNITY SUPPORT: Sister settlements sent {aid_amount} units of emergency food aid!")
                    
            elif interaction_type == "hunting_party":
                # Joint hunting party increases animal catch
                if self.animals > 30:  # Only if enough animals
                    hunting_bonus = random.randint(2, 5)
                    self.food_storage += hunting_bonus
                    self.food_storage = min(self.max_food_storage, self.food_storage)
                    print(f"JOINT VENTURE: A combined hunting party with sister settlement hunters brought in {hunting_bonus} extra food!")
    
    def status_report(self):
        print(f"\n===== DAY {self.days} | {self.seasons[self.current_season]} (Day {self.current_day_in_season+1}) =====")
        print(f"Rainfall: {self.rainfall}/100 {'(SEVERE DROUGHT)' if self.rainfall < self.drought_threshold else '(FLOODING)' if self.rainfall > self.flood_threshold else '(Normal)'}")
        print(f"Humans: {self.humans}")
        print(f"Animals: {self.animals}")
        print(f"Plants: {self.plants} (includes {self.plant_reserves} protected plants)")
        
        # Show active divine events
        active_events = [event for event, duration in self.active_events.items() if duration > 0]
        if active_events:
            print("\nACTIVE DIVINE EVENTS:")
            for event in active_events:
                print(f"  - {event.replace('_', ' ').title()}: {self.active_events[event]} days remaining")
        
        # Show conservation status if active
        if self.animal_conservation_level > 0:
            print(f"Animal Conservation: Level {self.animal_conservation_level} ({self.animal_reserves} protected animals)")
        
        if self.plant_conservation_level > 0:
            print(f"Plant Conservation: Level {self.plant_conservation_level}")
        
        # Show advanced human capabilities
        if self.food_storage > 0:
            print(f"Food Storage: {self.food_storage}/{self.max_food_storage}")
        
        print(f"Survival Knowledge: {self.survival_knowledge:.2f}")
        
        if self.farming_level > 0:
            print(f"Farming: Level {self.farming_level} (Efficiency {self.farming_efficiency:.1f}x)")
        
        print(f"Tool Quality: {self.tools_quality:.1f}x")
        
        # Add migration information
        if self.total_migrations > 0:
            print(f"Migration: {self.total_migrations} humans have migrated to establish new settlements")
            if self.sister_settlements > 0:
                print(f"Sister Settlements: {self.sister_settlements} established settlements in the region")
        
        plant_modifier = self.get_plant_growth_modifier()
        if plant_modifier > 1.5:
            print("Plants are EXPLODING with growth!")
        elif plant_modifier > 1.2:
            print("Plants are thriving!")
        elif plant_modifier < 0.5:
            print("Plants are SEVERELY struggling to grow!")
        elif plant_modifier < 0.8:
            print("Plants are growing slowly.")
        
        if self.humans == 0:
            print("The human population has DIED OUT!")
        elif self.humans >= 50:
            print("The human population is BOOMING!")
        
        if self.animals < 10:
            print("WARNING: Animal population is CRITICALLY ENDANGERED!")
        elif self.animals == 0:
            print("The animal population has gone EXTINCT!")
        elif self.animals > 150:
            print("The animal population is ABUNDANT!")
            
        if self.plants < 30:
            print("WARNING: Plant resources are CRITICALLY SCARCE!")
        elif self.plants > 400:
            print("Plant life is OVERGROWING the region!")
    
    def summary_report(self):
        """Print a summary report of the current simulation state and history"""
        print("\nPOPULATION SUMMARY:")
        print(f"Humans: Started with 10, Now at {self.humans}")
        print(f"Animals: Started with 50, Now at {self.animals}")
        print(f"Plants: Started with 100, Now at {self.plants}")
        
        # Add migration summary
        if self.total_migrations > 0:
            print(f"Total Migrations: {self.total_migrations} humans have left to establish new communities")
            if self.sister_settlements > 0:
                print(f"Sister Settlements: {self.sister_settlements} new settlements established in the region")
        
        if len(self.history['humans']) > 0:
            print("\nPOPULATION RANGES:")
            print(f"Human population ranged from {min(self.history['humans'])} to {max(self.history['humans'])}")
            print(f"Animal population ranged from {min(self.history['animals'])} to {max(self.history['animals'])}")
            print(f"Plant population ranged from {min(self.history['plants'])} to {max(self.history['plants'])}")
            print(f"\nSimulation has run for {self.days} days ({self.days // 30} months, {(self.days // 30) // 12} years)")
            print(f"Survival Knowledge Level: {self.survival_knowledge:.2f}")
            print(f"Farming Level: {self.farming_level}")
            print(f"Animal Conservation Level: {self.animal_conservation_level}")
            print(f"Plant Conservation Level: {self.plant_conservation_level}")
            print(f"Tool Quality: {self.tools_quality:.1f}x")
            print(f"Food Storage Capacity: {self.max_food_storage}")
            
            # OPTIONAL: Calculate theoretical total human population (current + migrants)
            theoretical_population = self.humans + self.total_migrations
            print(f"Theoretical Total Human Population (Current + Migrated): {theoretical_population}")

    # GOD MODE METHODS
    
    def trigger_plague(self, duration=5):
        """Trigger a plague that reduces human population"""
        self.active_events['plague'] = duration
        print(f"DIVINE INTERVENTION: You have triggered a plague for {duration} days!")
        
    def trigger_drought(self, duration=10):
        """Trigger a drought that severely reduces rainfall"""
        self.active_events['drought'] = duration
        # Immediately reduce rainfall
        self.rainfall = max(5, self.rainfall - random.randint(20, 40))
        print(f"DIVINE INTERVENTION: You have triggered a severe drought for {duration} days!")
        
    def trigger_animal_disease(self, duration=7):
        """Trigger a disease affecting animals"""
        self.active_events['animal_disease'] = duration
        print(f"DIVINE INTERVENTION: You have triggered an animal disease for {duration} days!")
        
    def trigger_plant_blight(self, duration=8):
        """Trigger a severe disease affecting plants"""
        self.active_events['plant_blight'] = duration
        
        # Make it more dramatic - immediately wipe out a significant portion of plants
        plant_reserves = self.plant_reserves  # Save the protected reserves
        plant_loss_percentage = random.uniform(0.3, 0.5)  # 30-50% of plants affected
        plant_loss = min(int(self.plants * plant_loss_percentage), self.plants - self.plant_reserves)
        
        if plant_loss > 0:
            self.plants -= plant_loss
            
            # Dramatic description based on severity
            if plant_loss_percentage > 0.4:
                print(f"CATASTROPHIC BLIGHT: A devastating fungal disease has swept through the region!")
                print(f"DIVINE WRATH: {plant_loss} plants withered and blackened before your eyes!")
                print(f"The few remaining plants show signs of infection, and the disease will continue for {duration} days.")
            else:
                print(f"DIVINE INTERVENTION: A virulent plant blight has struck the ecosystem!")
                print(f"DESTRUCTION: {plant_loss} plants have been destroyed, their leaves curling and falling away!")
                print(f"The blight will continue to spread for {duration} more days.")
            
            # Chance for mutation that affects farming efficiency temporarily
            if self.farming_level > 0 and random.random() < 0.7:
                old_efficiency = self.farming_efficiency
                reduction = random.uniform(0.2, 0.4)
                self.farming_efficiency = max(0.5, self.farming_efficiency * (1 - reduction))
                print(f"MUTATION: The blight has damaged farming knowledge! Efficiency temporarily reduced from {old_efficiency:.1f}x to {self.farming_efficiency:.1f}x")
                print("Farming efficiency will recover when the blight ends.")
        else:
            print(f"DIVINE INTERVENTION: You have triggered a plant blight for {duration} days!")
        
        # Chance to affect the animal population as well (through food chain)
        if random.random() < 0.4 and self.animals > 20:
            animal_sickness = min(int(self.animals * 0.15), self.animals - 10)
            if animal_sickness > 0:
                self.animals -= animal_sickness
                print(f"ECOSYSTEM IMPACT: {animal_sickness} animals sickened after consuming blighted plants!")

            
    def grant_blessing(self, duration=7):
        """Grant a divine blessing that improves all conditions"""
        self.active_events['blessing'] = duration
        # Immediate effects
        self.rainfall = min(70, self.rainfall + random.randint(10, 20))  # Improve rainfall toward ideal
        # Give humans some food
        blessing_food = random.randint(5, 15)
        self.food_storage = min(self.max_food_storage, self.food_storage + blessing_food)
        print(f"DIVINE INTERVENTION: You have granted a blessing for {duration} days! Rainfall improved and {blessing_food} units of food appeared.")
    
    def set_human_population(self, new_population):
        """Directly set human population to a specific value"""
        old_pop = self.humans
        self.humans = max(0, min(100, new_population))  # Constrain within limits
        print(f"DIVINE INTERVENTION: Human population changed from {old_pop} to {self.humans}")
        
    def set_animal_population(self, new_population):
        """Directly set animal population to a specific value"""
        old_pop = self.animals
        self.animals = max(0, min(200, new_population))  # Constrain within limits
        print(f"DIVINE INTERVENTION: Animal population changed from {old_pop} to {self.animals}")
        
    def set_plant_population(self, new_population):
        """Directly set plant population to a specific value"""
        old_pop = self.plants
        self.plants = max(self.plant_reserves, min(500, new_population))  # Ensure plant reserves remain
        print(f"DIVINE INTERVENTION: Plant population changed from {old_pop} to {self.plants}")
        
    def set_rainfall(self, new_rainfall):
        """Directly set rainfall to a specific value"""
        old_rain = self.rainfall
        self.rainfall = max(0, min(100, new_rainfall))  # Constrain within limits
        print(f"DIVINE INTERVENTION: Rainfall changed from {old_rain} to {self.rainfall}")
        
    def boost_knowledge(self, amount=0.5):
        """Give humans a boost in knowledge"""
        old_knowledge = self.survival_knowledge
        self.survival_knowledge += amount
        print(f"DIVINE INTERVENTION: Human knowledge increased from {old_knowledge:.2f} to {self.survival_knowledge:.2f}")
        
    def boost_farming(self, levels=1):
        """Boost human farming capability"""
        old_level = self.farming_level
        self.farming_level += levels
        self.farming_efficiency = 1.0 + (self.farming_level * 0.15)
        print(f"DIVINE INTERVENTION: Farming level increased from {old_level} to {self.farming_level} (Efficiency: {self.farming_efficiency:.1f}x)")
        
    def trigger_flood(self):
        """Trigger an immediate flood"""
        old_rain = self.rainfall
        self.rainfall = min(100, self.rainfall + random.randint(30, 50))
        print(f"DIVINE INTERVENTION: You have triggered a flood! Rainfall spiked from {old_rain} to {self.rainfall}.")
        
    def add_food(self, amount=10):
        """Add food to human storage"""
        self.food_storage = min(self.max_food_storage, self.food_storage + amount)
        print(f"DIVINE INTERVENTION: {amount} units of food added to storage (Total: {self.food_storage}/{self.max_food_storage})")
        
    def cancel_events(self):
        """Cancel all active divine events"""
        active_count = sum(1 for duration in self.active_events.values() if duration > 0)
        if active_count > 0:
            for event in self.active_events:
                self.active_events[event] = 0
            print(f"DIVINE INTERVENTION: All {active_count} active events have been canceled.")
        else:
            print("No active events to cancel.")


def run_command_based_simulation():
    """Run the ecosystem simulation with flexible command-based control"""
    ecosystem = SimpleEcosystem()
    
    print("Starting Command-Based Hunter-Gatherer Ecosystem Simulation with GOD MODE")
    print("\nAVAILABLE COMMANDS:")
    print("  SIMULATION COMMANDS:")
    print("  day [n]      - Simulate n days (default: 1)")
    print("  week [n]     - Simulate n weeks (default: 1)")
    print("  month [n]    - Simulate n months (default: 1)")
    print("  season [n]   - Simulate n seasons (default: 1)")
    print("  year [n]     - Simulate n years (default: 1)")
    print("  status       - Show current ecosystem status")
    print("  summary      - Show simulation summary")
    print("  help         - Show available commands")
    print("  quit         - Exit simulation")
    print("\n  GOD MODE COMMANDS:")
    print("  plague [n]   - Trigger a plague for n days (default: 5)")
    print("  drought [n]  - Trigger a drought for n days (default: 10)")
    print("  flood        - Trigger an immediate flood")
    print("  bless [n]    - Grant divine blessing for n days (default: 7)")
    print("  animal_disease [n] - Trigger animal disease for n days (default: 7)")
    print("  plant_blight [n]   - Trigger plant disease for n days (default: 8)")
    print("  humans [n]   - Set human population to n")
    print("  animals [n]  - Set animal population to n")
    print("  plants [n]   - Set plant population to n")
    print("  rain [n]     - Set rainfall to n (0-100)")
    print("  food [n]     - Add n food to storage (default: 10)")
    print("  knowledge [n]- Boost knowledge by n amount (default: 0.5)")
    print("  farming [n]  - Boost farming by n levels (default: 1)")
    print("  cancel       - Cancel all active divine events")
    print("  god_help     - Show god mode commands")
    ecosystem.status_report()
    
    while True:
        try:
            # Get user command
            command_input = input("\nCommand: ").strip().lower()
            
            # Parse command and arguments
            parts = command_input.split()
            if not parts:
                continue
                
            command = parts[0]
            
            # Get numeric argument if provided
            value = 1  # Default value if not specified
            if len(parts) > 1:
                try:
                    value = int(parts[1])
                    if value <= 0 and command not in ['humans', 'animals', 'plants', 'rain']:
                        print("Please enter a positive number")
                        continue
                except ValueError:
                    print(f"Invalid number: {parts[1]}")
                    continue
            
            # Process commands
            if command == "quit" or command == "exit":
                print("\nSimulation ended by user")
                break
                
            elif command == "help":
                print("\nAVAILABLE COMMANDS:")
                print("  SIMULATION COMMANDS:")
                print("  day [n]      - Simulate n days (default: 1)")
                print("  week [n]     - Simulate n weeks (default: 1)")
                print("  month [n]    - Simulate n months (default: 1)")
                print("  season [n]   - Simulate n seasons (default: 1)")
                print("  year [n]     - Simulate n years (default: 1)")
                print("  status       - Show current ecosystem status")
                print("  summary      - Show simulation summary")
                print("  help         - Show available commands")
                print("  quit         - Exit simulation")
                print("\n  Type 'god_help' to see god mode commands")
                
            elif command == "god_help":
                print("\n  GOD MODE COMMANDS:")
                print("  plague [n]   - Trigger a plague for n days (default: 5)")
                print("  drought [n]  - Trigger a drought for n days (default: 10)")
                print("  flood        - Trigger an immediate flood")
                print("  bless [n]    - Grant divine blessing for n days (default: 7)")
                print("  animal_disease [n] - Trigger animal disease for n days (default: 7)")
                print("  plant_blight [n]   - Trigger plant disease for n days (default: 8)")
                print("  humans [n]   - Set human population to n")
                print("  animals [n]  - Set animal population to n")
                print("  plants [n]   - Set plant population to n")
                print("  rain [n]     - Set rainfall to n (0-100)")
                print("  food [n]     - Add n food to storage (default: 10)")
                print("  knowledge [n]- Boost knowledge by n amount (default: 0.5)")
                print("  farming [n]  - Boost farming by n levels (default: 1)")
                print("  cancel       - Cancel all active divine events")
                
            elif command == "status":
                ecosystem.status_report()
                
            elif command == "summary":
                ecosystem.summary_report()
                
            # GOD MODE COMMANDS
            elif command == "plague":
                duration = value if len(parts) > 1 else 5  # Default 5 days
                ecosystem.trigger_plague(duration)
                
            elif command == "drought":
                duration = value if len(parts) > 1 else 10  # Default 10 days
                ecosystem.trigger_drought(duration)
                
            elif command == "flood":
                ecosystem.trigger_flood()
                
            elif command == "bless":
                duration = value if len(parts) > 1 else 7  # Default 7 days
                ecosystem.grant_blessing(duration)
                
            elif command == "animal_disease":
                duration = value if len(parts) > 1 else 7  # Default 7 days
                ecosystem.trigger_animal_disease(duration)
                
            elif command == "plant_blight":
                duration = value if len(parts) > 1 else 8  # Default 8 days
                ecosystem.trigger_plant_blight(duration)
                
            elif command == "humans":
                if len(parts) > 1:
                    ecosystem.set_human_population(value)
                else:
                    print("Please specify a population value")
                    
            elif command == "animals":
                if len(parts) > 1:
                    ecosystem.set_animal_population(value)
                else:
                    print("Please specify a population value")
                    
            elif command == "plants":
                if len(parts) > 1:
                    ecosystem.set_plant_population(value)
                else:
                    print("Please specify a population value")
                    
            elif command == "rain":
                if len(parts) > 1:
                    ecosystem.set_rainfall(value)
                else:
                    print("Please specify a rainfall value (0-100)")
                    
            elif command == "food":
                amount = value if len(parts) > 1 else 10  # Default 10 units
                ecosystem.add_food(amount)
                
            elif command == "knowledge":
                amount = float(value) if len(parts) > 1 else 0.5  # Default 0.5
                ecosystem.boost_knowledge(amount)
                
            elif command == "farming":
                levels = value if len(parts) > 1 else 1  # Default 1 level
                ecosystem.boost_farming(levels)
                
            elif command == "cancel":
                ecosystem.cancel_events()
                
            elif command == "day":
                days_to_simulate = value
                print(f"Simulating {days_to_simulate} day(s)...")
                
                season_changed = False
                for _ in range(days_to_simulate):
                    season_changed_this_update = ecosystem.update()
                    season_changed = season_changed or season_changed_this_update
                    
                    # End simulation if humans die out
                    if ecosystem.humans == 0:
                        print("\nSimulation ended: Human population extinct")
                        break
                
                # Only show status report at the end, not for each day
                ecosystem.status_report()
                
            elif command == "week":
                days_to_simulate = value * 7
                print(f"Simulating {value} week(s) ({days_to_simulate} days)...")
                
                season_changes = 0
                for _ in range(days_to_simulate):
                    season_changed = ecosystem.update()
                    if season_changed:
                        season_changes += 1
                        # Don't print status here, as update() already announces season change
                    
                    # End simulation if humans die out
                    if ecosystem.humans == 0:
                        print("\nSimulation ended: Human population extinct")
                        break
                
                # Only show final status
                ecosystem.status_report()
                
            elif command == "month":
                days_to_simulate = value * 30
                print(f"Simulating {value} month(s) ({days_to_simulate} days)...")
                
                for _ in range(days_to_simulate):
                    season_changed = ecosystem.update()
                    # End simulation if humans die out
                    if ecosystem.humans == 0:
                        print("\nSimulation ended: Human population extinct")
                        break
                
                # Only report at the end
                ecosystem.status_report()
                
            elif command == "season":
                print(f"Simulating {value} season(s)...")
                
                seasons_completed = 0
                current_season = ecosystem.current_season
                
                # Continue until we've completed the requested number of seasons
                while seasons_completed < value and ecosystem.humans > 0:
                    season_changed = ecosystem.update()
                    
                    # Check if season changed
                    if season_changed:
                        seasons_completed += 1
                        # Don't print status here as update() already announces season changes
                
                # Final status report after all seasons are done
                ecosystem.status_report()
                
            elif command == "year":
                print(f"Simulating {value} year(s)...")
                seasons_per_year = 4
                seasons_to_simulate = value * seasons_per_year
                
                seasons_completed = 0
                while seasons_completed < seasons_to_simulate and ecosystem.humans > 0:
                    season_changed = ecosystem.update()
                    
                    # Check if season changed
                    if season_changed:
                        seasons_completed += 1
                        # Season change is announced by update()
                
                # Final status after completion
                ecosystem.status_report()
                
            else:
                print(f"Unknown command: {command}. Type 'help' for available commands or 'god_help' for god mode commands.")
                
        except Exception as e:
            print(f"Error: {e}")
        
        # Check if humans died out during simulation
        if ecosystem.humans == 0:
            print("\nSimulation ended: Human population extinct")
            break
    
    # Final summary at the end
    print("\nFinal Results:")
    ecosystem.summary_report()

if __name__ == "__main__":
    run_command_based_simulation()