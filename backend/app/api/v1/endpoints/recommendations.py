"""
Recommendations and condition info endpoints
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.db.models import ConditionInfo
from app.db.schemas import ConditionInfoResponse
from app.config import settings

router = APIRouter()


@router.get("/conditions", response_model=List[str])
async def get_all_conditions():
    """
    Get list of all detectable skin conditions
    """
    return settings.CONDITIONS


@router.get("/conditions/{condition_name}", response_model=ConditionInfoResponse)
async def get_condition_info(
    condition_name: str,
    db: Session = Depends(get_db)
):
    """
    Get detailed information about a specific condition
    
    - **condition_name**: Name of the condition
    """
    # Check if condition exists in our list
    if condition_name not in settings.CONDITIONS:
        raise HTTPException(
            status_code=404,
            detail=f"Condition '{condition_name}' not found"
        )
    
    # Try to get from database
    condition_info = db.query(ConditionInfo).filter(
        ConditionInfo.condition_name == condition_name
    ).first()
    
    if condition_info:
        return condition_info
    
    # Return default info if not in database
    return get_default_condition_info(condition_name)


def get_default_condition_info(condition_name: str) -> dict:
    """Get default condition information"""
    
    default_info = {
        "acne": {
            "display_name": "Acne",
            "description": "Acne is a skin condition that occurs when hair follicles become clogged with oil and dead skin cells, causing whiteheads, blackheads, or pimples.",
            "causes": [
                "Excess oil production",
                "Clogged hair follicles",
                "Bacteria",
                "Hormonal changes",
                "Certain medications",
                "Diet"
            ],
            "symptoms": [
                "Whiteheads",
                "Blackheads",
                "Pimples",
                "Cysts",
                "Inflammation",
                "Redness"
            ],
            "immediate_actions": [
                "Cleanse face gently twice daily",
                "Avoid touching or picking",
                "Use oil-free products"
            ],
            "skincare_tips": [
                "Use non-comedogenic products",
                "Apply benzoyl peroxide or salicylic acid",
                "Moisturize with lightweight formula"
            ],
            "lifestyle_tips": [
                "Change pillowcases regularly",
                "Reduce stress",
                "Stay hydrated",
                "Eat balanced diet"
            ],
            "product_categories": [
                "Gentle cleanser",
                "Salicylic acid treatment",
                "Oil-free moisturizer",
                "Non-comedogenic sunscreen"
            ],
            "when_to_see_doctor": "If acne is severe, cystic, painful, or not improving after 8-12 weeks"
        },
        "redness": {
            "display_name": "Redness/Inflammation",
            "description": "Skin redness is a common condition characterized by visible blood vessels, flushing, or irritation.",
            "causes": [
                "Sensitive skin",
                "Rosacea",
                "Allergic reactions",
                "Harsh products",
                "Environmental factors",
                "Sun exposure"
            ],
            "symptoms": [
                "Visible redness",
                "Flushing",
                "Burning sensation",
                "Irritation",
                "Visible blood vessels"
            ],
            "immediate_actions": [
                "Apply cool compress",
                "Stop using harsh products",
                "Use gentle, fragrance-free products"
            ],
            "skincare_tips": [
                "Use soothing ingredients (centella, niacinamide)",
                "Apply barrier repair creams",
                "Use mineral sunscreen"
            ],
            "lifestyle_tips": [
                "Avoid hot water",
                "Reduce stress",
                "Avoid trigger foods (spicy, alcohol)",
                "Protect from extreme temperatures"
            ],
            "product_categories": [
                "Gentle cleanser",
                "Centella serum",
                "Barrier repair cream",
                "Mineral sunscreen"
            ],
            "when_to_see_doctor": "If redness is persistent, spreading, or accompanied by pain"
        },
        "dryness": {
            "display_name": "Dry Skin",
            "description": "Dry skin lacks moisture and can feel tight, rough, or flaky.",
            "causes": [
                "Low humidity",
                "Hot showers",
                "Harsh soaps",
                "Aging",
                "Climate",
                "Dehydration"
            ],
            "symptoms": [
                "Tightness",
                "Flaking",
                "Rough texture",
                "Itching",
                "Fine lines",
                "Dullness"
            ],
            "immediate_actions": [
                "Apply rich moisturizer",
                "Use humidifier",
                "Drink more water"
            ],
            "skincare_tips": [
                "Use creamy cleansers",
                "Apply hyaluronic acid",
                "Use face oils",
                "Apply thick night cream"
            ],
            "lifestyle_tips": [
                "Limit shower time",
                "Use lukewarm water",
                "Increase water intake",
                "Use humidifier at night"
            ],
            "product_categories": [
                "Creamy cleanser",
                "Hyaluronic acid serum",
                "Face oil",
                "Rich moisturizer",
                "Sleeping mask"
            ],
            "when_to_see_doctor": "If dryness causes cracking, bleeding, or doesn't improve"
        },
        "oiliness": {
            "display_name": "Oily Skin",
            "description": "Oily skin produces excess sebum, leading to a shiny appearance and potential breakouts.",
            "causes": [
                "Genetics",
                "Hormonal changes",
                "Humidity",
                "Over-cleansing",
                "Wrong products",
                "Diet"
            ],
            "symptoms": [
                "Shiny appearance",
                "Enlarged pores",
                "Frequent breakouts",
                "Thick skin texture"
            ],
            "immediate_actions": [
                "Use oil-control cleanser",
                "Use blotting papers",
                "Avoid over-cleansing"
            ],
            "skincare_tips": [
                "Use lightweight products",
                "Apply niacinamide",
                "Use clay masks weekly",
                "Choose oil-free formulas"
            ],
            "lifestyle_tips": [
                "Balanced diet",
                "Don't touch face",
                "Clean phone screen",
                "Change pillowcases"
            ],
            "product_categories": [
                "Foaming cleanser",
                "Niacinamide serum",
                "Oil-free moisturizer",
                "Clay mask",
                "Matte sunscreen"
            ],
            "when_to_see_doctor": "If accompanied by severe acne or hormonal issues"
        },
        "aging_signs": {
            "display_name": "Aging Signs",
            "description": "Visible signs of skin aging including wrinkles, fine lines, and loss of elasticity.",
            "causes": [
                "Natural aging",
                "Sun exposure",
                "Smoking",
                "Repetitive facial expressions",
                "Poor sleep",
                "Stress"
            ],
            "symptoms": [
                "Fine lines",
                "Wrinkles",
                "Loss of elasticity",
                "Sagging",
                "Age spots",
                "Dullness"
            ],
            "immediate_actions": [
                "Apply SPF 50+ daily",
                "Start using retinol",
                "Use antioxidant serum"
            ],
            "skincare_tips": [
                "Use retinol/retinoid",
                "Apply vitamin C",
                "Use peptide creams",
                "Apply eye cream"
            ],
            "lifestyle_tips": [
                "Sleep on back",
                "Get adequate sleep",
                "Eat antioxidant-rich foods",
                "Stay hydrated",
                "Quit smoking"
            ],
            "product_categories": [
                "Retinol serum",
                "Vitamin C serum",
                "Peptide cream",
                "Eye cream",
                "SPF 50+"
            ],
            "when_to_see_doctor": "Consider professional treatments (laser, fillers) for advanced signs"
        },
        "dark_spots": {
            "display_name": "Dark Spots/Hyperpigmentation",
            "description": "Dark spots or patches of skin caused by excess melanin production.",
            "causes": [
                "Sun exposure",
                "Acne scarring",
                "Hormonal changes",
                "Aging",
                "Inflammation",
                "Certain medications"
            ],
            "symptoms": [
                "Brown or dark patches",
                "Uneven skin tone",
                "Post-acne marks",
                "Melasma"
            ],
            "immediate_actions": [
                "Apply SPF religiously",
                "Use brightening serum",
                "Avoid sun exposure"
            ],
            "skincare_tips": [
                "Use vitamin C",
                "Apply niacinamide",
                "Use alpha arbutin",
                "Try kojic acid"
            ],
            "lifestyle_tips": [
                "Wear hat and sunglasses",
                "Seek shade",
                "Don't pick at skin",
                "Reapply sunscreen"
            ],
            "product_categories": [
                "Vitamin C serum",
                "Niacinamide",
                "Alpha arbutin",
                "SPF 50+",
                "Brightening mask"
            ],
            "when_to_see_doctor": "If spots are growing, changing shape, or not fading after 3 months"
        },
        "texture_issues": {
            "display_name": "Texture Issues",
            "description": "Uneven skin texture characterized by bumps, roughness, or large pores.",
            "causes": [
                "Dead skin buildup",
                "Clogged pores",
                "Sun damage",
                "Aging",
                "Genetics",
                "Lack of exfoliation"
            ],
            "symptoms": [
                "Rough texture",
                "Bumps",
                "Enlarged pores",
                "Uneven surface",
                "Dullness"
            ],
            "immediate_actions": [
                "Start gentle exfoliation",
                "Hydrate skin",
                "Use chemical exfoliants"
            ],
            "skincare_tips": [
                "Use AHA/BHA",
                "Apply retinol",
                "Use hydrating products",
                "Exfoliate 2-3x weekly"
            ],
            "lifestyle_tips": [
                "Don't over-exfoliate",
                "Stay hydrated",
                "Get enough sleep",
                "Eat balanced diet"
            ],
            "product_categories": [
                "AHA toner",
                "BHA serum",
                "Retinol",
                "Hydrating essence",
                "Chemical exfoliant"
            ],
            "when_to_see_doctor": "If texture is severe or accompanied by persistent bumps"
        },
        "healthy": {
            "display_name": "Healthy Skin",
            "description": "Your skin appears healthy with no major concerns detected.",
            "causes": [
                "Good skincare routine",
                "Healthy lifestyle",
                "Proper hydration",
                "Balanced diet",
                "Sun protection"
            ],
            "symptoms": [
                "Even tone",
                "Smooth texture",
                "Good hydration",
                "Radiance",
                "No major concerns"
            ],
            "immediate_actions": [
                "Maintain current routine",
                "Continue sun protection"
            ],
            "skincare_tips": [
                "Continue gentle cleansing",
                "Use antioxidants",
                "Maintain moisturization",
                "Keep using SPF"
            ],
            "lifestyle_tips": [
                "Maintain healthy diet",
                "Stay hydrated",
                "Get adequate sleep",
                "Manage stress"
            ],
            "product_categories": [
                "Gentle cleanser",
                "Antioxidant serum",
                "Moisturizer",
                "SPF 30+"
            ],
            "when_to_see_doctor": None
        }
    }
    
    info = default_info.get(condition_name, {})
    info["condition_name"] = condition_name
    
    return info