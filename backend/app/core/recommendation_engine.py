"""
Recommendation Engine for personalized skincare advice
"""

from typing import Dict, List
from app.config import settings


class RecommendationEngine:
    """Generate personalized recommendations based on skin analysis"""
    
    # Recommendation database
    CONDITION_TREATMENTS = {
        "acne": {
            "immediate_actions": [
                {
                    "title": "Gentle Cleansing",
                    "description": "Wash face twice daily with a gentle, non-comedogenic cleanser",
                    "priority": "high"
                },
                {
                    "title": "Avoid Touching",
                    "description": "Avoid touching or picking at acne to prevent scarring",
                    "priority": "high"
                },
                {
                    "title": "Spot Treatment",
                    "description": "Apply benzoyl peroxide or salicylic acid spot treatment",
                    "priority": "medium"
                }
            ],
            "skincare_routine": {
                "morning": [
                    "Gentle cleanser",
                    "Oil-free moisturizer",
                    "Non-comedogenic sunscreen SPF 30+"
                ],
                "evening": [
                    "Gentle cleanser",
                    "Salicylic acid or benzoyl peroxide treatment",
                    "Light, oil-free moisturizer"
                ]
            },
            "lifestyle_tips": [
                {
                    "title": "Change Pillowcases",
                    "description": "Change pillowcases every 2-3 days to reduce bacteria",
                    "priority": "medium"
                },
                {
                    "title": "Stay Hydrated",
                    "description": "Drink at least 8 glasses of water daily",
                    "priority": "medium"
                },
                {
                    "title": "Reduce Dairy",
                    "description": "Consider reducing dairy intake as it may trigger acne",
                    "priority": "low"
                }
            ],
            "product_categories": [
                "Salicylic acid cleanser",
                "Benzoyl peroxide spot treatment",
                "Oil-free moisturizer",
                "Non-comedogenic sunscreen"
            ],
            "when_to_see_doctor": "If acne is severe, cystic, or not improving after 8-12 weeks of treatment"
        },
        "redness": {
            "immediate_actions": [
                {
                    "title": "Cool Compress",
                    "description": "Apply cool compress to reduce inflammation",
                    "priority": "high"
                },
                {
                    "title": "Avoid Irritants",
                    "description": "Stop using harsh products, fragrances, or alcohol-based toners",
                    "priority": "high"
                }
            ],
            "skincare_routine": {
                "morning": [
                    "Gentle, fragrance-free cleanser",
                    "Soothing serum with niacinamide or centella",
                    "Gentle moisturizer",
                    "Mineral sunscreen"
                ],
                "evening": [
                    "Gentle cleanser",
                    "Calming treatment",
                    "Rich, barrier-repair moisturizer"
                ]
            },
            "lifestyle_tips": [
                {
                    "title": "Avoid Hot Water",
                    "description": "Use lukewarm water for washing face",
                    "priority": "high"
                },
                {
                    "title": "Reduce Stress",
                    "description": "Practice stress management techniques",
                    "priority": "medium"
                }
            ],
            "product_categories": [
                "Gentle cleanser",
                "Niacinamide serum",
                "Centella asiatica products",
                "Barrier repair cream"
            ],
            "when_to_see_doctor": "If redness persists, spreads, or is accompanied by pain or burning"
        },
        "dryness": {
            "immediate_actions": [
                {
                    "title": "Intense Hydration",
                    "description": "Apply a rich moisturizer immediately after cleansing",
                    "priority": "high"
                },
                {
                    "title": "Humidifier",
                    "description": "Use a humidifier in your room, especially at night",
                    "priority": "medium"
                }
            ],
            "skincare_routine": {
                "morning": [
                    "Creamy, hydrating cleanser",
                    "Hyaluronic acid serum",
                    "Rich moisturizer",
                    "Hydrating sunscreen"
                ],
                "evening": [
                    "Creamy cleanser or cleansing balm",
                    "Hydrating toner/essence",
                    "Face oil",
                    "Thick night cream or sleeping mask"
                ]
            },
            "lifestyle_tips": [
                {
                    "title": "Drink Water",
                    "description": "Increase water intake to 10+ glasses daily",
                    "priority": "high"
                },
                {
                    "title": "Avoid Long Hot Showers",
                    "description": "Limit shower time and use lukewarm water",
                    "priority": "medium"
                }
            ],
            "product_categories": [
                "Hyaluronic acid serum",
                "Ceramide moisturizer",
                "Face oils",
                "Sleeping masks"
            ],
            "when_to_see_doctor": "If dryness is severe, causes cracking, or doesn't improve with moisturization"
        },
        "oiliness": {
            "immediate_actions": [
                {
                    "title": "Oil-Control Cleanser",
                    "description": "Use a gentle foaming cleanser for oily skin",
                    "priority": "high"
                },
                {
                    "title": "Blotting Papers",
                    "description": "Use throughout the day to absorb excess oil",
                    "priority": "medium"
                }
            ],
            "skincare_routine": {
                "morning": [
                    "Foaming cleanser",
                    "Oil-controlling toner",
                    "Lightweight, oil-free moisturizer",
                    "Matte sunscreen"
                ],
                "evening": [
                    "Double cleanse (oil cleanser then foaming)",
                    "Niacinamide serum",
                    "Light gel moisturizer"
                ]
            },
            "lifestyle_tips": [
                {
                    "title": "Balanced Diet",
                    "description": "Reduce greasy, fried foods",
                    "priority": "medium"
                },
                {
                    "title": "Don't Over-Cleanse",
                    "description": "Cleanse only twice daily to avoid overproduction",
                    "priority": "high"
                }
            ],
            "product_categories": [
                "Foaming cleanser",
                "Niacinamide serum",
                "Oil-free moisturizer",
                "Clay masks (weekly)"
            ],
            "when_to_see_doctor": "If oiliness is severe or accompanied by persistent acne"
        },
        "aging_signs": {
            "immediate_actions": [
                {
                    "title": "Sun Protection",
                    "description": "Apply SPF 50+ daily, even indoors",
                    "priority": "high"
                },
                {
                    "title": "Retinol Introduction",
                    "description": "Start using retinol 2-3 times per week at night",
                    "priority": "high"
                }
            ],
            "skincare_routine": {
                "morning": [
                    "Gentle cleanser",
                    "Vitamin C serum",
                    "Peptide moisturizer",
                    "Broad-spectrum SPF 50+"
                ],
                "evening": [
                    "Gentle cleanser",
                    "Retinol or retinoid",
                    "Rich anti-aging cream",
                    "Eye cream"
                ]
            },
            "lifestyle_tips": [
                {
                    "title": "Sleep Position",
                    "description": "Sleep on your back to prevent sleep wrinkles",
                    "priority": "medium"
                },
                {
                    "title": "Antioxidant Diet",
                    "description": "Eat foods rich in antioxidants (berries, green tea)",
                    "priority": "medium"
                },
                {
                    "title": "Adequate Sleep",
                    "description": "Get 7-9 hours of quality sleep nightly",
                    "priority": "high"
                }
            ],
            "product_categories": [
                "Retinol serum",
                "Vitamin C serum",
                "Peptide creams",
                "SPF 50+ sunscreen",
                "Eye cream"
            ],
            "when_to_see_doctor": "Consider professional treatments like laser or injectables for advanced signs"
        },
        "dark_spots": {
            "immediate_actions": [
                {
                    "title": "Sun Protection",
                    "description": "Strict sun protection to prevent darkening",
                    "priority": "high"
                },
                {
                    "title": "Brightening Serum",
                    "description": "Use vitamin C or niacinamide serum daily",
                    "priority": "high"
                }
            ],
            "skincare_routine": {
                "morning": [
                    "Gentle cleanser",
                    "Vitamin C serum",
                    "Niacinamide moisturizer",
                    "SPF 50+ sunscreen"
                ],
                "evening": [
                    "Gentle cleanser",
                    "Alpha arbutin or kojic acid serum",
                    "Moisturizer",
                    "Spot treatment if needed"
                ]
            },
            "lifestyle_tips": [
                {
                    "title": "Hat and Sunglasses",
                    "description": "Wear protective accessories when outdoors",
                    "priority": "high"
                },
                {
                    "title": "Avoid Picking",
                    "description": "Don't pick at skin to prevent post-inflammatory hyperpigmentation",
                    "priority": "high"
                }
            ],
            "product_categories": [
                "Vitamin C serum",
                "Niacinamide",
                "Alpha arbutin",
                "Kojic acid",
                "SPF 50+"
            ],
            "when_to_see_doctor": "If spots are growing, changing, or not fading after 3 months"
        },
        "texture_issues": {
            "immediate_actions": [
                {
                    "title": "Gentle Exfoliation",
                    "description": "Use chemical exfoliant (AHA/BHA) 2-3x weekly",
                    "priority": "high"
                },
                {
                    "title": "Hydration",
                    "description": "Keep skin well-moisturized",
                    "priority": "medium"
                }
            ],
            "skincare_routine": {
                "morning": [
                    "Gentle cleanser",
                    "Hydrating toner",
                    "Moisturizer",
                    "Sunscreen"
                ],
                "evening": [
                    "Gentle cleanser",
                    "AHA/BHA toner (alternate nights)",
                    "Serum",
                    "Moisturizer"
                ]
            },
            "lifestyle_tips": [
                {
                    "title": "Avoid Over-Exfoliation",
                    "description": "Don't exfoliate more than 3x per week",
                    "priority": "high"
                }
            ],
            "product_categories": [
                "AHA toner (glycolic/lactic acid)",
                "BHA serum (salicylic acid)",
                "Retinol",
                "Hydrating essences"
            ],
            "when_to_see_doctor": "If texture is severe or accompanied by bumps or rashes"
        },
        "healthy": {
            "immediate_actions": [
                {
                    "title": "Maintain Routine",
                    "description": "Continue your current skincare routine",
                    "priority": "medium"
                }
            ],
            "skincare_routine": {
                "morning": [
                    "Gentle cleanser",
                    "Antioxidant serum",
                    "Moisturizer",
                    "SPF 30+"
                ],
                "evening": [
                    "Gentle cleanser",
                    "Treatment (optional)",
                    "Moisturizer"
                ]
            },
            "lifestyle_tips": [
                {
                    "title": "Prevention",
                    "description": "Focus on prevention with SPF and antioxidants",
                    "priority": "high"
                }
            ],
            "product_categories": [
                "Gentle cleanser",
                "Antioxidant serum",
                "Moisturizer",
                "Sunscreen"
            ],
            "when_to_see_doctor": None
        }
    }
    
    def generate_recommendations(self, analysis_results: Dict) -> Dict:
        """
        Generate personalized recommendations
        
        Args:
            analysis_results: Results from ML analysis
        
        Returns:
            Recommendations dictionary
        """
        detected_conditions = analysis_results.get("detected_conditions", [])
        
        if not detected_conditions:
            # If no issues, return healthy skin recommendations
            return self._format_recommendations(["healthy"])
        
        # Get top 2-3 conditions
        top_conditions = [
            cond["condition"] for cond in detected_conditions[:3]
        ]
        
        return self._format_recommendations(top_conditions)
    
    def _format_recommendations(self, conditions: List[str]) -> Dict:
        """Format recommendations from multiple conditions"""
        
        all_immediate = []
        all_skincare = {"morning": set(), "evening": set()}
        all_lifestyle = []
        all_products = set()
        doctor_needed = []
        
        for condition in conditions:
            if condition not in self.CONDITION_TREATMENTS:
                continue
            
            treatment = self.CONDITION_TREATMENTS[condition]
            
            # Immediate actions
            all_immediate.extend(treatment["immediate_actions"])
            
            # Skincare routine
            all_skincare["morning"].update(treatment["skincare_routine"]["morning"])
            all_skincare["evening"].update(treatment["skincare_routine"]["evening"])
            
            # Lifestyle tips
            all_lifestyle.extend(treatment["lifestyle_tips"])
            
            # Products
            all_products.update(treatment["product_categories"])
            
            # Doctor recommendation
            if treatment["when_to_see_doctor"]:
                doctor_needed.append(treatment["when_to_see_doctor"])
        
        # Remove duplicates and prioritize
        unique_immediate = self._deduplicate_recommendations(all_immediate)
        unique_lifestyle = self._deduplicate_recommendations(all_lifestyle)
        
        return {
            "immediate_actions": unique_immediate[:5],  # Top 5
            "skincare_routine": {
                "morning": list(all_skincare["morning"]),
                "evening": list(all_skincare["evening"])
            },
            "lifestyle_tips": unique_lifestyle[:5],  # Top 5
            "product_categories": list(all_products),
            "when_to_see_doctor": " OR ".join(doctor_needed) if doctor_needed else None
        }
    
    def _deduplicate_recommendations(self, recommendations: List[Dict]) -> List[Dict]:
        """Remove duplicate recommendations, keeping highest priority"""
        seen = {}
        
        for rec in recommendations:
            title = rec["title"]
            if title not in seen or self._priority_value(rec["priority"]) > self._priority_value(seen[title]["priority"]):
                seen[title] = rec
        
        # Sort by priority
        return sorted(
            seen.values(),
            key=lambda x: self._priority_value(x["priority"]),
            reverse=True
        )
    
    def _priority_value(self, priority: str) -> int:
        """Convert priority to numeric value"""
        priority_map = {"high": 3, "medium": 2, "low": 1}
        return priority_map.get(priority, 0)


# Singleton instance
_recommendation_engine = RecommendationEngine()


def get_recommendation_engine() -> RecommendationEngine:
    """Get recommendation engine instance"""
    return _recommendation_engine