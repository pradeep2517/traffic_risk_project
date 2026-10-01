"""
Multilingual Early Warning Alert System
Generates actionable safety alerts in English, Hindi, and Tamil based on risk levels.
"""

class AlertGenerator:
    def __init__(self):
        # Dictionary storing alert templates for different languages
        self.templates = {
            "en": {
                "LOW (Green)": "Traffic flow is stable. Continue with standard caution.",
                "MODERATE (Yellow)": "Moderate Risk: Minor congestion or road irregularities ahead. Stay alert.",
                "HIGH (Orange)": "High Risk Alert: Wet roads and heavy congestion detected. Reduce speed.",
                "CRITICAL (Red)": "CRITICAL WARNING: High accident probability ahead! Reduce speed immediately to 40 km/h and maintain safe distance."
            },
            "hi": {
                "LOW (Green)": "यातायात स्थिर है। सामान्य सावधानी के साथ आगे बढ़ें।",
                "MODERATE (Yellow)": "मध्यम जोखिम: आगे हल्का जाम या खराब सड़क है। सतर्क रहें।",
                "HIGH (Orange)": "उच्च जोखिम चेतावनी: गीली सड़क और भारी जाम। गति कम करें।",
                "CRITICAL (Red)": "अत्यंत गंभीर चेतावनी: आगे दुर्घटना की उच्च संभावना है! तुरंत गति कम करके 40 किमी/घंटा करें और सुरक्षित दूरी बनाए रखें।"
            },
            "ta": {
                "LOW (Green)": "போக்குவரத்து சீராக உள்ளது. பாதுகாப்பாக செல்லவும்.",
                "MODERATE (Yellow)": "மிதமான ஆபத்து: முன்னால் போக்குவரத்து நெரிசல் அல்லது சாலை பழுது. கவனமாக இருக்கவும்.",
                "HIGH (Orange)": "அதிக ஆபத்து: ஈரமான சாலை மற்றும் நெரிசல். வேகத்தை குறைக்கவும்.",
                "CRITICAL (Red)": "அபாய எச்சரிக்கை: விபத்து ஏற்பட அதிக வாய்ப்பு உள்ளது! உடனடியாக வேகத்தை 40 கி.மீ ஆக குறைத்து பாதுகாப்பான இடைவெளியை கடைபிடிக்கவும்."
            }
        }

    def generate_alert(self, risk_level, language="en"):
        """
        Returns the localized alert message for the given risk level.
        Defaults to English if language is not supported.
        """
        lang = language if language in self.templates else "en"
        
        # Exact match
        if risk_level in self.templates[lang]:
            return self.templates[lang][risk_level]
            
        # Fallback partial matching in case strings differ slightly
        for key, message in self.templates[lang].items():
            if key.split()[0] in risk_level:
                return message
                
        return "System Warning: Proceed with caution."

if __name__ == "__main__":
    alert_system = AlertGenerator()
    
    print("[INFO] Testing Multilingual Alert Generator...\n")
    test_level = "CRITICAL (Red)"
    
    print(f"English: {alert_system.generate_alert(test_level, 'en')}")
    print(f"Hindi:   {alert_system.generate_alert(test_level, 'hi')}")
    print(f"Tamil:   {alert_system.generate_alert(test_level, 'ta')}")
    print("\n[SUCCESS] Alert System initialized successfully!")