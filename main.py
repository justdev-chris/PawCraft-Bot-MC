from pymine import Client
import time

class PawCraftBot:
    def __init__(self, username='PawCraft_Bot'):
        self.client = Client('pawcraft.catsdevs.online', 25565, username=username)
        print(f"🐾 PawCraft Bot connecting to pawcraft.catsdevs.online...")
        self.client.login()
        print("✅ Connected to PawCraft server!")
        
        # Block/item name to ID mapping
        self.block_ids = {
            'wood': 17, 'log': 17, 'oak_wood': 17,
            'stone': 1, 'cobblestone': 4,
            'coal_ore': 16, 'iron_ore': 15, 'diamond_ore': 56,
            'crafting_table': 58, 'furnace': 61,
            'dirt': 3, 'grass': 2
        }
        
        self.item_ids = {
            'planks': 5, 'sticks': 280,
            'wooden_pickaxe': 270, 'stone_pickaxe': 274, 
            'iron_pickaxe': 257, 'diamond_pickaxe': 278,
            'crafting_table': 58, 'furnace': 61
        }
    
    def get_block_id(self, name):
        return self.block_ids.get(name.lower())
    
    def get_item_id(self, name):
        return self.item_ids.get(name.lower())
    
    def wait_for_chunk(self):
        while not self.client.chunks:
            time.sleep(0.1)
    
    def find_nearest_block(self, block_id):
        self.wait_for_chunk()
        player_pos = self.client.position
        nearest = None
        min_dist = float('inf')
        
        for chunk in self.client.chunks.values():
            for x, y, z, block in chunk.blocks():
                if block == block_id:
                    dist = ((player_pos.x - x)**2 + 
                           (player_pos.y - y)**2 + 
                           (player_pos.z - z)**2)
                    if dist < min_dist:
                        min_dist = dist
                        nearest = (x, y, z)
        return nearest
    
    def navigate_and_dig(self, pos, tool=None):
        self.client.position = pos
        self.client.dig(pos[0], pos[1], pos[2])
    
    def craft_item(self, item_id, quantity=1):
        print(f"Crafting item {item_id}")
    
    def drop_item(self, item_name=None, quantity=1):
        """Drop items from inventory"""
        if item_name:
            item_id = self.get_item_id(item_name)
            if item_id:
                print(f"🗑️ Dropping {quantity} {item_name}")
                # Actual drop logic would go here
                # self.client.drop_item(item_id, quantity)
            else:
                print(f"❌ Unknown item: {item_name}")
        else:
            print("🗑️ Dropping all items")
            # Drop entire inventory
            # for item in self.client.inventory:
            #    self.client.drop_item(item.id, item.count)
    
    def execute_task(self, task):
        if task.startswith("find_nearest_"):
            block_type = task.replace("find_nearest_", "")
            block_id = self.get_block_id(block_type)
            pos = self.find_nearest_block(block_id)
            print(f"📍 Found {block_type} at {pos}")
            return pos
            
        elif task.startswith("mine_"):
            block_type = task.replace("mine_", "")
            block_id = self.get_block_id(block_type)
            pos = self.find_nearest_block(block_id)
            if pos:
                print(f"⛏️ Mining {block_type} at {pos}")
                self.navigate_and_dig(pos)
            else:
                print(f"❌ No {block_type} found")
                
        elif task.startswith("craft_"):
            item_name = task.replace("craft_", "")
            item_id = self.get_item_id(item_name)
            if item_id:
                print(f"🛠️ Crafting {item_name}")
                self.craft_item(item_id, 1)
            else:
                print(f"❌ Unknown item: {item_name}")
                
        elif task.startswith("drop_"):
            item_name = task.replace("drop_", "")
            if item_name == "all":
                self.drop_item()
            else:
                self.drop_item(item_name)
        
        else:
            print(f"❌ Unknown task: {task}")

# Usage
if __name__ == "__main__":
    bot = PawCraftBot('PawCraft_Bot')
    
    # Example tasks
    tasks = [
        "find_nearest_wood",
        "mine_wood", 
        "craft_planks",
        "craft_sticks",
        "craft_wooden_pickaxe",
        "drop_sticks",  # Drop sticks if we have too many
        "drop_all"      # Clear inventory
    ]
    
    for task in tasks:
        bot.execute_task(task)
        time.sleep(1)
