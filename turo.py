import json
import asyncio
import zendriver as zd
from curl_cffi import requests

# Global variables to store captured network data
captured_headers = {}
captured_cookies = {}
captured_requests = []
search_api_request = None

async def capture_turo_network_data():
    """
    Uses Zendriver to automate Turo website and capture network requests
    """
    global captured_headers, captured_cookies, captured_requests, search_api_request
    
    print("Starting Zendriver browser...")
    
    # Configure Zendriver
    config = zd.Config()
    config.headless = False  # Set to True if you want headless mode
    
    browser = await zd.start(config)
    page = await browser.get("https://turo.com")
    
    # Enable network domain to capture requests
    await page.send(zd.cdp.network.enable())
    
    # Set up network request listener specifically for the search API
    def on_request_will_be_sent(event, connection=None):
        request = event.request
        if request.url == "https://turo.com/api/v2/search":
            print(f"🎯 CAPTURED TARGET REQUEST: {request.url}")
            global search_api_request
            
            # Parse cookies safely
            cookie_header = request.headers.get('Cookie', '')
            cookies = {}
            if cookie_header:
                try:
                    # Split cookies and create dictionary
                    cookie_pairs = [pair.strip() for pair in cookie_header.split(';') if pair.strip()]
                    for pair in cookie_pairs:
                        if '=' in pair:
                            key, value = pair.split('=', 1)
                            cookies[key.strip()] = value.strip()
                except Exception as e:
                    print(f"⚠️  Error parsing cookies: {e}")
                    cookies = {}
            
            search_api_request = {
                'url': request.url,
                'method': request.method,
                'cookies': cookies,
                'headers': dict(request.headers),
                'post_data': getattr(request, 'post_data', None)
            }
            captured_requests.append(search_api_request)
            # Store the headers from this specific request
            captured_headers.update(dict(request.headers))
            print(f"📋 Captured {len(request.headers)} headers from search API request")
    
    # Set up response listener to capture response headers
    def on_response_received(event, connection=None):
        response = event.response
        if response.url == "https://turo.com/api/v2/search":
            print(f"🎯 RESPONSE FROM TARGET: {response.url} - Status: {response.status}")
            if hasattr(response, 'headers'):
                print(f"📋 Captured {len(response.headers)} response headers from search API")
    
    # Add event listeners
    page.add_handler(zd.cdp.network.RequestWillBeSent, on_request_will_be_sent)
    page.add_handler(zd.cdp.network.ResponseReceived, on_response_received)
    
    try:
        print("Navigating to Turo.com...")
        await page.get("https://turo.com")
        
        # Wait for page to load
        await asyncio.sleep(3)
        
        print("Looking for search input field...")
        # Find the search input field using the data-testid attribute
        search_input = await page.find('[data-testid="search-form-location-typeahead-input"]', timeout=10)
        
        if search_input:
            print("Found search input, clicking it...")
            await search_input.click()
            await asyncio.sleep(1)
            
            print("Typing 'JFK' in search field...")
            await search_input.send_keys("JFK")
            await asyncio.sleep(2)
            
            print("Looking for search button...")
            # Find and click the search button
            search_button = await page.find('[data-testid="search-form-submit-button"]', timeout=10)
            
            if search_button:
                print("Found search button, clicking it...")
                await search_button.click()
                
                # Wait for the search request to complete
                print("⏳ Waiting for search API request...")
                await asyncio.sleep(5)
                
                # Capture cookies from the browser after the search
                cookies_response = await page.send(zd.cdp.network.get_cookies())
                
                # Handle the cookies response properly
                if isinstance(cookies_response, list):
                    # Direct list of cookie objects
                    captured_cookies = {cookie.name: cookie.value for cookie in cookies_response}
                elif hasattr(cookies_response, 'cookies') and cookies_response.cookies:
                    captured_cookies = {cookie.name: cookie.value for cookie in cookies_response.cookies}
                elif isinstance(cookies_response, dict) and 'cookies' in cookies_response:
                    captured_cookies = {cookie['name']: cookie['value'] for cookie in cookies_response['cookies']}
                else:
                    print(f"⚠️  Unexpected cookies response format: {type(cookies_response)}")
                    captured_cookies = {}
                
                print(f"🍪 Captured {len(captured_cookies)} cookies from browser")
                
                if search_api_request:
                    print("✅ Successfully captured data from https://turo.com/api/v2/search")
                else:
                    print("❌ Did not capture the target search API request")
                
            else:
                print("Search button not found!")
        else:
            print("Search input field not found!")
            
    except Exception as e:
        print(f"Error during automation: {e}")
    
    finally:
        print("Closing browser...")
        await browser.stop()
    
    return captured_headers, captured_cookies, captured_requests

def make_turo_request_with_captured_data():
    """
    Makes a request to Turo's search API using captured headers and cookies
    """
    global captured_headers, captured_cookies, captured_requests, search_api_request
    
    if not search_api_request:
        print("❌ No search API request captured! Run capture_turo_network_data() first.")
        return None
    
    # URL for the request
    url = "https://turo.com/api/v2/search"
    
    # Use the exact headers from the captured search API request
    headers = search_api_request['headers'].copy()
    
    # Add some essential headers that might be missing
    essential_headers = {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.8',
        'content-type': 'application/json',
        'origin': 'https://turo.com',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
    }
    
    # Add essential headers if they're not already present
    for key, value in essential_headers.items():
        if key not in headers and key.lower() not in [h.lower() for h in headers.keys()]:
            headers[key] = value
    
    print(f"🚀 Using {len(headers)} headers from captured search API request")
    
    if captured_cookies:
        print(f"🍪 Using {len(captured_cookies)} cookies from browser session")
    else:
        print("⚠️  No cookies captured, proceeding without cookies")
    
    # Use the exact POST data from the captured request if available
    if search_api_request.get('post_data'):
        try:
            data = json.loads(search_api_request['post_data'])
            print("📦 Using exact POST data from captured request")
        except json.JSONDecodeError:
            print("⚠️  Could not parse captured POST data, using fallback")
            # Fallback data
            data = {
                "filters": {
                    "location": {
                        "country": "US",
                        "type": "poi",
                        "locationId": 7904760,
                        "pickupType": "ALL"
                    },
                    "age": 27,
                    "engines": [],
                    "makes": [],
                    "models": [],
                    "dates": {
                        "end": "2025-07-07T10:00",
                        "start": "2025-07-03T10:00"
                    },
                    "tmvTiers": [],
                    "features": [],
                    "types": []
                },
                "sorts": {
                    "direction": "ASC",
                    "type": "RELEVANCE"
                }
            }
    else:
        print("⚠️  No POST data captured, using fallback")
        # Fallback data
        data = {
            "filters": {
                "location": {
                    "country": "US",
                    "type": "poi",
                    "locationId": 7904760,
                    "pickupType": "ALL"
                },
                "age": 27,
                "engines": [],
                "makes": [],
                "models": [],
                "dates": {
                    "end": "2025-06-07T10:00",
                    "start": "2025-06-03T10:00"
                },
                "tmvTiers": [],
                "features": [],
                "types": []
            },
            "sorts": {
                "direction": "ASC",
                "type": "RELEVANCE"
            }
        }
    
    try:
        print("\n🔄 Making request with captured data...")
        
        # Make the request using curl_cffi with captured cookies and headers
        response = requests.post(
            url,
            headers=headers,
            cookies=captured_cookies if captured_cookies else None,
            json=data,
            impersonate="chrome"
        )
        
        # Print response details
        print(f"📊 Status Code: {response.status_code}")
        print(f"📋 Response Headers: {len(response.headers)} headers")
        
        # If successful, print a truncated version of the JSON response
        if response.status_code == 200:
            try:
                json_response = response.json()
                print("\n✅ SUCCESS! Truncated JSON Response:")
                
                # Print basic structure info
                if isinstance(json_response, dict):
                    print(f"📦 Response contains {len(json_response)} top-level keys:")
                    for key in json_response.keys():
                        value = json_response[key]
                        if isinstance(value, list):
                            print(f"   • {key}: array with {len(value)} items")
                        elif isinstance(value, dict):
                            print(f"   • {key}: object with {len(value)} keys")
                        else:
                            print(f"   • {key}: {type(value).__name__}")
                    
                    # Show first few items if there's a results/data array
                    for key in ['results', 'data', 'vehicles', 'cars']:
                        if key in json_response and isinstance(json_response[key], list):
                            items = json_response[key]
                            print(f"\n🚗 First 3 items from '{key}' array:")
                            for i, item in enumerate(items[:3]):
                                if isinstance(item, dict):
                                    # Show key fields for each item
                                    item_info = []
                                    for field in ['id', 'name', 'make', 'model', 'year', 'price', 'dailyPrice']:
                                        if field in item:
                                            item_info.append(f"{field}: {item[field]}")
                                    print(f"   {i+1}. {', '.join(item_info[:4])}")
                            if len(items) > 3:
                                print(f"   ... and {len(items) - 3} more items")
                            break
                    
                    # Show pagination info if available
                    for key in ['pagination', 'meta', 'paging']:
                        if key in json_response and isinstance(json_response[key], dict):
                            paging = json_response[key]
                            print(f"\n📄 Pagination info:")
                            for field in ['total', 'count', 'page', 'limit', 'totalPages']:
                                if field in paging:
                                    print(f"   • {field}: {paging[field]}")
                            break
                
                elif isinstance(json_response, list):
                    print(f"📦 Response is an array with {len(json_response)} items")
                    if json_response:
                        print(f"   First item type: {type(json_response[0]).__name__}")
                
                print(f"\n💾 Full response size: {len(response.text)} characters")
                
            except json.JSONDecodeError:
                print("\n⚠️  Response is not valid JSON")
                print(f"Response Body (first 500 chars): {response.text[:500]}...")
        else:
            print(f"\n❌ Request failed with status {response.status_code}")
            print(f"Response Body (first 500 chars): {response.text[:500]}...")
        
        return response
        
    except Exception as e:
        print(f"❌ Error making request: {e}")
        return None

def print_captured_data():
    """
    Prints the captured network data for inspection
    """
    print("\n" + "="*60)
    print("🎯 CAPTURED DATA FROM https://turo.com/api/v2/search")
    print("="*60)
    
    if search_api_request:
        print("\n🚀 TARGET SEARCH API REQUEST:")
        print(f"   URL: {search_api_request['url']}")
        print(f"   Method: {search_api_request['method']}")
        print(f"   Headers ({len(search_api_request['headers'])} total):")
        for key, value in search_api_request['headers'].items():
            print(f"     {key}: {value}")
        
        if search_api_request['post_data']:
            print(f"\n   📦 POST Data:")
            try:
                post_data = json.loads(search_api_request['post_data'])
                print(json.dumps(post_data, indent=6))
            except:
                print(f"     {search_api_request['post_data']}")
    else:
        print("\n❌ No data captured from the target search API endpoint")
    
    print(f"\n🍪 CAPTURED COOKIES ({len(captured_cookies)} total):")
    for key, value in captured_cookies.items():
        print(f"   {key}: {value}")
    
    print(f"\n📡 ALL CAPTURED REQUESTS ({len(captured_requests)} total):")
    for i, req in enumerate(captured_requests):
        icon = "🎯" if req['url'] == "https://turo.com/api/v2/search" else "📡"
        print(f"   {icon} Request {i+1}: {req['method']} {req['url']}")
        
    print("\n" + "="*60)
    print("💡 Use the headers and cookies above for your API requests!")
    print("="*60)

async def main():
    """
    Main function that orchestrates the entire process
    """
    print("Starting Turo automation with Zendriver...")
    
    # Step 1: Capture network data using browser automation
    await capture_turo_network_data()
    
    # Step 2: Print captured data for inspection
    print_captured_data()
    
    # Step 3: Use captured data to make API request
    print("\n" + "="*50)
    print("MAKING API REQUEST WITH CAPTURED DATA")
    print("="*50)
    make_turo_request_with_captured_data()

if __name__ == "__main__":
    print("Turo Network Capture Tool")
    print("This script will:")
    print("1. Open Turo.com in a browser")
    print("2. Search for 'JFK'")
    print("3. Capture network requests, headers, and cookies")
    print("4. Use captured data to make API requests")
    print("\nStarting...")
    
    asyncio.run(main())
