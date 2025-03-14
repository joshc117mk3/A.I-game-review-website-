import requests
import pandas as pd
import time

# API keys
STEAM_API_KEY = "enter api"

# Candidate games (100 appids)
candidate_games = [
    {"appid": 730, "name": "Counter-Strike 2"},
    {"appid": 271590, "name": "Grand Theft Auto V"},
    {"appid": 578080, "name": "PUBG: BATTLEGROUNDS"},
    {"appid": 359550, "name": "Rainbow Six Siege"},
    {"appid": 252490, "name": "Rust"},
    {"appid": 1245620, "name": "Elden Ring"},
    {"appid": 413150, "name": "Stardew Valley"},
    {"appid": 431960, "name": "Wallpaper Engine"},
    {"appid": 346110, "name": "ARK: Survival Evolved"},
    {"appid": 1085660, "name": "Destiny 2"},
    {"appid": 582010, "name": "Monster Hunter: World"},
    {"appid": 238960, "name": "Path of Exile"},
    {"appid": 381210, "name": "Dead by Daylight"},
    {"appid": 304930, "name": "Unturned"},
    {"appid": 620, "name": "Portal 2"},
    {"appid": 230410, "name": "Warframe"},
    {"appid": 4000, "name": "Garry's Mod"},
    {"appid": 294100, "name": "RimWorld"},
    {"appid": 105600, "name": "Terraria"},
    {"appid": 892970, "name": "Valheim"},
    {"appid": 377160, "name": "Fallout 4"},
    {"appid": 548430, "name": "Deep Rock Galactic"},
    {"appid": 1599340, "name": "Lost Ark"},
    {"appid": 440, "name": "Team Fortress 2"},
    {"appid": 550, "name": "Left 4 Dead 2"},
    {"appid": 1086940, "name": "Baldur's Gate 3"},
    {"appid": 1172470, "name": "Apex Legends"},
    {"appid": 252950, "name": "Rocket League"},
    {"appid": 1145360, "name": "Hades"},
    {"appid": 990080, "name": "Hogwarts Legacy"},
    {"appid": 1938090, "name": "Call of Duty HQ"},
    {"appid": 1675200, "name": "Starfield"},
    {"appid": 1240440, "name": "Halo Infinite"},
    {"appid": 1449850, "name": "Space Marine 2"},
    {"appid": 218620, "name": "PAYDAY 2"},
    {"appid": 236390, "name": "War Thunder"},
    {"appid": 255710, "name": "Cities: Skylines"},
    {"appid": 261550, "name": "Mount & Blade II: Bannerlord"},
    {"appid": 289070, "name": "Civilization VI"},
    {"appid": 322330, "name": "Don't Starve Together"},
    {"appid": 394360, "name": "Hearts of Iron IV"},
    {"appid": 427520, "name": "Factorio"},
    {"appid": 489830, "name": "Skyrim Special Edition"},
    {"appid": 594650, "name": "Hunt: Showdown"},
    {"appid": 601510, "name": "Yu-Gi-Oh! Duel Links"},
    {"appid": 648800, "name": "Raft"},
    {"appid": 668950, "name": "Hollow Knight"},
    {"appid": 739630, "name": "Phasmophobia"},
    {"appid": 813630, "name": "Supraland"},
    {"appid": 945360, "name": "Among Us"},
    {"appid": 960090, "name": "Bloons TD 6"},
    {"appid": 962130, "name": "Grounded"},
    {"appid": 108600, "name": "Project Zomboid"},
    {"appid": 1158310, "name": "Crusader Kings III"},
    {"appid": 1174180, "name": "Red Dead Redemption 2"},
    {"appid": 1203220, "name": "NARAKA: BLADEPOINT"},
    {"appid": 1222670, "name": "The Forest"},
    {"appid": 1286830, "name": "Star Wars: Squadrons"},
    {"appid": 1326470, "name": "Sons Of The Forest"},
    {"appid": 1366540, "name": "Dyson Sphere Program"},
    {"appid": 1426210, "name": "It Takes Two"},
    {"appid": 1455840, "name": "Slime Rancher"},
    {"appid": 1468810, "name": "Satisfactory"},
    {"appid": 1517290, "name": "Battlefield 2042"},
    {"appid": 1623660, "name": "Balatro"},
    {"appid": 1659040, "name": "Hitman 3"},
    {"appid": 1811260, "name": "EA SPORTS FC 25"},
    {"appid": 1888160, "name": "Risk of Rain 2"},
    {"appid": 1966720, "name": "Lethal Company"},
    {"appid": 2073850, "name": "The Finals"},
    {"appid": 2087030, "name": "Party Animals"},
    {"appid": 2215430, "name": "Ghost Watchers"},
    {"appid": 2322010, "name": "God of War Ragnarök"},
    {"appid": 2358720, "name": "Overwatch 2"},
    {"appid": 2448970, "name": "Sniper Elite 5"},
    {"appid": 251570, "name": "7 Days to Die"},
    {"appid": 264710, "name": "Subnautica"},
    {"appid": 275850, "name": "No Man's Sky"},
    {"appid": 286690, "name": "Metro Exodus"},
    {"appid": 292030, "name": "The Witcher 3: Wild Hunt"},
    {"appid": 301520, "name": "Robocraft"},
    {"appid": 304390, "name": "For Honor"},
    {"appid": 361420, "name": "Astroneer"},
    {"appid": 386360, "name": "SMITE"},
    {"appid": 393380, "name": "Squad"},
    {"appid": 444090, "name": "Paladins"},
    {"appid": 460930, "name": "Tom Clancy's Ghost Recon Wildlands"},
    {"appid": 504230, "name": "Celeste"},
    {"appid": 526870, "name": "Vampire Survivors"},
    {"appid": 552520, "name": "Far Cry 5"},
    {"appid": 553850, "name": "Helldivers"},
    {"appid": 570940, "name": "The Elder Scrolls V: Skyrim VR"},
    {"appid": 629760, "name": "MORDHAU"},
    {"appid": 632360, "name": "Risk of Rain"},
    {"appid": 646570, "name": "Slay the Spire"},
    {"appid": 698780, "name": "Dofus"},
    {"appid": 704270, "name": "BATTLETECH"},
    {"appid": 761890, "name": "Albion Online"},
    {"appid": 1091500, "name": "Cyberpunk 2077"}
]

# Fetch review counts to rank
def get_review_count(appid):
    url = f"https://store.steampowered.com/appreviews/{appid}?json=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        if "query_summary" in data and "total_reviews" in data["query_summary"]:
            return data["query_summary"]["total_reviews"]
        print(f"No review data for appid {appid}")
        return 0
    print(f"Failed to fetch reviews for appid {appid}: {response.status_code}")
    return 0

for game in candidate_games:
    game["total_reviews"] = get_review_count(game["appid"])
    print(f"Total reviews for {game['name']}: {game['total_reviews']}")
    time.sleep(1)

# Sort and take top 100
top_games = sorted(candidate_games, key=lambda x: x["total_reviews"], reverse=True)[:100]

# Fetch game details from appdetails
def get_game_details(appid):
    url = f"http://store.steampowered.com/api/appdetails?appids={appid}"
    response = requests.get(url)
    if response.status_code == 200:
        app_data = response.json()[str(appid)]
        if app_data.get("success") and "data" in app_data:
            data = app_data["data"]
            price_data = data.get("price_overview", {})
            details = {
                "name": data.get("name", "Unknown"),
                "release_date": data.get("release_date", {}).get("date", "N/A"),
                "price": price_data.get("final_formatted", "Free") if data.get("is_free", False) or price_data else "N/A",
                "genres": ", ".join([g["description"] for g in data.get("genres", [])]),
                "developers": ", ".join(data.get("developers", ["N/A"])),
                "publishers": ", ".join(data.get("publishers", ["N/A"])),
                "metacritic_score": data.get("metacritic", {}).get("score", "N/A"),
                "description": data.get("short_description", "No description available.")
            }
            return details
        else:
            print(f"No valid data for appid {appid}: {app_data}")
    print(f"Failed to fetch details for appid {appid}: {response.status_code}")
    return {
        "name": "Unknown", "release_date": "N/A", "price": "N/A", "genres": "N/A",
        "developers": "N/A", "publishers": "N/A", "metacritic_score": "N/A", "description": "N/A"
    }

# Fetch review data from appreviews
def get_review_data(appid):
    url = f"https://store.steampowered.com/appreviews/{appid}?json=1"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        reviews = data.get("reviews", [])[:2]  # First 2 reviews
        review_text = " | ".join([r["review"] for r in reviews]) if reviews else "No reviews found."
        review_sentiment = ", ".join([("Positive" if r["voted_up"] else "Negative") for r in reviews]) if reviews else "N/A"
        playtime = ", ".join([str(round(r["author"]["playtime_forever"] / 60, 1)) + " hrs" for r in reviews]) if reviews else "N/A"
        return {
            "review_text": review_text[:100] + "..." if len(review_text) > 100 else review_text,
            "review_score": data["query_summary"].get("review_score", 0) * 10,  # Convert 1-10 to 0-100%
            "review_sentiment": review_sentiment,
            "playtime": playtime
        }
    print(f"Failed to fetch reviews for appid {appid}: {response.status_code}")
    return {"review_text": "No reviews found.", "review_score": 0, "review_sentiment": "N/A", "playtime": "N/A"}

# Process top games
for game in top_games:
    details = get_game_details(game["appid"])
    game.update(details)
    review_data = get_review_data(game["appid"])
    game.update(review_data)
    # Placeholder ratings
    game["mechanics"] = 4.0
    game["graphics"] = 4.5
    game["story"] = 3.5
    game["performance"] = 4.0
    game["overall"] = 4.0
    print(f"Processed {game['name']}")
    time.sleep(1)

# Create CSV
data = {
    "Rank": list(range(1, len(top_games) + 1)),
    "Name": [game["name"] for game in top_games],
    "Total Reviews": [game["total_reviews"] for game in top_games],
    "Release Date": [game["release_date"] for game in top_games],
    "Price": [game["price"] for game in top_games],
    "Genres": [game["genres"] for game in top_games],
    "Developers": [game["developers"] for game in top_games],
    "Publishers": [game["publishers"] for game in top_games],
    "Metacritic Score": [game["metacritic_score"] for game in top_games],
    "Description": [game["description"] for game in top_games],
    "Review Text": [game["review_text"] for game in top_games],
    "Review Score (%)": [game["review_score"] for game in top_games],
    "Review Sentiment": [game["review_sentiment"] for game in top_games],
    "Playtime (hrs)": [game["playtime"] for game in top_games],
    "Mechanics": [game["mechanics"] for game in top_games],
    "Graphics": [game["graphics"] for game in top_games],
    "Story": [game["story"] for game in top_games],
    "Performance": [game["performance"] for game in top_games],
    "Overall": [game["overall"] for game in top_games]
}
df = pd.DataFrame(data)
df.to_csv("top_100_steam_games.csv", index=False)
print("CSV updated with enhanced Steam API data!")