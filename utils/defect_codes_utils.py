import json
from typing import List, Dict, Optional
from difflib import SequenceMatcher

def load_defect_codes(json_path: str) -> List[Dict]:
    """Load defect codes from JSON file."""
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

def find_best_defect_code(text: str, defect_codes: List[Dict]) -> Optional[Dict]:
    """Find the best matching defect code based on text similarity."""
    if not text or not defect_codes:
        return None
    
    text_lower = text.lower()
    best_match = None
    best_score = 0
    
    for code in defect_codes:
        score = calculate_match_score(text_lower, code)
        if score > best_score:
            best_score = score
            best_match = code
    
    return best_match if best_score > 0 else None

def calculate_match_score(text: str, code: Dict) -> float:
    """Calculate similarity score between text and defect code."""
    score = 0
    
    # Direct code match (highest weight)
    code_str = code.get("code", "").lower()
    if code_str and code_str in text:
        score += 10
    
    # Category match
    category = code.get("category", "").lower()
    if category and category in text:
        score += 3
    
    # Subcategory match
    subcategory = code.get("subcategory", "").lower()
    if subcategory and subcategory in text:
        score += 3
    
    # Description similarity
    description = code.get("description", "").lower()
    if description:
        similarity = SequenceMatcher(None, text, description).ratio()
        score += similarity * 5
        
        # Word-level matches in description
        desc_words = description.split()
        text_words = text.split()
        common_words = set(desc_words) & set(text_words)
        score += len(common_words) * 0.5
    
    return score

def filter_relevant_codes(query: str, defect_codes: List[Dict], max_codes: int = 15) -> List[Dict]:
    """Filter defect codes to only include those relevant to the query."""
    if not query or not defect_codes:
        return defect_codes[:max_codes]
    
    # Calculate relevance scores
    scored_codes = []
    query_lower = query.lower()
    query_words = set(query_lower.split())
    
    for code in defect_codes:
        # Combine all searchable text
        searchable_text = f"{code.get('category', '')} {code.get('subcategory', '')} {code.get('description', '')}".lower()
        searchable_words = set(searchable_text.split())
        
        # Calculate relevance score
        word_matches = len(query_words & searchable_words)
        text_similarity = SequenceMatcher(None, query_lower, searchable_text).ratio()
        
        relevance_score = word_matches * 2 + text_similarity * 3
        
        if relevance_score > 0:
            scored_codes.append((code, relevance_score))
    
    # Sort by relevance and return top codes
    scored_codes.sort(key=lambda x: x[1], reverse=True)
    return [code for code, score in scored_codes[:max_codes]]

def defect_codes_summary(defect_codes: List[Dict]) -> str:
    """Generate a concise summary of defect codes."""
    if not defect_codes:
        return "No defect codes available."
    
    summary = []
    for code in defect_codes:
        summary.append(
            f"{code.get('code', 'N/A')}: {code.get('category', 'N/A')} - "
            f"{code.get('subcategory', 'N/A')} - {code.get('description', 'N/A')}"
        )
    return "\n".join(summary)

def create_compact_codes_reference(defect_codes: List[Dict]) -> str:
    """Create a compact reference format for AI prompts."""
    if not defect_codes:
        return "No defect codes available."
    
    # Group by category for better organization
    categories = {}
    for code in defect_codes:
        category = code.get('category', 'Other')
        if category not in categories:
            categories[category] = []
        categories[category].append(code)
    
    compact_ref = []
    for category, codes in categories.items():
        compact_ref.append(f"\n**{category}:**")
        for code in codes:
            compact_ref.append(
                f"  {code.get('code', '')}: {code.get('subcategory', '')} - {code.get('description', '')}"
            )
    
    return "\n".join(compact_ref)

def get_code_by_id(code_id: str, defect_codes: List[Dict]) -> Optional[Dict]:
    """Get a specific defect code by its ID."""
    for code in defect_codes:
        if code.get('code', '').upper() == code_id.upper():
            return code
    return None

def validate_defect_codes(defect_codes: List[Dict]) -> List[str]:
    """Validate defect codes structure and return any issues found."""
    issues = []
    required_fields = ['code', 'category', 'subcategory', 'description']
    
    for i, code in enumerate(defect_codes):
        if not isinstance(code, dict):
            issues.append(f"Item {i} is not a dictionary")
            continue
        
        for field in required_fields:
            if field not in code or not code[field]:
                issues.append(f"Item {i} missing or empty field: {field}")
        
        # Check for duplicate codes
        code_id = code.get('code', '')
        if code_id:
            duplicates = [j for j, other in enumerate(defect_codes) 
                         if j != i and other.get('code', '') == code_id]
            if duplicates:
                issues.append(f"Duplicate code '{code_id}' found at indices {i} and {duplicates}")
    
    return issues