import requests
import json
import time


def test_website():
    """Test website functionality"""
    base_url = "http://127.0.0.1:5000"

    print("🧪 Testing Schizophrenia Prediction Website")
    print("=" * 50)

    # Test 1: Check if website is accessible
    try:
        response = requests.get(base_url, timeout=5)
        if response.status_code == 200:
            print("✅ Website accessible")
        else:
            print(f"❌ Website error: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to website: {e}")
        return False

    # Test 2: Test model info API
    try:
        response = requests.get(f"{base_url}/api/model-info", timeout=5)
        if response.status_code == 200:
            info = response.json()
            print("✅ Model info API working")
            print(f"   Model: {info.get('model_type')}")
            print(f"   Features: {len(info.get('features', []))}")
            print(f"   Classes: {len(info.get('classes', []))}")
        else:
            print("❌ Model info API error")
    except Exception as e:
        print(f"❌ Model info API failed: {e}")

    # Test 3: Test prediction with sample data
    test_cases = [
        {
            "name": "Low Risk Sample",
            "data": {
                "age": 60,
                "gender": 0,  # Female
                "marital_status": 1,  # Married
                "fatigue": 0.1,
                "slowing": 0.1,
                "pain": 0.0,
                "hygiene": 0.8,
                "movement": 0.2,
            },
        },
        {
            "name": "High Risk Sample",
            "data": {
                "age": 75,
                "gender": 1,  # Male
                "marital_status": 3,  # Widowed
                "fatigue": 0.8,
                "slowing": 0.7,
                "pain": 0.6,
                "hygiene": 0.2,
                "movement": 0.9,
            },
        },
    ]

    print("\n🎯 Testing Predictions:")
    print("-" * 30)

    for test_case in test_cases:
        try:
            response = requests.post(
                f"{base_url}/predict", data=test_case["data"], timeout=10
            )
            if response.status_code == 200:
                result = response.json()
                if result.get("success"):
                    print(f"\n✅ {test_case['name']}:")
                    print(f"   Prediction: {result['prediction']}")

                    # Show top 3 probabilities
                    probs = result["probabilities"]
                    sorted_probs = sorted(
                        probs.items(), key=lambda x: x[1], reverse=True
                    )[:3]
                    print("   Top probabilities:")
                    for class_name, prob in sorted_probs:
                        print(f"     {class_name}: {prob}%")
                else:
                    print(f"❌ {test_case['name']}: {result.get('error')}")
            else:
                print(f"❌ {test_case['name']}: HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {test_case['name']}: {e}")

    print("\n" + "=" * 50)
    print("🎉 Website testing completed!")
    print("\n📝 Access the website at: http://127.0.0.1:5000")
    print("📝 Try the prediction form with your own data")

    return True


if __name__ == "__main__":
    # Wait a moment for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)

    test_website()
