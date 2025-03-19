import random

class LootBox:
    def __init__(self):
        # Define total unique items for each category
        self.unique_items = {
            "Emote T1": {"total": 20, "collected": set()},
            "Emote T2": {"total": 8, "collected": set()},
            "Spawn Plat T1": {"total": 8, "collected": set()},
            "Spawn Plat T2": {"total": 0, "collected": set()},
            "Pets T1": {"total": 56, "collected": set()},
            "Pets T2": {"total": 32, "collected": set()},
            "Chess Set: T1": {"total": 112, "collected": set()},
            "Chess Set: T2": {"total": 32, "collected": set()},
            "Chess Set: T3": {"total": 0, "collected": set()},
        }
        
        # Configure item properties
        self.item_properties = {
            "Currency High": {"value": 100, "collected": 0},
            "Currency Med": {"value": 50, "collected": 0},
            "Currency Low": {"value": 20, "collected": 0},
            "Emote T1": {"duplicate_currency": 5},
            "Emote T2": {"duplicate_currency": 10},
            "Spawn Plat T1": {"duplicate_currency": 10},
            "Spawn Plat T2": {"duplicate_currency": 0},
            "Pets T1": {"duplicate_currency": 5},
            "Pets T2": {"duplicate_currency": 10},
            "Chess Set: T1": {"duplicate_currency": 20},
            "Chess Set: T2": {"duplicate_currency": 50},
            "Chess Set: T3": {"duplicate_currency": 0},
        }
        
        # Using original drop rates for all slots
        original_loot_table = {
            "Currency High": 5.0,
            "Currency Med": 8.0,
            "Currency Low": 18.0,
            "Emote T1": 10.0,
            "Emote T2": 5.0,
            "Spawn Plat T1": 5.0,
            "Spawn Plat T2": 0.0,
            "Pets T1": 20.0,
            "Pets T2": 5.0,
            "Chess Set: T1": 20.0,
            "Chess Set: T2": 4.0,
            "Chess Set: T3": 0.0,
        }
        
        # Define slot-specific loot tables (all using the same original probabilities for now)
        self.slot_loot_tables = [
            original_loot_table.copy(),  # Slot 1
            original_loot_table.copy(),  # Slot 2
            original_loot_table.copy()   # Slot 3
        ]
        
        # Validate each slot's loot table adds up to 100%
        for i, loot_table in enumerate(self.slot_loot_tables):
            total_rate = sum(loot_table.values())
            if abs(total_rate - 100.0) > 0.01:
                raise ValueError(f"Slot {i+1} drop rates must sum to 100% (current sum: {total_rate}%)")
        
        self.total_currency = 0
        self.boxes_opened = 0
        self.total_duplicates = 0

    def get_random_item_number(self, item_type):
        """Get a random number for a specific item type"""
        return random.randint(1, self.unique_items[item_type]["total"])

    def get_item_from_slot(self, slot_index):
        """Get a random item from the specified slot's loot table"""
        loot_table = self.slot_loot_tables[slot_index]
        items = list(loot_table.keys())
        probabilities = [loot_table[item] / 100 for item in items]
        
        return random.choices(items, weights=probabilities, k=1)[0]

    def open_box(self):
        """Open a loot box and get rewards from all three slots"""
        rewards = []
        self.boxes_opened += 1
        
        for slot_index in range(3):
            item = self.get_item_from_slot(slot_index)
            
            if "Currency" in item:
                currency_amount = self.item_properties[item]["value"]
                self.total_currency += currency_amount
                rewards.append(f"Slot {slot_index+1}: {item}: {currency_amount}")
                self.item_properties[item]["collected"] += 1
            else:
                # Handle unique items (Emotes, Spawn Platforms, Pets, Chess Sets)
                if self.unique_items[item]["total"] > 0:
                    item_number = self.get_random_item_number(item)
                    if item_number in self.unique_items[item]["collected"]:
                        # Duplicate item
                        self.total_duplicates += 1
                        duplicate_currency = self.item_properties[item]["duplicate_currency"]
                        self.total_currency += duplicate_currency
                        rewards.append(f"Slot {slot_index+1}: {item} #{item_number} (Duplicate: +{duplicate_currency} currency)")
                    else:
                        # New item
                        self.unique_items[item]["collected"].add(item_number)
                        rewards.append(f"Slot {slot_index+1}: New {item} #{item_number} "
                                    f"({len(self.unique_items[item]['collected'])}/{self.unique_items[item]['total']})")
                else:
                    # This should not happen with proper configuration, but just in case
                    rewards.append(f"Slot {slot_index+1}: Error: {item} has no items to collect")
        
        return rewards

    def get_collection_stats(self):
        """Return collection statistics for display"""
        stats = {
            "boxes_opened": self.boxes_opened,
            "total_currency": self.total_currency,
            "total_duplicates": self.total_duplicates,
            "avg_currency": self.total_currency / self.boxes_opened if self.boxes_opened > 0 else 0,
            "collection_progress": {},
            "currency_collected": {
                "Currency High": self.item_properties["Currency High"]["collected"],
                "Currency Med": self.item_properties["Currency Med"]["collected"],
                "Currency Low": self.item_properties["Currency Low"]["collected"]
            }
        }
        
        for item_type in sorted(self.unique_items.keys()):
            collected = len(self.unique_items[item_type]["collected"])
            total = self.unique_items[item_type]["total"]
            progress = (collected / total) if total > 0 else 0
            stats["collection_progress"][item_type] = {
                "collected": collected,
                "total": total,
                "progress": progress
            }
            
        return stats

    def open_multiple_boxes(self, count):
        """Open multiple boxes and return summary statistics"""
        all_rewards = []
        initial_currency = self.total_currency
        initial_duplicates = self.total_duplicates
        initial_collected = {
            item_type: len(self.unique_items[item_type]["collected"]) 
            for item_type in self.unique_items
        }
        
        for _ in range(count):
            rewards = self.open_box()
            all_rewards.extend(rewards)
        
        # Generate summary statistics
        summary = {
            "boxes_opened": count,
            "currency_gained": self.total_currency - initial_currency,
            "new_duplicates": self.total_duplicates - initial_duplicates,
            "new_items": {
                item_type: len(self.unique_items[item_type]["collected"]) - initial_collected[item_type]
                for item_type in self.unique_items
            },
            "avg_currency_per_box": (self.total_currency - initial_currency) / count if count > 0 else 0
        }
        
        return all_rewards, summary

    def get_slot_drop_rates(self):
        """Return the drop rates for each slot for display"""
        return self.slot_loot_tables 