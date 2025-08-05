import sys
import io
try:
    import openai
except ImportError:
    openai = None

# Force stdout to use utf-8 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Safe print function to handle UnicodeEncodeError
def safe_print(text):
    try:
        print(text)
    except UnicodeEncodeError:
        # In case of an encoding issue, fallback to utf-8 handling
        print(text.encode('utf-8').decode('utf-8'))

# Get values from UI
args = sys.argv[1:]
if len(args) < 6:
    sys.exit(1)  # Exit silently if not enough args

flower_name, plant_color, plant_age, soil_type, mature_level, patches = args


api_key = "YOUR_API_KEY_HERE"  # Replace with your OpenAI API key

# -------------------------------
# BASIC FALLBACK ANALYSIS
# -------------------------------
def basic_analysis():
    feedback = f"🌸 Flower: {flower_name}\n"
    feedback += f"🎨 Color: {plant_color}\n"
    feedback += f"🌱 Age: {plant_age}, Maturity: {mature_level}\n"
    feedback += f"🌍 Soil Type: {soil_type}\n"
    feedback += f"🔍 Patches Present: {patches}\n\n"

    issues = []

    # Check for patch issues
    if patches.lower() == "yes":
        feedback += "⚠️ Detected signs of fungal or pest problems.\n"
        feedback += "🧴 Suggestion: Use neem oil or pesticide.\n"
        issues.append("Patches Present")

    # Soil checks
    if "dry" in soil_type.lower():
        feedback += "💧 Soil appears dry. Increase watering and compost.\n"
        issues.append("Dry Soil")
    elif "clay" in soil_type.lower():
        feedback += "🥣 Clay soil may block drainage. Improve with sand or compost.\n"
        issues.append("Clay Soil")
    elif "sandy" in soil_type.lower():
        feedback += "🏖️ Sandy soil drains fast. Use mulch to retain water.\n"
        issues.append("Sandy Soil")

    # General care
    feedback += "☀️ Ensure enough sunlight (4–6 hrs).\n"
    feedback += "🍃 Trim old leaves and maintain airflow.\n"
    feedback += "🪴 Use organic fertilizer every few weeks.\n"
    feedback += "🧪 Optional: Check soil pH.\n"

    # Final judgment
    feedback += "\n📋 Final Plant Condition: "
    if issues:
        feedback += "Bad\n❌ Condition: Bad\n"
    else:
        feedback += "Good\n✅ Condition: Good\n"

    return feedback

# -------------------------------
# GPT ANALYSIS USING OPENAI
# -------------------------------
def gpt_analysis():
    prompt = f"""
You are a helpful plant doctor. Based on the following plant info, give a warm, emoji-filled status update and helpful growth tips.

Flower: {flower_name}
Color: {plant_color}
Age: {plant_age}
Soil: {soil_type}
Mature Level: {mature_level}
Any patches: {patches}

Include a final summary line that says:
✅ Condition: Good — if the plant seems healthy
OR
❌ Condition: Needs Attention — if there are problems

Use emojis and give tips on watering, pests, and soil care.
"""

    try:
        openai.api_key = api_key
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        # If OpenAI API fails, return the basic analysis
        return basic_analysis()

# -------------------------------
# FINAL EXECUTION
# -------------------------------
if api_key and openai:
    safe_print(gpt_analysis())
else:
    safe_print(basic_analysis())
