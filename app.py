import streamlit as st
from lootbox_model import LootBox
from lootbox_ui import (
    display_controls,
    display_rewards,
    display_inventory_stats,
    display_collection_progress,
    display_currency_status,
    display_drop_rates
)

def main():
    st.title("🎁 Loot Box Simulator")
    
    # Initialize the loot box if it doesn't exist
    if "loot_box" not in st.session_state:
        st.session_state.loot_box = LootBox()

    loot_box = st.session_state.loot_box
    
    # Display UI components
    display_controls()
    display_rewards()
    display_inventory_stats(loot_box)
    display_collection_progress(loot_box)
    display_currency_status(loot_box)
    display_drop_rates(loot_box)

if __name__ == "__main__":
    main() 