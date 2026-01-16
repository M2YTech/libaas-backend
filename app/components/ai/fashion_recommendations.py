"""
Fashion Recommendation Engine
Generates personalized outfit recommendations based on user profile attributes.
"""

from typing import Dict, List, Any


# Body Shape Recommendations for FEMALE
FEMALE_BODY_SHAPE_RECOMMENDATIONS = {
    "hourglass": {
        "best_fits": ["Fitted dresses", "Wrap dresses", "High-waisted bottoms", "Belted outfits"],
        "best_styles": ["Defined waist", "V-necklines", "Bodycon fits", "Pencil skirts"],
        "avoid": ["Shapeless clothing", "Oversized tops", "Boxy silhouettes"],
        "tips": "Emphasize your balanced proportions with fitted styles that highlight your waist."
    },
    "pear": {
        "best_fits": ["A-line skirts", "Wide-leg pants", "Boat necks", "Statement tops"],
        "best_styles": ["Broader shoulders", "Detailed necklines", "Dark bottom colors", "Light top colors"],
        "avoid": ["Skinny jeans", "Tight bottoms", "Hip pockets", "Horizontal stripes on hips"],
        "tips": "Balance your silhouette by drawing attention to your upper body with detailed tops."
    },
    "rectangle": {
        "best_fits": ["Peplum tops", "Ruffled dresses", "Layered outfits", "Belted styles"],
        "best_styles": ["Create curves", "Textured fabrics", "Asymmetric cuts", "Color blocking"],
        "avoid": ["Straight cuts", "Column dresses", "Shapeless fits"],
        "tips": "Create the illusion of curves with structured pieces and strategic layering."
    },
    "inverted": {
        "best_fits": ["Wide-leg pants", "A-line skirts", "V-necks", "Bootcut jeans"],
        "best_styles": ["Dark top colors", "Detailed bottoms", "Lower necklines", "Structured skirts"],
        "avoid": ["Shoulder pads", "Boat necks", "Cap sleeves", "Skinny jeans"],
        "tips": "Balance broad shoulders by adding volume to your lower body and softening the neckline."
    },
    "round": {
        "best_fits": ["Empire waist", "Wrap dresses", "V-necks", "Vertical lines"],
        "best_styles": ["Elongating cuts", "Monochrome outfits", "Structured fabrics", "A-line silhouettes"],
        "avoid": ["Tight fits", "Horizontal stripes", "Bulky fabrics", "High necklines"],
        "tips": "Choose styles that create vertical lines and elongate your silhouette."
    },
    "athletic": {
        "best_fits": ["Peplum tops", "Ruffled dresses", "Cinched waist", "Soft fabrics"],
        "best_styles": ["Feminine details", "Curved lines", "Layered looks", "Textured pieces"],
        "avoid": ["Boxy shapes", "Stiff fabrics", "Straight cuts"],
        "tips": "Add curves and softness with ruffles, draping, and feminine details."
    }
}

# Body Shape Recommendations for MALE
MALE_BODY_SHAPE_RECOMMENDATIONS = {
    "athletic": {
        "best_fits": ["Fitted shirts", "Slim-fit trousers", "Structured blazers", "Tapered pants"],
        "best_styles": ["Defined shoulders", "Fitted waist", "Straight cuts", "Modern silhouettes"],
        "avoid": ["Baggy clothes", "Oversized shirts", "Loose-fitting pants"],
        "tips": "Showcase your athletic build with well-fitted, structured pieces."
    },
    "rectangle": {
        "best_fits": ["Layered outfits", "Textured fabrics", "Horizontal stripes", "Casual blazers"],
        "best_styles": ["Add dimension", "Color blocking", "Patterned shirts", "Contrast layers"],
        "avoid": ["Tight fits", "Vertical stripes", "Plain single colors"],
        "tips": "Create visual interest with layers and patterns to add dimension."
    },
    "inverted": {
        "best_fits": ["Straight-leg pants", "Dark-colored shirts", "V-neck t-shirts", "Relaxed-fit bottoms"],
        "best_styles": ["Balance proportions", "Lighter bottom colors", "Slim-fit pants", "Avoid tight tops"],
        "avoid": ["Shoulder-heavy jackets", "Tight shirts", "Skinny jeans", "Wide shoulder cuts"],
        "tips": "Balance broad shoulders with relaxed-fit pants and avoid emphasizing the upper body."
    },
    "round": {
        "best_fits": ["Vertical stripes", "Dark colors", "Structured jackets", "Long coats"],
        "best_styles": ["Elongating cuts", "Monochrome outfits", "V-necks", "Single-breasted suits"],
        "avoid": ["Horizontal stripes", "Tight clothes", "Double-breasted jackets", "Bulky layers"],
        "tips": "Choose vertical lines and darker colors to create a slimmer, taller appearance."
    },
    "pear": {
        "best_fits": ["Structured jackets", "Broader shoulder cuts", "Tapered pants", "Fitted shirts"],
        "best_styles": ["Emphasize upper body", "Light-colored tops", "Dark bottoms", "Defined shoulders"],
        "avoid": ["Baggy tops", "Tight pants", "Large pockets on pants", "Light-colored bottoms"],
        "tips": "Draw attention upward with structured tops and keep bottoms streamlined."
    },
    "hourglass": {
        "best_fits": ["Fitted shirts", "Tailored suits", "Slim-fit pants", "Structured jackets"],
        "best_styles": ["Show your shape", "Well-fitted pieces", "Modern cuts", "Proportioned looks"],
        "avoid": ["Overly baggy clothes", "Boxy fits", "Too tight clothing"],
        "tips": "Maintain balance with well-fitted, tailored pieces that show your proportions."
    }
}

# Skin Tone Color Recommendations
SKIN_TONE_COLORS = {
    "fair": {
        "best_colors": ["Pastels", "Soft pink", "Lavender", "Baby blue", "Mint green", "Light gray"],
        "complementary": ["Navy", "Burgundy", "Forest green", "Royal blue"],
        "avoid": ["Neon colors", "Very dark colors without contrast", "Yellow-based whites"],
        "jewelry": "Silver, white gold, platinum"
    },
    "warm": {
        "best_colors": ["Earth tones", "Coral", "Peach", "Golden yellow", "Olive green", "Rust"],
        "complementary": ["Brown", "Camel", "Terracotta", "Warm red", "Mustard"],
        "avoid": ["Cool pinks", "Icy blue", "Pure black", "Stark white"],
        "jewelry": "Gold, bronze, copper"
    },
    "olive": {
        "best_colors": ["Jewel tones", "Emerald", "Sapphire", "Amethyst", "Rich purple", "Teal"],
        "complementary": ["Burgundy", "Navy", "Forest green", "Deep red"],
        "avoid": ["Pale colors", "Washed-out pastels", "Orange"],
        "jewelry": "Gold, rose gold"
    },
    "tan": {
        "best_colors": ["Warm neutrals", "Coral", "Turquoise", "Burnt orange", "Golden yellow", "Red"],
        "complementary": ["White", "Cream", "Chocolate brown", "Bright pink"],
        "avoid": ["Very pale colors", "Neon yellow", "Muddy browns"],
        "jewelry": "Gold, brass, copper"
    },
    "deep": {
        "best_colors": ["Bold colors", "Bright white", "Electric blue", "Fuchsia", "Emerald", "Gold"],
        "complementary": ["Rich jewel tones", "Pure black", "Vibrant red", "Royal purple"],
        "avoid": ["Dusty pastels", "Washed-out colors", "Beige"],
        "jewelry": "Gold, silver (both work well)"
    }
}

# Height-based Recommendations
HEIGHT_RECOMMENDATIONS = {
    "petite": {  # Under 160 cm
        "best_styles": ["Cropped pants", "High-waisted bottoms", "Vertical lines", "Fitted silhouettes"],
        "best_lengths": ["Above knee", "Midi length", "Cropped jackets"],
        "avoid": ["Maxi dresses", "Oversized clothing", "Wide belts", "Long coats"],
        "tips": "Create the illusion of height with high-waisted pieces and monochromatic outfits."
    },
    "average": {  # 160-170 cm
        "best_styles": ["Most styles work", "Experiment freely", "Balanced proportions"],
        "best_lengths": ["Knee-length", "Midi", "Ankle-length"],
        "avoid": ["Extreme proportions"],
        "tips": "You can pull off most styles - experiment with different trends and fits."
    },
    "tall": {  # Over 170 cm
        "best_styles": ["Maxi dresses", "Wide-leg pants", "Long coats", "Statement pieces"],
        "best_lengths": ["Floor-length", "Full-length pants", "Long sleeves"],
        "avoid": ["Very short hemlines", "Cropped styles", "Small prints"],
        "tips": "Embrace your height with flowing silhouettes and bold patterns."
    }
}

# Gender-specific Recommendations
GENDER_RECOMMENDATIONS = {
    "female": {
        "categories": ["Dresses", "Skirts", "Blouses", "Tops", "Pants", "Ethnic wear"],
        "focus": ["Silhouette", "Waist definition", "Neckline", "Color harmony"]
    },
    "male": {
        "categories": ["Shirts", "Pants", "Suits", "Casual wear", "Ethnic wear"],
        "focus": ["Fit at shoulders", "Sleeve length", "Trouser break", "Color coordination"]
    },
    "other": {
        "categories": ["Universal pieces", "Unisex clothing", "Custom fits", "Androgynous styles"],
        "focus": ["Personal comfort", "Self-expression", "Versatile pieces", "Quality fabrics"]
    }
}


def get_height_category(height: str) -> str:
    """Categorize height as petite, average, or tall."""
    try:
        height_cm = int(height)
        if height_cm < 160:
            return "petite"
        elif height_cm <= 170:
            return "average"
        else:
            return "tall"
    except (ValueError, TypeError):
        return "average"


def generate_recommendations(
    gender: str,
    body_shape: str = None,
    skin_tone: str = None,
    height: str = None,
    country: str = None
) -> Dict[str, Any]:
    """
    Generate personalized fashion recommendations based on user profile.
    
    Args:
        gender: User's gender
        body_shape: User's body shape
        skin_tone: User's skin tone
        height: User's height in cm
        country: User's country
    
    Returns:
        Dictionary containing personalized recommendations
    """
    recommendations = {
        "summary": "",
        "best_fits": [],
        "best_colors": [],
        "complementary_colors": [],
        "styles_to_try": [],
        "avoid": [],
        "jewelry_metals": "",
        "pro_tips": []
    }
    
    # Body shape recommendations (gender-specific)
    if body_shape and gender:
        body_shape_lower = body_shape.lower()
        gender_lower = gender.lower()
        
        # Select appropriate recommendations based on gender
        if gender_lower == "male" and body_shape_lower in MALE_BODY_SHAPE_RECOMMENDATIONS:
            shape_rec = MALE_BODY_SHAPE_RECOMMENDATIONS[body_shape_lower]
            recommendations["best_fits"] = shape_rec["best_fits"]
            recommendations["styles_to_try"].extend(shape_rec["best_styles"])
            recommendations["avoid"].extend(shape_rec["avoid"])
            recommendations["pro_tips"].append(shape_rec["tips"])
        elif gender_lower == "female" and body_shape_lower in FEMALE_BODY_SHAPE_RECOMMENDATIONS:
            shape_rec = FEMALE_BODY_SHAPE_RECOMMENDATIONS[body_shape_lower]
            recommendations["best_fits"] = shape_rec["best_fits"]
            recommendations["styles_to_try"].extend(shape_rec["best_styles"])
            recommendations["avoid"].extend(shape_rec["avoid"])
            recommendations["pro_tips"].append(shape_rec["tips"])
        elif gender_lower == "other":
            # For non-binary/other, provide neutral recommendations
            if body_shape_lower in MALE_BODY_SHAPE_RECOMMENDATIONS:
                male_rec = MALE_BODY_SHAPE_RECOMMENDATIONS[body_shape_lower]
                female_rec = FEMALE_BODY_SHAPE_RECOMMENDATIONS.get(body_shape_lower, {})
                # Combine both recommendations
                recommendations["best_fits"] = male_rec.get("best_fits", [])[:2] + female_rec.get("best_fits", [])[:2]
                recommendations["styles_to_try"].extend(male_rec.get("best_styles", [])[:2])
                recommendations["pro_tips"].append("Choose styles that make you feel confident and comfortable.")
    
    # Skin tone color recommendations
    if skin_tone and skin_tone.lower() in SKIN_TONE_COLORS:
        tone_rec = SKIN_TONE_COLORS[skin_tone.lower()]
        recommendations["best_colors"] = tone_rec["best_colors"]
        recommendations["complementary_colors"] = tone_rec["complementary"]
        recommendations["avoid"].extend(tone_rec["avoid"])
        recommendations["jewelry_metals"] = tone_rec["jewelry"]
    
    # Height-based recommendations
    if height:
        height_category = get_height_category(height)
        height_rec = HEIGHT_RECOMMENDATIONS[height_category]
        recommendations["styles_to_try"].extend(height_rec["best_styles"])
        recommendations["avoid"].extend(height_rec["avoid"])
        recommendations["pro_tips"].append(height_rec["tips"])
    
    # Gender-specific focus
    if gender and gender.lower() in GENDER_RECOMMENDATIONS:
        gender_rec = GENDER_RECOMMENDATIONS[gender.lower()]
        # Add gender-specific summary
        recommendations["focus_areas"] = gender_rec["focus"]
    
    # Generate summary (gender-aware)
    summary_parts = []
    if body_shape:
        if gender and gender.lower() == "male":
            summary_parts.append(f"Your {body_shape} build suits modern, structured styles")
        else:
            summary_parts.append(f"Your {body_shape} shape is beautifully balanced")
    if skin_tone:
        summary_parts.append(f"your {skin_tone} skin tone pairs well with rich, complementary colors")
    if height:
        height_cat = get_height_category(height)
        summary_parts.append(f"your {height_cat} height allows for versatile styling options")
    
    recommendations["summary"] = ". ".join(summary_parts).capitalize() + "." if summary_parts else "Complete your profile for personalized recommendations."
    
    # Remove duplicates from avoid list
    recommendations["avoid"] = list(set(recommendations["avoid"]))
    recommendations["styles_to_try"] = list(set(recommendations["styles_to_try"]))
    
    return recommendations

