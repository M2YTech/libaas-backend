"""
Outfit Recommendation Engine
Intelligently combines wardrobe items based on event type, user profile, and fashion rules
"""
from typing import List, Dict, Optional
import random


class OutfitRecommender:
    """Generate outfit combinations from user's wardrobe"""
    
    # Event-specific style preferences
    EVENT_STYLES = {
        "wedding": {
            "preferred_categories": ["Dresses & Lehengas", "Cultural / Special", "Tops & Kurtas"],
            "preferred_colors": ["red", "maroon", "gold", "pink", "purple", "emerald"],
            "preferred_styles": ["traditional", "ethnic", "formal"],
            "formality": "formal"
        },
        "mehndi": {
            "preferred_categories": ["Tops & Kurtas", "Dresses & Lehengas", "Cultural / Special"],
            "preferred_colors": ["yellow", "orange", "green", "pink", "multicolor"],
            "preferred_styles": ["ethnic", "traditional", "fusion"],
            "formality": "semi-formal"
        },
        "cultural": {
            "preferred_categories": ["Cultural / Special", "Dresses & Lehengas", "Tops & Kurtas"],
            "preferred_colors": ["multicolor", "red", "blue", "green", "gold"],
            "preferred_styles": ["ethnic", "traditional"],
            "formality": "formal"
        },
        "office": {
            "preferred_categories": ["Tops & Kurtas", "Bottoms & Shalwar"],
            "preferred_colors": ["black", "navy", "white", "gray", "beige", "blue"],
            "preferred_styles": ["formal", "western", "modern"],
            "formality": "formal"
        },
        "casual": {
            "preferred_categories": ["Tops & Kurtas", "Bottoms & Shalwar", "Dresses & Lehengas"],
            "preferred_colors": ["any"],
            "preferred_styles": ["casual", "western", "fusion", "modern"],
            "formality": "casual"
        },
        "party": {
            "preferred_categories": ["Dresses & Lehengas", "Tops & Kurtas"],
            "preferred_colors": ["black", "red", "gold", "silver", "purple", "emerald"],
            "preferred_styles": ["modern", "western", "fusion"],
            "formality": "semi-formal"
        },
        "formal": {
            "preferred_categories": ["Dresses & Lehengas", "Tops & Kurtas", "Cultural / Special"],
            "preferred_colors": ["black", "navy", "maroon", "emerald", "gold"],
            "preferred_styles": ["formal", "modern", "traditional"],
            "formality": "formal"
        }
    }
    
    def __init__(self):
        pass
    
    def generate_outfits(
        self,
        wardrobe_items: List[Dict],
        event_type: str,
        num_looks: int = 5,
        user_profile: Optional[Dict] = None
    ) -> List[Dict]:
        """
        Generate outfit combinations from wardrobe items
        
        Args:
            wardrobe_items: List of user's wardrobe items
            event_type: Type of event (wedding, casual, etc.)
            num_looks: Number of outfit combinations to generate
            user_profile: Optional user profile for personalization
            
        Returns:
            List of outfit dictionaries with items and metadata
        """
        if not wardrobe_items:
            return []
        
        event_prefs = self.EVENT_STYLES.get(event_type.lower(), self.EVENT_STYLES["casual"])
        
        # Filter items suitable for this event
        suitable_items = self._filter_suitable_items(wardrobe_items, event_prefs)
        
        if not suitable_items:
            # Fallback to all items if no suitable ones found
            suitable_items = wardrobe_items
        
        # Group items by category
        items_by_category = self._group_by_category(suitable_items)
        
        # Generate outfit combinations
        outfits = []
        max_attempts = num_looks * 3  # Try multiple times to get diverse looks
        attempts = 0
        
        while len(outfits) < num_looks and attempts < max_attempts:
            attempts += 1
            outfit = self._create_outfit_combination(
                items_by_category,
                event_prefs,
                user_profile
            )
            
            if outfit and not self._is_duplicate_outfit(outfit, outfits):
                # Calculate match score
                match_score = self._calculate_match_score(outfit, event_prefs, user_profile)
                outfit["match_score"] = match_score
                outfit["event_type"] = event_type
                outfits.append(outfit)
        
        # Sort by match score
        outfits.sort(key=lambda x: x["match_score"], reverse=True)
        
        return outfits[:num_looks]
    
    def _filter_suitable_items(self, items: List[Dict], event_prefs: Dict) -> List[Dict]:
        """Filter items suitable for the event"""
        suitable = []
        preferred_categories = event_prefs.get("preferred_categories", [])
        preferred_colors = event_prefs.get("preferred_colors", [])
        preferred_styles = event_prefs.get("preferred_styles", [])
        
        for item in items:
            category = item.get("category", "")
            color = item.get("color", "").lower()
            style = item.get("style", "").lower()
            
            # Check category match
            category_match = any(cat in category for cat in preferred_categories)
            
            # Check color match (if not "any")
            color_match = "any" in preferred_colors or any(
                pref_color in color for pref_color in preferred_colors
            )
            
            # Check style match
            style_match = any(pref_style in style for pref_style in preferred_styles)
            
            # Item is suitable if it matches at least one criteria strongly
            if category_match or (color_match and style_match):
                suitable.append(item)
        
        return suitable
    
    def _group_by_category(self, items: List[Dict]) -> Dict[str, List[Dict]]:
        """Group items by their category"""
        grouped = {}
        
        for item in items:
            category = item.get("category", "Uncategorized")
            if category not in grouped:
                grouped[category] = []
            grouped[category].append(item)
        
        return grouped
    
    def _create_outfit_combination(
        self,
        items_by_category: Dict[str, List[Dict]],
        event_prefs: Dict,
        user_profile: Optional[Dict]
    ) -> Optional[Dict]:
        """Create a single outfit combination"""
        outfit_items = []
        
        # Strategy: Pick one main garment + accessories
        # Priority: Dresses > Tops > Bottoms
        
        # Try to get a dress/lehenga first
        if "Dresses & Lehengas" in items_by_category and items_by_category["Dresses & Lehengas"]:
            main_item = random.choice(items_by_category["Dresses & Lehengas"])
            outfit_items.append(main_item)
            
            # Add dupatta if available
            if "Dupattas & Scarves" in items_by_category:
                dupattas = items_by_category["Dupattas & Scarves"]
                if dupattas:
                    dupatta = self._pick_matching_item(main_item, dupattas)
                    if dupatta:
                        outfit_items.append(dupatta)
        
        # Otherwise, try top + bottom combination
        elif "Tops & Kurtas" in items_by_category and items_by_category["Tops & Kurtas"]:
            top = random.choice(items_by_category["Tops & Kurtas"])
            outfit_items.append(top)
            
            # Try to add bottom
            if "Bottoms & Shalwar" in items_by_category:
                bottoms = items_by_category["Bottoms & Shalwar"]
                if bottoms:
                    bottom = self._pick_matching_item(top, bottoms)
                    if bottom:
                        outfit_items.append(bottom)
            
            # Try to add dupatta
            if "Dupattas & Scarves" in items_by_category:
                dupattas = items_by_category["Dupattas & Scarves"]
                if dupattas:
                    dupatta = self._pick_matching_item(top, dupattas)
                    if dupatta:
                        outfit_items.append(dupatta)
        
        # Add shoes if available (sometimes skip for variety)
        if "Shoes & Sandals" in items_by_category and random.random() > 0.2:
            shoes = items_by_category["Shoes & Sandals"]
            if shoes and outfit_items:
                shoe = self._pick_matching_item(outfit_items[0], shoes)
                if shoe:
                    outfit_items.append(shoe)
        
        # Add jewelry if available (vary the number to create different looks)
        if "Jewelry" in items_by_category:
            jewelry = items_by_category["Jewelry"]
            if jewelry:
                # Randomly pick 0-2 jewelry items for variety
                num_jewelry = random.randint(0, min(2, len(jewelry)))
                if num_jewelry > 0:
                    selected_jewelry = random.sample(jewelry, num_jewelry)
                    outfit_items.extend(selected_jewelry)
        
        # Add accessories/bags if available (sometimes skip for variety)
        if "Accessories & Bags" in items_by_category and random.random() > 0.3:
            accessories = items_by_category["Accessories & Bags"]
            if accessories:
                accessory = random.choice(accessories)
                outfit_items.append(accessory)
        
        if not outfit_items:
            return None
        
        return {
            "items": outfit_items,
            "primary_color": outfit_items[0].get("color", "unknown"),
            "style": outfit_items[0].get("style", "casual")
        }
    
    def _pick_matching_item(self, base_item: Dict, candidates: List[Dict]) -> Optional[Dict]:
        """Pick an item that matches well with the base item"""
        base_color = base_item.get("color", "").lower()
        base_style = base_item.get("style", "").lower()
        
        # Try to find complementary colors
        complementary_colors = {
            "red": ["gold", "cream", "white", "black"],
            "blue": ["white", "silver", "cream", "gold"],
            "green": ["gold", "cream", "white", "brown"],
            "yellow": ["white", "brown", "blue", "green"],
            "black": ["red", "white", "gold", "silver"],
            "white": ["any"],
            "gold": ["red", "green", "maroon", "black"],
            "pink": ["white", "gold", "silver", "cream"]
        }
        
        matching = []
        for candidate in candidates:
            candidate_color = candidate.get("color", "").lower()
            candidate_style = candidate.get("style", "").lower()
            
            # Check color compatibility
            if base_color in complementary_colors:
                if any(comp in candidate_color for comp in complementary_colors[base_color]) or "any" in complementary_colors[base_color]:
                    matching.append(candidate)
            elif candidate_color == base_color:  # Same color is always safe
                matching.append(candidate)
        
        if matching:
            return random.choice(matching)
        
        # Fallback to random if no perfect match
        return random.choice(candidates) if candidates else None
    
    def _is_duplicate_outfit(self, outfit: Dict, existing_outfits: List[Dict]) -> bool:
        """Check if this outfit is too similar to existing ones"""
        outfit_item_ids = set(item.get("id") for item in outfit["items"])
        
        for existing in existing_outfits:
            existing_ids = set(item.get("id") for item in existing["items"])
            
            # Check if outfits are identical (100% overlap)
            # This allows maximum variety - only reject exact duplicates
            if outfit_item_ids == existing_ids:
                return True
        
        return False
    
    def _calculate_match_score(
        self,
        outfit: Dict,
        event_prefs: Dict,
        user_profile: Optional[Dict]
    ) -> int:
        """Calculate how well this outfit matches the event and user"""
        score = 70  # Base score
        
        # Check event appropriateness
        preferred_colors = event_prefs.get("preferred_colors", [])
        preferred_styles = event_prefs.get("preferred_styles", [])
        
        outfit_color = outfit.get("primary_color", "").lower()
        outfit_style = outfit.get("style", "").lower()
        
        # Color match bonus
        if "any" in preferred_colors or any(color in outfit_color for color in preferred_colors):
            score += 10
        
        # Style match bonus
        if any(style in outfit_style for style in preferred_styles):
            score += 10
        
        # Completeness bonus (more items = better outfit)
        num_items = len(outfit.get("items", []))
        if num_items >= 4:
            score += 10
        elif num_items >= 3:
            score += 5
        
        # User profile matching (if available)
        if user_profile:
            # Future: Add personalization based on body shape, skin tone, etc.
            pass
        
        # Ensure score is within 70-100 range
        return min(100, max(70, score))


# Global instance
_outfit_recommender = None

def get_outfit_recommender() -> OutfitRecommender:
    """Get or create the outfit recommender instance"""
    global _outfit_recommender
    if _outfit_recommender is None:
        _outfit_recommender = OutfitRecommender()
    return _outfit_recommender

