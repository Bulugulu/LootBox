import random
import streamlit as st

class LootBox:
    def __init__(self):
        # Define total unique items for each category
        self.unique_items = {
            "Emotes": {"total": 20, "collected": set()},
            "Spawn Plat.": {"total": 8, "collected": set()},
            "Pets": {"total": 80, "collected": set()},
            "Chess Set: T1": {"total": 112, "collected": set()},
            "Chess Set: T2": {"total": 32, "collected": set()},
            "Chess Set: T3": {"total": 2, "collected": set()}
        }
        
        # Drop rates configuration
        self.item_config = {
            "Emotes": {"drop_rate": 15.0},
            "Currency": {"drop_rate": 10.0, "max_count": float('inf'), "collected": 0},
            "Spawn Plat.": {"drop_rate": 5.0},
            "Pets": {"drop_rate": 40.0},
            "Chess Set: T1": {"drop_rate": 25.0},
            "Chess Set: T2": {"drop_rate": 4.5},
            "Chess Set: T3": {"drop_rate": 0.5}
        }
        
        total_rate = sum(item["drop_rate"] for item in self.item_config.values())
        if abs(total_rate - 100.0) > 0.01:
            raise ValueError(f"Drop rates must sum to 100% (current sum: {total_rate}%)")
            
        self.currency_for_duplicate = 100
        self.total_currency = 0
        self.boxes_opened = 0

    def get_random_item_number(self, item_type):
        """Get a random number for a specific item type"""
        return random.randint(1, self.unique_items[item_type]["total"])

    def open_box(self):
        rewards = []
        self.boxes_opened += 1
        
        for _ in range(1):
            items = list(self.item_config.keys())
            probabilities = [self.item_config[item]["drop_rate"] / 100 for item in items]
            
            item = random.choices(items, weights=probabilities, k=1)[0]
            
            if item == "Currency":
                currency_amount = random.randint(50, 200)
                self.total_currency += currency_amount
                rewards.append(f"Currency: {currency_amount}")
                self.item_config[item]["collected"] += 1
            else:
                # Handle unique items (Emotes, Spawn Platforms, Pets, Chess Sets)
                item_number = self.get_random_item_number(item)
                if item_number in self.unique_items[item]["collected"]:
                    # Duplicate item
                    self.total_currency += self.currency_for_duplicate
                    rewards.append(f"{item} #{item_number} (Duplicate: +{self.currency_for_duplicate} currency)")
                else:
                    # New item
                    self.unique_items[item]["collected"].add(item_number)
                    rewards.append(f"New {item} #{item_number} "
                                 f"({len(self.unique_items[item]['collected'])}/{self.unique_items[item]['total']})")
        
        return rewards

    def display_inventory(self):
        print("\nCollection Progress:")
        print(f"Boxes Opened: {self.boxes_opened}")
        print(f"Average Currency per Box: {self.total_currency / self.boxes_opened:.2f}" if self.boxes_opened > 0 else "No boxes opened yet")
        st.text("\nCollection Progress:")
        st.text(f"Boxes Opened: {self.boxes_opened}")
        st.text(f"Average Currency per Box: {self.total_currency / self.boxes_opened:.2f}" if self.boxes_opened > 0 else "No boxes opened yet")



        # Display unique items progress
        for item_type in sorted(self.unique_items.keys()):
            collected = len(self.unique_items[item_type]["collected"])
            total = self.unique_items[item_type]["total"]
            progress = (collected / total * 100)
            print(f"- {item_type}: {collected}/{total} ({progress:.1f}%)")
            st.text(f"- {item_type}: {collected}/{total} ({progress:.1f}%)")
        
        # Display currency
        print(f"- Currency obtained: {self.item_config['Currency']['collected']} times")
        print(f"Total Currency: {self.total_currency}")
        st.text(f"- Currency obtained: {self.item_config['Currency']['collected']} times")
        st.text(f"Total Currency: {self.total_currency}")

    def display_drop_rates(self):
        print("\nDrop Rates:")
        for item, config in self.item_config.items():
            if item in self.unique_items:
                print(f"- {item}: {config['drop_rate']}% (Unique Items: {self.unique_items[item]['total']})")
                st.text(f"- {item}: {config['drop_rate']}% (Unique Items: {self.unique_items[item]['total']})")
            else:
                print(f"- {item}: {config['drop_rate']}% (Unlimited)")
                st.text(f"- {item}: {config['drop_rate']}% (Unlimited)")

def main():
    if "loot_box" not in st.session_state:
        st.session_state.loot_box = LootBox()

    loot_box = st.session_state.loot_box

    st.title("Loot Box Simulator")
    loot_box.display_drop_rates()

    if st.button("Open a Loot Box"):
        rewards = loot_box.open_box()

        st.write("### You received:")
        for reward in rewards:
            st.write(f"- {reward}")

   # Button to reset inventory
    if st.button("Reset Inventory"):
        st.session_state.loot_box = LootBox()  # Reset the loot box instance
        st.write("### Inventory Reset!")

    st.write("### Inventory Update:")
    loot_box.display_inventory()

if __name__ == "__main__":
    main()