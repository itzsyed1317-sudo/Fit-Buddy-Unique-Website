import os
import re
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
ALLOW_DEMO_FALLBACK = os.getenv("ALLOW_DEMO_FALLBACK", "true").lower() == "true"

try:
    import google.generativeai as genai
    if API_KEY:
        genai.configure(api_key=API_KEY)
except Exception:
    genai = None

def _clean(text):
    text = text.strip()
    text = re.sub(r"```(?:text|markdown)?", "", text, flags=re.I)
    return text.replace("```", "").strip()

def _demo_plan(name, goal, intensity):
    return f"""7-DAY PULSE PLAN FOR {name.upper()}
Goal: {goal.title()}
Intensity: {intensity.title()}

DAY 1 — FULL BODY FOUNDATION
• Warm-up: 5–10 min easy movement
• Main: Squat pattern 3×8–12, incline push-up 3×8–12, row 3×8–12
• Finish: gentle mobility and breathing

DAY 2 — CARDIO + CORE
• Warm-up: 5–10 min
• Main: 20–30 min comfortable cardio + dead bug 3×8/side + plank 3×20–30 sec
• Finish: easy cooldown

DAY 3 — RECOVERY
• 15–25 min easy walk or mobility
• Keep the session comfortable and focus on recovery

DAY 4 — UPPER BODY
• Warm-up: 5–10 min
• Main: push-up variation 3×8–12, row variation 3×8–12, shoulder press variation 2×8–12
• Finish: upper-body mobility

DAY 5 — LOWER BODY
• Warm-up: 5–10 min
• Main: squat variation 3×8–12, hip-hinge variation 3×8–12, step-up 2×8/side
• Finish: easy cooldown

DAY 6 — CHOICE DAY
• Choose 20–30 min of an enjoyable activity at a comfortable effort
• Add 10 min of mobility

DAY 7 — REST + RESET
• Rest, gentle movement if desired, hydration and sleep routine
• Review how the week felt before planning the next one

SAFETY NOTE
Adjust or stop an exercise if it causes pain, dizziness, or unusual discomfort. This plan is a general educational example, not medical advice."""

def _demo_tip(goal):
    tips = {
        "weight loss": "Build balanced meals around protein, vegetables or fruit, whole-food carbohydrates, and regular hydration. Avoid extreme restriction.",
        "muscle gain": "Include a protein-rich food in regular meals and prioritize recovery, hydration, and adequate overall nutrition.",
        "general wellness": "Keep meals varied, stay hydrated, and pair regular movement with consistent sleep and recovery.",
        "flexibility": "Support mobility work with regular meals, hydration, and gradual progression rather than forcing a stretch."
    }
    return tips.get(goal.lower(), tips["general wellness"])

def generate_workout(name, age, weight, goal, intensity):
    prompt = f"""Create a practical, general 7-day fitness plan for a user named {name}, age {age}, weight {weight}, goal {goal}, preferred intensity {intensity}.
Return plain text with Day 1 through Day 7. For each day include warm-up, main workout with sets/reps or duration, and cooldown/recovery.
Keep it general and adaptable. Do not diagnose, prescribe treatment, encourage extreme dieting, or promise specific body changes.
Mention that exercises should be adapted to ability and stopped if they cause pain or unusual symptoms."""
    if genai and API_KEY:
        try:
            # The project documentation uses Gemini Pro terminology.
            model = genai.GenerativeModel("gemini-1.5-pro")
            return _clean(model.generate_content(prompt).text), "Gemini"
        except Exception:
            if not ALLOW_DEMO_FALLBACK:
                raise
    return _demo_plan(name, goal, intensity), "Demo"

def generate_tip(goal):
    prompt = f"""Give one concise, practical nutrition or recovery tip for the fitness goal: {goal}.
Avoid extreme dieting, calorie restriction instructions, medical claims, or promises. Keep it suitable for a general wellness app."""
    if genai and API_KEY:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            return _clean(model.generate_content(prompt).text), "Gemini"
        except Exception:
            if not ALLOW_DEMO_FALLBACK:
                raise
    return _demo_tip(goal), "Demo"

def update_workout(original_plan, feedback, goal, intensity):
    prompt = f"""Revise this general 7-day fitness plan.
Goal: {goal}
Intensity: {intensity}
Original plan:
{original_plan}

User feedback:
{feedback}

Return a complete revised Day 1–Day 7 plan. Apply the feedback where reasonable. Keep it general, adaptable, and safety-conscious."""
    if genai and API_KEY:
        try:
            model = genai.GenerativeModel("gemini-1.5-pro")
            return _clean(model.generate_content(prompt).text), "Gemini"
        except Exception:
            if not ALLOW_DEMO_FALLBACK:
                raise

    # Simple local revision for demo mode.
    revised = original_plan + f"\n\nFEEDBACK APPLIED (DEMO)\n{feedback}\nThe next session should be adjusted gradually and kept comfortable."
    return revised, "Demo"
