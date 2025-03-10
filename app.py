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

def lootbox_tab():
    """Content for the Loot Box tab"""
    # Display UI components for the loot box tab
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
    
    display_inventory_stats(st.session_state.loot_box)
    display_currency_status(st.session_state.loot_box)
    display_drop_rates(st.session_state.loot_box)

def collection_tab():
    """Content for the Collection tab"""
    st.header("🏆 Your Collection")
    
    loot_box = st.session_state.loot_box
    stats = loot_box.get_collection_stats()
    
    # Summary statistics
    st.subheader("Collection Summary")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        total_items = sum(item["total"] for item in loot_box.unique_items.values())
        collected_items = sum(len(item["collected"]) for item in loot_box.unique_items.values())
        completion_pct = (collected_items / total_items * 100) if total_items > 0 else 0
        st.metric("Overall Completion", f"{completion_pct:.1f}%")
    
    with col2:
        st.metric("Items Collected", f"{collected_items}/{total_items}")
    
    with col3:
        st.metric("Boxes Opened", stats["boxes_opened"])
    
    # Detailed collection progress
    st.subheader("Collection Details")
    
    # Group items by category
    categories = {
        "Emotes": ["Emote T1", "Emote T2"],
        "Spawn Platforms": ["Spawn Plat T1", "Spawn Plat T2"],
        "Pets": ["Pets T1", "Pets T2"],
        "Chess Sets": ["Chess Set: T1", "Chess Set: T2", "Chess Set: T3"]
    }
    
    # Display each category in an expander
    for category, item_types in categories.items():
        with st.expander(f"{category}", expanded=True):
            for item_type in item_types:
                if item_type in stats["collection_progress"]:
                    item_stats = stats["collection_progress"][item_type]
                    
                    # Skip items with 0 total
                    if item_stats["total"] == 0:
                        continue
                    
                    # Create a progress bar with more details
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.progress(item_stats["progress"])
                    with col2:
                        st.write(f"{item_stats['collected']}/{item_stats['total']}")
                    
                    st.caption(f"{item_type}: {item_stats['progress']*100:.1f}% complete")
                    
                    # If we have items collected, show a visual representation
                    if item_stats["collected"] > 0:
                        # Create a grid of colored squares to represent collected items
                        # This is a simple visualization - you could enhance this further
                        cols = st.columns(10)
                        for i in range(min(50, item_stats["total"])):
                            with cols[i % 10]:
                                if i < item_stats["collected"]:
                                    st.markdown("🟢")  # Collected
                                else:
                                    st.markdown("⚪")  # Not collected
                        
                        if item_stats["total"] > 50:
                            st.caption(f"Showing 50/{item_stats['total']} items")
    
    # Currency section
    st.subheader("💰 Currency Status")
    st.metric("Total Currency", stats["total_currency"])
    
    # Currency breakdown
    currency_data = stats["currency_collected"]
    st.bar_chart(currency_data)

def main():
    st.title("🎁 Loot Box Simulator")
    
    # Initialize the loot box if it doesn't exist
    if "loot_box" not in st.session_state:
        st.session_state.loot_box = LootBox()
    
    # Create tabs
    tab1, tab2 = st.tabs(["🎁 Loot Box", "🏆 Collection"])
    
    # Content for Loot Box tab
    with tab1:
        lootbox_tab()
    
    # Content for Collection tab
    with tab2:
        collection_tab()

if __name__ == "__main__":
    main() 