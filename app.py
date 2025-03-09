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
    
    # Display batch summary if available
    if hasattr(st.session_state, 'batch_summary'):
        with st.expander("📊 Batch Opening Summary", expanded=True):
            summary = st.session_state.batch_summary
            
            # Create columns for summary stats
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Boxes Opened", summary["boxes_opened"])
            with col2:
                st.metric("Currency Gained", summary["currency_gained"])
            with col3:
                st.metric("New Duplicates", summary["new_duplicates"])
            
            # Show new items collected
            st.subheader("New Items Collected")
            for item_type, count in summary["new_items"].items():
                if count > 0:
                    st.success(f"{item_type}: +{count} new items")
    
    display_inventory_stats(loot_box)
    display_collection_progress(loot_box)
    display_currency_status(loot_box)
    display_drop_rates(loot_box)

if __name__ == "__main__":
    main() 