import streamlit as st
import requests
import speech_recognition as sr
import pyttsx3

# Weather API key
weather_api_key = "e4b646c69c594aaea6c150817240404"

# Function to take input from the farmer
def take_farmer_input(language):
    st.header(get_welcome_message(language))
    st.subheader(get_label("Please provide the following information:", language))
    location = st.text_input(get_label("Enter your location (city, country):", language))
    crops_grown = st.text_input(get_label("Enter the crops you grow (comma-separated):", language))
    years_growing = st.number_input(get_label("How many years have you been growing crops?", language))
    soil_type = st.text_input(get_label("Enter your soil type:", language))
    farm_size = st.number_input(get_label("Enter your farm size (in hectares):", language))
    
    farmer_input = {
        'location': location,
        'crops_grown': crops_grown,
        'years_growing': years_growing,
        'soil_type': soil_type,
        'farm_size': farm_size
    }
    
    return farmer_input

# Function to fetch real-time weather data
def fetch_realtime_weather(location):
    url = f"https://api.weatherapi.com/v1/current.json?key={weather_api_key}&q={location}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data['current']
    else:
        st.error("Error fetching weather data.")
        return None

# Function to generate optimization techniques based on weather conditions and farmer's inputs
def generate_optimization_techniques(farmer_input, weather_data, language):
    temperature = weather_data.get('temp_c', 0)
    precipitation = weather_data.get('precip_mm', 0)
    humidity = weather_data.get('humidity', 0)
    wind_speed = weather_data.get('wind_kph', 0)
    
    years_growing = farmer_input.get('years_growing', 0)
    soil_type = farmer_input.get('soil_type', '')
    crop_types = farmer_input.get('crops_grown', '').split(',')
    farm_size = farmer_input.get('farm_size', 0)
    
    optimization_techniques = []
    
    if temperature > 30:
        optimization_techniques.append(get_optimization_message("During hot weather, provide shade or cover to crops to prevent wilting and heat stress.", language))
    elif temperature < 10:
        optimization_techniques.append(get_optimization_message("During cold weather, protect sensitive crops from frost by covering them or using protective measures.", language))
    
    if precipitation > 20:
        optimization_techniques.append(get_optimization_message("Improve drainage systems to prevent waterlogging during heavy rainfall.", language))
    elif precipitation < 5:
        optimization_techniques.append(get_optimization_message("During dry spells, implement irrigation techniques such as drip irrigation or rainwater harvesting.", language))
    
    if humidity > 80:
        optimization_techniques.append(get_optimization_message("Increase ventilation in storage areas to prevent mold and fungal growth.", language))
    
    if wind_speed > 20:
        optimization_techniques.append(get_optimization_message("Plant windbreaks such as trees or shrubs to reduce wind speed and protect crops from wind damage.", language))
    
    if 'sandy' in soil_type.lower():
        optimization_techniques.append(get_optimization_message("In sandy soil, apply organic mulches to improve moisture retention and soil structure.", language))
    elif 'clay' in soil_type.lower():
        optimization_techniques.append(get_optimization_message("In clay soil, implement raised beds or improve drainage to prevent waterlogging.", language))
    
    if 'rice' in crop_types:
        optimization_techniques.append(get_optimization_message("For rice cultivation, ensure proper water management by maintaining consistent water levels in fields.", language))
        if 'wheat' in crop_types or 'legumes' in crop_types:
            optimization_techniques.append(get_optimization_message("Practice crop rotation by alternating rice with wheat or legumes to improve soil fertility and reduce pest pressure.", language))
    if 'sugarcane' in crop_types:
        optimization_techniques.append(get_optimization_message("For sugarcane cultivation, practice timely harvesting and proper storage to maintain sugar content.", language))
        if 'legumes' in crop_types or 'cereals' in crop_types:
            optimization_techniques.append(get_optimization_message("Rotate sugarcane with legumes or cereals to break disease cycles and enhance soil health.", language))
    if 'cotton' in crop_types:
        optimization_techniques.append(get_optimization_message("For cotton cultivation, implement integrated pest management practices to control pests and reduce pesticide usage.", language))
        if 'pulses' in crop_types or 'oilseeds' in crop_types:
            optimization_techniques.append(get_optimization_message("Rotate cotton with pulses or oilseeds to manage soil-borne diseases and improve nutrient availability.", language))
    
    if farm_size > 10:
        optimization_techniques.append(get_optimization_message("Consider forming cooperatives or collective farming initiatives to pool resources and improve market access.", language))
    
    return optimization_techniques

# Function to get welcome message in different languages
def get_welcome_message(language):
    language_options = {
        "English": "Welcome to the Agriculture Optimization App!",
        "Hindi": "कृषि अनुकूलन ऐप में आपका स्वागत है!",
        "Tamil": "விவசாய சுருக்க பயன்பாட்டிற்கு வரவேற்கின்றேன்!",
        "Telugu": "వ్యవసాయ సారాంశం అనుకూలత యాప్‌కు స్వాగతం!",
        "Marathi": "कृषी सुधारणा अ‍ॅपमध्ये आपले स्वागत आहे!",
        "Bengali": "কৃষি অপ্টিমাইজেশন অ্যাপে আপনাকে স্বাগতম!",
        "Gujarati": "કૃષિ સુધારણ એપ્લિકેશનમાં આપનું સ્વાગત છે!",
        "Kannada": "ಕೃಷಿ ಒಪ್ಟಿಮೈಸೇಷನ್ ಅಪ್‌ನಲ್ಲಿ ಸುಸ್ವಾಗತ!",
        "Malayalam": "കൃഷി ഓപ്റ്റിമൈസേഷൻ ആപ്പിലേക്ക് സ്വാഗതം!"
    }

    return language_options.get(language, "Welcome to the Agriculture Optimization App!")

# Function to get language-specific labels
def get_label(label_text, language):
    language_labels = {
        "English": label_text,
        "Hindi": "कृपया " + label_text + " दर्ज करें",
        "Tamil": label_text + " உள்ளிடவும்",
        "Telugu": label_text + " నమోదు చేయండి",
        "Marathi": label_text + " टाका",
        "Bengali": label_text + " লিখুন",
        "Gujarati": label_text + " નો નામ લખો",
        "Kannada": label_text + " ನ್ನು ನಮೂದಿಸಿ",
        "Malayalam": label_text + " നൽകുക"
    }

    return language_labels.get(language, label_text)

# Function to get language-specific optimization messages
def get_optimization_message(message_text, language):
    language_messages = {
        "English": message_text,
        "Hindi": message_text,
        "Tamil": message_text,
        "Telugu": message_text,
        "Marathi": message_text,
        "Bengali": message_text,
        "Gujarati": message_text,
        "Kannada": message_text,
        "Malayalam": message_text
    }

    return language_messages.get(language, message_text)

# Function to convert text to speech
def text_to_speech(text, language):
    engine = pyttsx3.init()
    engine.setProperty('rate', 150)  # Speed percent (can go over 100)
    engine.setProperty('volume', 1)  # Volume 0-1
    engine.setProperty('voice', language)  # Voice
    engine.say(text)
    engine.runAndWait()

# Main function
def main():
    st.sidebar.header(get_label("Language Selection", "English"))
    language = st.sidebar.selectbox(get_label("Select Language", "English"), options=["English", "Hindi", "Tamil", "Telugu", "Marathi", "Bengali", "Gujarati", "Kannada", "Malayalam"])

    farmer_input = take_farmer_input(language)

    weather_data = fetch_realtime_weather(farmer_input['location'])

    if weather_data:
        optimization_techniques = generate_optimization_techniques(farmer_input, weather_data, language)

        st.header(get_label("Optimization Recommendations", language))
        for recommendation in optimization_techniques:
            st.markdown(f"- {recommendation}")
            text_to_speech(recommendation, language.lower())

if __name__ == "__main__":
    main()
