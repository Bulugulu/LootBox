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
        
        # Drop rates configuration
        self.item_config = {
            "Currency High": {"drop_rate": 5.0, "max_count": float('inf'), "collected": 0, "value": 100},
            "Currency Med": {"drop_rate": 8.0, "max_count": float('inf'), "collected": 0, "value": 50},
            "Currency Low": {"drop_rate": 18.0, "max_count": float('inf'), "collected": 0, "value": 20},
            "Emote T1": {"drop_rate": 10.0, "duplicate_currency": 5},
            "Emote T2": {"drop_rate": 5.0, "duplicate_currency": 10},
            "Spawn Plat T1": {"drop_rate": 5.0, "duplicate_currency": 10},
            "Spawn Plat T2": {"drop_rate": 0.0, "duplicate_currency": 0},
            "Pets T1": {"drop_rate": 20.0, "duplicate_currency": 5},
            "Pets T2": {"drop_rate": 5.0, "duplicate_currency": 10},
            "Chess Set: T1": {"drop_rate": 20.0, "duplicate_currency": 20},
            "Chess Set: T2": {"drop_rate": 4.0, "duplicate_currency": 50},
            "Chess Set: T3": {"drop_rate": 0.0, "duplicate_currency": 0},
        }
        
        total_rate = sum(item["drop_rate"] for item in self.item_config.values())
        if abs(total_rate - 100.0) > 0.01:
            raise ValueError(f"Drop rates must sum to 100% (current sum: {total_rate}%)")
            
        self.total_currency = 0
        self.boxes_opened = 0
        self.total_duplicates = 0

    def get_random_item_number(self, item_type):
        """Get a random number for a specific item type"""
        return random.randint(1, self.unique_items[item_type]["total"])

    def open_box(self):
        rewards = []
        self.boxes_opened += 1
        
        for _ in range(3):
            items = list(self.item_config.keys())
            probabilities = [self.item_config[item]["drop_rate"] / 100 for item in items]
            
            item = random.choices(items, weights=probabilities, k=1)[0]
            
            if "Currency" in item:
                currency_amount = self.item_config[item]["value"]
                self.total_currency += currency_amount
                rewards.append(f"{item}: {currency_amount}")
                self.item_config[item]["collected"] += 1
            else:
                # Handle unique items (Emotes, Spawn Platforms, Pets, Chess Sets)
                if self.unique_items[item]["total"] > 0:
                    item_number = self.get_random_item_number(item)
                    if item_number in self.unique_items[item]["collected"]:
                        # Duplicate item
                        self.total_duplicates += 1
                        duplicate_currency = self.item_config[item]["duplicate_currency"]
                        self.total_currency += duplicate_currency
                        rewards.append(f"{item} #{item_number} (Duplicate: +{duplicate_currency} currency)")
                    else:
                        # New item
                        self.unique_items[item]["collected"].add(item_number)
                        rewards.append(f"New {item} #{item_number} "
                                    f"({len(self.unique_items[item]['collected'])}/{self.unique_items[item]['total']})")
                else:
                    # This should not happen with proper configuration, but just in case
                    rewards.append(f"Error: {item} has no items to collect")
        
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
                "Currency High": self.item_config["Currency High"]["collected"],
                "Currency Med": self.item_config["Currency Med"]["collected"],
                "Currency Low": self.item_config["Currency Low"]["collected"]
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