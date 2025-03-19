import streamlit as st
from lootbox_model import LootBox

def display_controls():
    """Display the control buttons for the lootbox simulator"""
    st.subheader("🎮 Controls")
    
    # Create a 3-column layout for controls
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        # Add number input for batch opening
        num_boxes = st.number_input(
            "Number of boxes to open:",
            min_value=1,
            max_value=1000,
            value=1,
            step=1,
            help="Enter the number of loot boxes you want to open at once"
        )
    
    with col2:
        # Open box button
        if st.button("🎁 Open Loot Box(es)", use_container_width=True):
            # Clear previous rewards if any
            st.session_state.last_rewards = []
            
            # Open the specified number of boxes
            progress_bar = st.progress(0)
            for i in range(num_boxes):
                rewards = st.session_state.loot_box.open_box()
                
                # Store only the last 10 rewards to avoid UI clutter
                if i >= num_boxes - 10:
                    st.session_state.last_rewards.extend(rewards)
                
                # Update progress bar
                progress_bar.progress((i + 1) / num_boxes)
            
            # Add a summary message
            if num_boxes > 1:
                summary = f"Opened {num_boxes} loot boxes! Showing the last {min(10, num_boxes)} boxes' rewards."
                st.session_state.summary_message = summary

    with col3:
        # Reset button
        if st.button("🔄 Reset Inventory", use_container_width=True, type="secondary"):
            st.session_state.loot_box = LootBox()
            st.session_state.last_rewards = None
            st.session_state.summary_message = None
            st.rerun()

def display_rewards():
    """Display the latest rewards if they exist"""
    if hasattr(st.session_state, 'summary_message') and st.session_state.summary_message:
        st.info(st.session_state.summary_message)
        
    if hasattr(st.session_state, 'last_rewards') and st.session_state.last_rewards:
        with st.expander("🎉 Latest Rewards", expanded=True):
            # Group rewards by type for better organization
            duplicates = []
            new_items = []
            currency = []
            
            for reward in st.session_state.last_rewards:
                if "Duplicate" in reward:
                    duplicates.append(reward)
                elif "New" in reward:
                    new_items.append(reward)
                else:
                    currency.append(reward)
            
            # Display new items first (they're most exciting)
            if new_items:
                st.markdown("### 🆕 New Items")
                for item in new_items:
                    st.success(item)
            
            # Display duplicates
            if duplicates:
                st.markdown("### 🔄 Duplicates")
                for item in duplicates:
                    st.warning(item)
            
            # Display currency
            if currency:
                st.markdown("### 💰 Currency")
                for item in currency:
                    st.info(item)

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
    st.subheader("📊 Drop Rates by Slot")
    
    slot_drop_rates = loot_box.get_slot_drop_rates()
    
    # Check if all slots have the same drop rates
    all_same = all(slot_drop_rates[0] == slot for slot in slot_drop_rates[1:])
    
    if all_same:
        # If all slots have the same drop rates, show a simplified view
        st.info("All slots currently have the same drop rates.")
        
        # Sort items by drop rate (descending)
        sorted_items = sorted(slot_drop_rates[0].items(), key=lambda x: x[1], reverse=True)
        
        for item, rate in sorted_items:
            # Skip items with 0% drop rate
            if rate == 0:
                continue
                
            st.progress(rate / 100)
            
            if item in loot_box.unique_items:
                total_items = loot_box.unique_items[item]["total"]
                st.caption(f"{item}: {rate}% (Unique Items: {total_items})")
            else:
                # Currency items
                value = loot_box.item_properties[item]["value"]
                st.caption(f"{item}: {rate}% (Value: {value})")
    else:
        # Show separate drop rates for each slot
        for slot_index, loot_table in enumerate(slot_drop_rates):
            st.markdown(f"#### Slot {slot_index+1}")
            
            # Sort items by drop rate (descending)
            sorted_items = sorted(loot_table.items(), key=lambda x: x[1], reverse=True)
            
            for item, rate in sorted_items:
                # Skip items with 0% drop rate
                if rate == 0:
                    continue
                    
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.progress(rate / 100)
                with col2:
                    st.write(f"{rate}%")
                    
                if item in loot_box.unique_items:
                    total_items = loot_box.unique_items[item]["total"]
                    st.caption(f"{item}: {rate}% (Unique Items: {total_items})")
                else:
                    # Currency items
                    value = loot_box.item_properties[item]["value"]
                    st.caption(f"{item}: {rate}% (Value: {value})")
            
            st.divider() 