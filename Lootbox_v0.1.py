import random
import streamlit as st

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
        
        # Add duplicate counter
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

    def display_inventory(self):
        print("\nCollection Progress:")
        print(f"Boxes Opened: {self.boxes_opened}")
        st.text("\nCollection Progress:")
        st.text(f"Boxes Opened: {self.boxes_opened}")

        if self.boxes_opened > 0:
            avg_currency = self.total_currency / self.boxes_opened
            print(f"Average Currency per Box: {avg_currency:.2f}")
            st.text(f"Average Currency per Box: {avg_currency:.2f}")
        else:
            print("No boxes opened yet")
            st.text("No boxes opened yet")

        # Add duplicate items count
        print(f"Total Duplicate Items: {self.total_duplicates}")
        st.text(f"Total Duplicate Items: {self.total_duplicates}")
        st.text("")

        # Display unique items progress
        for item_type in sorted(self.unique_items.keys()):
            collected = len(self.unique_items[item_type]["collected"])
            total = self.unique_items[item_type]["total"]
            progress = (collected / total * 100) if total > 0 else 0
            print(f"- {item_type}: {collected}/{total} ({progress:.1f}%)")
            st.text(f"- {item_type}: {collected}/{total} ({progress:.1f}%)")
        
        # Display currency
        print(f"- Currency obtained: {self.item_config['Currency High']['collected']} times")
        print(f"- Currency obtained: {self.item_config['Currency Med']['collected']} times")
        print(f"- Currency obtained: {self.item_config['Currency Low']['collected']} times")
        print(f"Total Currency: {self.total_currency}")
        st.text(f"- Currency obtained: {self.item_config['Currency High']['collected']} times")
        st.text(f"- Currency obtained: {self.item_config['Currency Med']['collected']} times")
        st.text(f"- Currency obtained: {self.item_config['Currency Low']['collected']} times")
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

    st.title("🎁 Loot Box Simulator")
    
    # Controls section
    st.subheader("🎮 Controls")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        # Make the open box button more prominent
        if st.button("🎁 Open a Loot Box", use_container_width=True):
            rewards = loot_box.open_box()
            st.session_state.last_rewards = rewards

        # Add some spacing
        st.write("")
        
        # Make the reset button less prominent
        if st.button("🔄 Reset Inventory", use_container_width=True, type="secondary"):
            st.session_state.loot_box = LootBox()
            st.session_state.last_rewards = None
            st.rerun()

    # Display rewards in an expander if they exist
    if hasattr(st.session_state, 'last_rewards') and st.session_state.last_rewards:
        with st.expander("🎉 Latest Rewards", expanded=True):
            for reward in st.session_state.last_rewards:
                if "Duplicate" in reward:
                    st.warning(reward)
                elif "New" in reward:
                    st.success(reward)
                else:
                    st.info(reward)

    # Display inventory in a nice format
    st.divider()
    st.subheader("📦 Inventory Status")
    
    # Create columns for stats
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    with stat_col1:
        st.metric("Boxes Opened", loot_box.boxes_opened)
    
    with stat_col2:
        avg_currency = loot_box.total_currency / loot_box.boxes_opened if loot_box.boxes_opened > 0 else 0
        st.metric("Avg. Currency per Box", f"{avg_currency:.1f}")
    
    with stat_col3:
        st.metric("Total Duplicates", loot_box.total_duplicates)

    # Create a progress bar for each collection category
    st.subheader("🏆 Collection Progress")
    for item_type in sorted(loot_box.unique_items.keys()):
        collected = len(loot_box.unique_items[item_type]["collected"])
        total = loot_box.unique_items[item_type]["total"]
        progress = (collected / total) if total > 0 else 0
        st.progress(progress)
        st.caption(f"{item_type}: {collected}/{total} ({progress*100:.1f}%)")

    # Currency section
    st.subheader("💰 Currency Status")
    curr_col1, curr_col2 = st.columns(2)
    with curr_col1:
        st.metric("Total Currency", loot_box.total_currency)
    with curr_col2:
        st.metric("Currency Drops", loot_box.item_config['Currency High']['collected'] +
                  loot_box.item_config['Currency Med']['collected'] +
                  loot_box.item_config['Currency Low']['collected'])

    # Drop rates section moved to the bottom
    st.divider()
    st.subheader("📊 Drop Rates")
    # Create a more visually appealing drop rates display
    for item, config in loot_box.item_config.items():
        if item in loot_box.unique_items:
            st.progress(config['drop_rate'] / 100)
            st.caption(f"{item}: {config['drop_rate']}% (Unique Items: {loot_box.unique_items[item]['total']})")
        else:
            st.progress(config['drop_rate'] / 100)
            st.caption(f"{item}: {config['drop_rate']}% (Unlimited)")

if __name__ == "__main__":
    main()