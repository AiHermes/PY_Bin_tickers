import requests
import socket

def internet_connected(host="8.8.8.8", port=53, timeout=3):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return True
    except socket.error as ex:
        print(f"No internet connection: {ex}")
        return False

def fetch_binance_futures_tickers():
    if not internet_connected():
        print("No internet connection")
        return None

    url = "https://fapi.binance.com/fapi/v1/ticker/24hr"
    
    print(f"Fetching data from {url}")
    
    # Прокси-сервер с авторизацией
    proxies = {
        "http": "http://buysellstyle:XPyp6tmBTc@45.145.221.74:50100",
        "https": "http://buysellstyle:XPyp6tmBTc@45.145.221.74:50100",
    }
    
    try:
        response = requests.get(url, proxies=proxies)
        print(f"Response status code: {response.status_code}")
        if response.status_code == 200:
            return response.json()
        else:
            print("Failed to fetch data from Binance API")
            return None
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def filter_tickers_by_volume(tickers):
    high_volume_tickers = []
    mid_volume_tickers = []
    
    for ticker in tickers:
        volume = float(ticker['quoteVolume'])
        if "usdt" in ticker['symbol'].lower():
            if volume > 100000000:
                high_volume_tickers.append((ticker['symbol'], volume))
            elif 10000000 < volume <= 100000000:
                mid_volume_tickers.append((ticker['symbol'], volume))
    
    # Sort tickers by volume in descending order
    high_volume_tickers.sort(key=lambda x: x[1], reverse=True)
    mid_volume_tickers.sort(key=lambda x: x[1], reverse=True)
    
    return high_volume_tickers, mid_volume_tickers

def save_tickers_to_file(tickers, filename):
    with open(filename, 'w') as file:
        for ticker, volume in tickers:
            file.write(f"BINANCE:{ticker}\n")

def main():
    tickers_data = fetch_binance_futures_tickers()
    
    if tickers_data:
        print(f"Fetched {len(tickers_data)} tickers")
        high_volume_tickers, mid_volume_tickers = filter_tickers_by_volume(tickers_data)
        
        save_tickers_to_file(high_volume_tickers, "1bin.txt")
        save_tickers_to_file(mid_volume_tickers, "100bin.txt")
        
        print("Filtered and sorted tickers have been saved to 1bin.txt and 100bin.txt.")
    else:
        print("No data to process.")

if __name__ == "__main__":
    main()
