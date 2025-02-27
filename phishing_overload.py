import sys
import time
import random
import urllib3
import argparse
import threading
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

# Change this part
PROXIES = [
    "http://5.5.5.5:8080",
    "http://1.2.3.4:4444"
]

def stress_test(url, num_requests, max_retries=20, delay=5):
    attempt = 0
    while attempt < max_retries:
        for i in range(num_requests):
            proxy = random.choice(PROXIES)
            use_proxy = {"http": proxy}
            try:
                response = requests.get(url, proxies=use_proxy, timeout=10, verify=False)
                if response.status_code == 200:
                    print(f"Request {i+1}: Success - Code {response.status_code}")
                else:
                    print(f"Request {i+1}: Error - Code {response.status_code}")
            except requests.exceptions.RequestException as e:
                print(f"Request {i+1}: Error al hacer la solicitud. {str(e)}")
                attempt += 1
                time.sleep(delay)

def run_stress_test(url, total_requests, threads):
    requests_per_thread = total_requests // threads
    threads_list = []

    for i in range(threads):
        thread = threading.Thread(target=stress_test, args=(url, requests_per_thread))
        threads_list.append(thread)

    for thread in threads_list:
        thread.start()

    for thread in threads_list:
        thread.join()

def load_urls_from_file(file_path):
    try:
        with open(file_path, "r") as file:
            urls = [line.strip() for line in file.readlines() if line.strip()]
        return urls
    except FileNotFoundError:
        print(f"[!] Error: File not found '{file_path}'")
        return []

if __name__ == "__main__":
    requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    parser = argparse.ArgumentParser(description="Prueba de sobrecarga a un endpoint o múltiples endpoints desde un archivo.")
    parser.add_argument("--url", type=str, help="La URL del endpoint a probar.")
    parser.add_argument("--file", type=str, help="Archivo .txt con múltiples URLs, una por línea.")
    parser.add_argument("total_requests", type=int, help="Número total de solicitudes que se desean realizar.")
    parser.add_argument("threads", type=int, help="Número de hilos concurrentes que se usarán para realizar las solicitudes.")
    
    args = parser.parse_args()
    
    if args.file:
        urls_to_test = load_urls_from_file(args.file)
    else:
        urls_to_test = [args.url]

    start_time = time.time()
    for url in urls_to_test:
        print(f"\n[*] Starting overload test for: {url}")
        run_stress_test(url, args.total_requests, args.threads)

    end_time = time.time()

    print(f"\nFinished test. Total duration: {end_time - start_time:.2f} seconds.")