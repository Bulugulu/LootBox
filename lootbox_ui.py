import streamlit as st
from lootbox_model import LootBox

def display_controls():
    """Display the control buttons for the lootbox simulator"""
    st.subheader("🎮 Controls")
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col2:
        # Make the open box button more prominent
        if st.button("🎁 Open a Loot Box", use_container_width=True):
            rewards = st.session_state.loot_box.open_box()
            st.session_state.last_rewards = rewards

        # Add some spacing
        st.write("")
        
        # Make the reset button less prominent
        if st.button("🔄 Reset Inventory", use_container_width=True, type="secondary"):
            st.session_state.loot_box = LootBox()
            st.session_state.last_rewards = None
            st.rerun()

def display_rewards():
    """Display the latest rewards if they exist"""
    if hasattr(st.session_state, 'last_rewards') and st.session_state.last_rewards:
        with st.expander("🎉 Latest Rewards", expanded=True):
            for reward in st.session_state.last_rewards:
                if "Duplicate" in reward:
                    st.warning(reward)
                elif "New" in reward:
                    st.success(reward)
                else:
                    st.info(reward)

def display_inventory_stats(loot_box):
    """Display inventory statistics"""
    st.divider()
    st.subheader("📦 Inventory Status")
    
    stats = loot_box.get_collection_stats()
    
    # Create columns for stats
    stat_col1, stat_col2, stat_col3 = st.columns(3)
    
    with stat_col1:
        st.metric("Boxes Opened", stats["boxes_opened"])
    
    with stat_col2:
        st.metric("Avg. Currency per Box", f"{stats['avg_currency']:.1f}")
    
    with stat_col3:
        st.metric("Total Duplicates", stats["total_duplicates"])

def display_collection_progress(loot_box):
    """Display collection progress with progress bars"""
    st.subheader("🏆 Collection Progress")
    
    stats = loot_box.get_collection_stats()
    
    for item_type, item_stats in stats["collection_progress"].items():
        st.progress(item_stats["progress"])
        st.caption(f"{item_type}: {item_stats['collected']}/{item_stats['total']} ({item_stats['progress']*100:.1f}%)")

def display_currency_status(loot_box):
    """Display currency statistics"""
    st.subheader("💰 Currency Status")
    
    stats = loot_box.get_collection_stats()
    
    curr_col1, curr_col2 = st.columns(2)
    with curr_col1:
        st.metric("Total Currency", stats["total_currency"])
    with curr_col2:
        total_currency_drops = sum(stats["currency_collected"].values())
        st.metric("Currency Drops", total_currency_drops)

def display_drop_rates(loot_box):
    """Display drop rates with progress bars"""
    st.divider()
    st.subheader("📊 Drop Rates")
    
    for item, config in loot_box.item_config.items():
        st.progress(config['drop_rate'] / 100)
        if item in loot_box.unique_items:
            st.caption(f"{item}: {config['drop_rate']}% (Unique Items: {loot_box.unique_items[item]['total']})")
        else:
            st.caption(f"{item}: {config['drop_rate']}% (Unlimited)") 