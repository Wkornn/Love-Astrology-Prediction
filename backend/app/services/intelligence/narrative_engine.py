"""LLM Narrative Engine - Generates human-readable narratives from numeric data"""

import os
import json
import logging
from typing import Dict, Optional
import google.generativeai as genai

logger = logging.getLogger(__name__)


class NarrativeEngine:
    """
    Generates narrative text from structured numeric data using Claude API
    
    Does NOT modify numeric values - only generates human-readable text
    """
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize with Google Gemini API key from environment or parameter"""
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemma-3-27b-it')
        else:
            self.model = None
            logger.warning("GEMINI_API_KEY not set - using fallback templates")
    
    def generate_mode1_narrative(self, scores: Dict) -> Dict[str, str]:
        """
        Generate Mode 1 narrative from love profile scores
        
        Args:
            scores: {
                'love_readiness': 0-100,
                'emotional_maturity': 0-100,
                'passion_level': 0-100,
                'stability_potential': 0-100,
                'fire_score': 0-1,
                'water_score': 0-1,
                ...
            }
        
        Returns:
            {
                'headline': str,
                'personality_summary': str,
                'love_style': str,
                'emotional_pattern': str,
                'relationship_advice': str,
                'bug_explanation': str
            }
        """
        if not self.model:
            return self._fallback_mode1(scores)
        
        try:
            prompt = f"""You are a Thai astrology fortune teller. Generate a playful, witty analysis in THAI language.

Scores:
Love Readiness: {scores.get('love_readiness', 50)}%
Emotional Maturity: {scores.get('emotional_maturity', 50)}%
Passion Level: {scores.get('passion_level', 50)}%
Stability: {scores.get('stability_potential', 50)}%
Fire: {scores.get('fire_score', 0.5)*100}%
Water: {scores.get('water_score', 0.5)*100}%

Generate ONLY valid JSON in THAI:
{{
  "headline": "ประโยคเด็ดสั้นๆ ตลกๆ ไม่เกิน 15 คำ",
  "personality_summary": "2-3 ประโยคเกี่ยวกับนิสัย แบบขำๆ แต่ตรงประเด็น",
  "love_style": "สไตล์รักของคุณ มีมุขตลก 2 ประโยค",
  "emotional_pattern": "รูปแบบอารมณ์ ล้อเล่นแต่จริงใจ 2 ประโยค",
  "relationship_advice": "คำแนะนำแบบเพื่อนคุย 2 ประโยค",
  "bug_explanation": "มุขตลกๆ สไตล์ดูดวง เช่น คุณเป็นคนสมพงษ์กับคนที่ไม่ตอบแชทคุณ"
}}

ใช้ภาษาไทยทั้งหมด ตลกแต่มีสาระ แบบเพื่อนคุยกัน"""

            response = self.model.generate_content(prompt)
            text = response.text
            
            # Extract JSON from response
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0]
            elif '```' in text:
                text = text.split('```')[1].split('```')[0]
            
            return json.loads(text.strip())
            
        except Exception as e:
            logger.error(f"LLM narrative generation failed: {e}")
            return self._fallback_mode1(scores)
    
    def generate_mode2_narrative(self, celebrity_name: str, similarity: float, 
                                 user_scores: Dict, celeb_scores: Dict) -> Dict[str, str]:
        """
        Generate Mode 2 celebrity match narrative
        
        Returns:
            {
                'match_headline': str,
                'why_you_match': str,
                'playful_roast_line': str,
                'fan_comment_style_line': str
            }
        """
        if not self.model:
            return self._fallback_mode2(celebrity_name, similarity)
        
        try:
            prompt = f"""You are a Thai fortune teller. Generate ONE funny joke in Thai.

Celebrity: {celebrity_name}
Match: {similarity}%

Generate ONLY valid JSON with ONE funny sentence in THAI:
{{
  "funny_joke": "ประโยคตลกๆ 1 ประโยค เกี่ยวกับการแมตช์กับดาราคนนี้ ขำๆ แบบล้อเล่น"
}}

ตัวอย่าง: 'คุณกับ {celebrity_name} เหมือนกันถึง {int(similarity)}% - แต่เธอรวยกว่า'
ตลกแต่ไม่เสียมารยาท สั้นๆ"""

            response = self.model.generate_content(prompt)
            text = response.text
            
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0]
            elif '```' in text:
                text = text.split('```')[1].split('```')[0]
            
            return json.loads(text.strip())
            
        except Exception as e:
            logger.error(f"LLM narrative generation failed: {e}")
            return self._fallback_mode2(celebrity_name, similarity)
    
    def generate_mode3_narrative(self, scores: Dict) -> Dict[str, str]:
        """
        Generate Mode 3 couple compatibility narrative
        
        Args:
            scores: {
                'overall_score': 0-100,
                'emotional_sync': 0-100,
                'chemistry_index': 0-100,
                'stability_index': 0-100,
                'hard_aspect_density': 0-1
            }
        
        Returns:
            {
                'relationship_summary': str,
                'key_strengths': str,
                'main_challenges': str,
                'conflict_pattern': str,
                'growth_advice': str,
                'drama_explanation': str
            }
        """
        if not self.model:
            return self._fallback_mode3(scores)
        
        try:
            prompt = f"""You are a Thai fortune teller. Generate playful Thai couple analysis.

Scores:
Overall: {scores.get('overall_score', 50)}%
Emotional Sync: {scores.get('emotional_sync', 50)}%
Chemistry: {scores.get('chemistry_index', 50)}%
Stability: {scores.get('stability_index', 50)}%

Generate ONLY valid JSON in THAI:
{{
  "relationship_summary": "2-3 ประโยคสรุปความสัมพันธ์",
  "key_strengths": "จุดแข็ง 2 ประโยค",
  "main_challenges": "จุดที่ต้องระวัง 2 ประโยค",
  "conflict_pattern": "รูปแบบความขัดแย้ง 1-2 ประโยค",
  "growth_advice": "คำแนะนำแบบเพื่อน 2 ประโยค",
  "drama_explanation": "มุขตลกๆ ประเมินความดราม่า"
}}

ตลกแต่มีสาระ"""

            response = self.model.generate_content(prompt)
            text = response.text
            
            if '```json' in text:
                text = text.split('```json')[1].split('```')[0]
            elif '```' in text:
                text = text.split('```')[1].split('```')[0]
            
            return json.loads(text.strip())
            
        except Exception as e:
            logger.error(f"LLM narrative generation failed: {e}")
            return self._fallback_mode3(scores)
    
    # Fallback templates
    def _fallback_mode1(self, scores: Dict) -> Dict[str, str]:
        """Simple template fallback for Mode 1 in Thai"""
        readiness = scores.get('love_readiness', 50)
        maturity = scores.get('emotional_maturity', 50)
        
        return {
            'headline': f"ความพร้อมรัก {int(readiness)}% - {'พร้อมลุย' if readiness > 60 else 'ยังต้องพัฒนา'}",
            'personality_summary': f"ความเป็นผู้ใหญ่ทางอารมณ์ของคุณอยู่ที่ {int(maturity)}% {'เก่งมาก' if maturity > 70 else 'กำลังพัฒนา'}",
            'love_style': "สไตล์รักของคุณถูกกำหนดโดยดาวเคราะห์ในชาร์ตของคุณ",
            'emotional_pattern': "คุณจัดการอารมณ์ในแบบที่เป็นเอกลักษณ์ของตัวเอง",
            'relationship_advice': "โฟกัสที่การเข้าใจรูปแบบของตัวเองและสื่อสารอย่างเปิดเผย",
            'bug_explanation': f"สถานะระบบ: {'เหมาะสม' if readiness > 70 else 'กำลังพัฒนา'} - ดำเนินการพัฒนาต่อไป"
        }
    
    def _fallback_mode2(self, celebrity_name: str, similarity: float) -> Dict[str, str]:
        """Simple template fallback for Mode 2 in Thai"""
        return {
            'funny_joke': f"คุณกับ {celebrity_name} เข้ากันได้ {int(similarity)}% - ดาวเคราะห์พูดว่าเข้ากันได้!"
        }
    
    def _fallback_mode3(self, scores: Dict) -> Dict[str, str]:
        """Simple template fallback for Mode 3"""
        overall = scores.get('overall_score', 50)
        
        return {
            'relationship_summary': f"Overall compatibility scores {int(overall)}%, indicating {'strong' if overall > 70 else 'moderate'} potential.",
            'key_strengths': "You share complementary qualities that can create balance.",
            'main_challenges': "Different approaches may require understanding and compromise.",
            'conflict_pattern': "Conflicts may arise from differing communication styles.",
            'growth_advice': "Focus on open communication and mutual respect.",
            'drama_explanation': f"Drama risk: {'Low' if overall > 70 else 'Moderate'} - maintain healthy boundaries."
        }
