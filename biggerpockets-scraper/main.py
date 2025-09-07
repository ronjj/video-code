from curl_cffi import requests
from bs4 import BeautifulSoup
import json

def parse_forum_posts(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    posts = []
    
    # Find all post containers
    post_containers = soup.find_all('div', class_='tw-bg-white tw-divide-solid tw-divide-neutral-200 tw-divide-y tw-shadow tw-border-neutral-400 simplified-forums__card-wrapper-compact tw-text-sm')
    
    for container in post_containers:
        post_divs = container.find_all('div', attrs={'data-topic-id': True})
        
        for post_div in post_divs:
            try:
                post_data = {}
                
                # Extract post title and URL
                title_link = post_div.find('a', class_='tw-font-semibold tw-text-lg tw-leading-none tw-text-slate-bp-dark')
                if title_link:
                    post_data['title'] = title_link.get_text(strip=True)
                    post_data['url'] = 'https://www.biggerpockets.com' + title_link.get('href', '')
                
                # Extract author
                author_link = post_div.find('a', class_='simplified-forums__user__profile-link')
                if author_link:
                    post_data['author'] = author_link.get_text(strip=True)
                    post_data['author_url'] = 'https://www.biggerpockets.com' + author_link.get('href', '')
                
                # Extract post timestamp
                time_element = post_div.find('time', attrs={'data-timeago-datetime-value': True})
                if time_element:
                    post_data['posted_date'] = time_element.get('data-timeago-datetime-value')
                    post_data['posted_date_readable'] = time_element.get('title', '')
                
                # Extract reply count
                reply_count = post_div.find('span', class_='simplified-forums__card__reply-count')
                if reply_count:
                    post_data['reply_count'] = reply_count.get_text(strip=True)
                
                # Extract vote count
                vote_count = post_div.find('span', class_='tw-text-gray-300 simplified-forums__vote__count')
                if vote_count:
                    post_data['vote_count'] = vote_count.get_text(strip=True)
                
                # Extract category
                category_link = post_div.find('a', class_='simplified-forums__topic-metadata__link')
                if category_link:
                    post_data['category'] = category_link.get_text(strip=True)
                
                # Extract location if available
                location_chip = post_div.find('div', class_='simplified-forums__tag-location')
                if location_chip:
                    location_span = location_chip.find('span')
                    if location_span:
                        post_data['location'] = location_span.get_text(strip=True)
                
                if post_data:  # Only add if we found some data
                    posts.append(post_data)
                    
            except Exception as e:
                print(f"Error parsing post: {e}")
                continue
    
    return posts

def parse_post_replies(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    replies = []
    
    # Find all JSON-LD script tags
    script_tags = soup.find_all('script', type='application/ld+json')
    
    for script in script_tags:
        try:
            # Parse the JSON content
            json_data = json.loads(script.string)
            
            # Handle both single objects and arrays
            if isinstance(json_data, list):
                json_objects = json_data
            else:
                json_objects = [json_data]
            
            # Look for the main entity with comments
            for obj in json_objects:
                if obj.get('@type') == 'WebPage' and 'mainEntity' in obj:
                    main_entity = obj['mainEntity']
                    if 'comment' in main_entity:
                        comments = main_entity['comment']
                        
                        for comment in comments:
                            try:
                                reply_data = {}
                                
                                # Extract reply author
                                if 'author' in comment:
                                    author = comment['author']
                                    reply_data['author'] = author.get('name', '')
                                    reply_data['author_url'] = author.get('url', '')
                                
                                # Extract reply content
                                if 'text' in comment:
                                    reply_data['content'] = comment['text']
                                
                                # Extract timestamps
                                if 'dateCreated' in comment:
                                    reply_data['posted_date'] = comment['dateCreated']
                                if 'datePublished' in comment:
                                    reply_data['published_date'] = comment['datePublished']
                                if 'dateModified' in comment:
                                    reply_data['modified_date'] = comment['dateModified']
                                
                                # Extract reply URL
                                if 'url' in comment:
                                    reply_data['reply_url'] = comment['url']
                                
                                # Extract interaction statistics (likes/votes)
                                if 'interactionStatistic' in comment:
                                    for interaction in comment['interactionStatistic']:
                                        if interaction.get('interactionType') == 'http://schema.org/LikeAction':
                                            reply_data['upvotes'] = interaction.get('userInteractionCount', 0)
                                
                                if reply_data:
                                    replies.append(reply_data)
                                    
                            except Exception as e:
                                print(f"Error parsing individual comment: {e}")
                                continue
                                
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON from script tag: {e}")
            continue
        except Exception as e:
            print(f"Error processing script tag: {e}")
            continue
    
    return replies

url = "https://www.biggerpockets.com/forums?conversion_id=8143&location=houston-texas"

payload = {}
headers = {
  'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
  'accept-language': 'en-US,en;q=0.7',
  'priority': 'u=0, i',
  'referer': 'https://www.biggerpockets.com/search?term=Houston+Texas',
  'sec-ch-ua': '"Not)A;Brand";v="8", "Chromium";v="138", "Brave";v="138"',
  'sec-ch-ua-mobile': '?1',
  'sec-ch-ua-platform': '"Android"',
  'sec-fetch-dest': 'document',
  'sec-fetch-mode': 'navigate',
  'sec-fetch-site': 'same-origin',
  'sec-fetch-user': '?1',
  'sec-gpc': '1',
  'upgrade-insecure-requests': '1',
  'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Mobile Safari/537.36',
}

response = requests.request("GET", url, headers=headers, data=payload, impersonate="chrome")

# Parse the forum posts
posts = parse_forum_posts(response.text)

# For each post, visit the URL and get replies
for post in posts:
    if 'url' in post:
        try:
            print(f"Fetching replies for: {post['title']}")
            post_response = requests.request("GET", post['url'], headers=headers, data=payload, impersonate="chrome")
            replies = parse_post_replies(post_response.text)
            post['replies'] = replies
            print(f"Found {len(replies)} replies")
        except Exception as e:
            print(f"Error fetching replies for {post['url']}: {e}")
            post['replies'] = []

# Output the parsed data as JSON
print(json.dumps(posts, indent=2, ensure_ascii=False))
