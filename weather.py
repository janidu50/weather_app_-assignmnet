import requests
import json

# URLs from the assignment
AREA_URL = "https://www.jma.go.jp/bosai/common/const/area.json"
FORECAST_URL_TEMPLATE = "https://www.jma.go.jp/bosai/forecast/data/forecast/{}.json"

def get_area_list():
    """Fetches the list of regions (prefectures) and returns a dictionary."""
    try:
        response = requests.get(AREA_URL)
        response.raise_for_status() # Check for errors
        data = response.json()
        return data['offices']
    except Exception as e:
        print(f"Error fetching area list: {e}")
        return None

def get_weather(region_code):
    """Fetches weather for a specific region code."""
    url = FORECAST_URL_TEMPLATE.format(region_code)
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching forecast: {e}")
        return None

def main():
    print("Fetching region list from JMA...")
    offices = get_area_list()
    
    if not offices:
        return

    # Display available regions
    print("\nAvailable Regions:")
    print("-" * 30)
    
    valid_codes = []
    for code, info in offices.items():
        print(f"{code}: {info['name']}")
        valid_codes.append(code)

    print("-" * 30)
    
    # User Input
    selected_code = input("\nEnter the region code (e.g., 130000 for Tokyo): ").strip()

    if selected_code not in valid_codes:
        print("Invalid code. Please run the program again.")
        return

    # Fetch Weather
    print(f"\nFetching weather for {offices[selected_code]['name']}...")
    weather_data = get_weather(selected_code)

    if weather_data:
        try:
            report = weather_data[0]
            area_forecast = report['timeSeries'][0]['areas'][0]
            
            location = area_forecast['area']['name']
            today_weather = area_forecast['weathers'][0] 
            
            print("\n" + "="*30)
            print(f"FORECAST FOR: {location}")
            print("="*30)
            print(f"Weather: {today_weather}")
            print(f"Date: {report['reportDatetime']}")
            print("="*30 + "\n")
            
        except (KeyError, IndexError):
            print("Error parsing the weather data.")
            

if __name__ == "__main__":
    main()   