# phishing-overload

This script is designed for internal use to **perform stress testing** on specific API endpoints to evaluate their performance and resilience under high traffic conditions (in some cases it can be used for phishing or fake websites). It allows sending multiple concurrent requests to a single URL or multiple URLs from a file, using **random proxies** to simulate different network conditions.

## Objective  

The goal of this script is to **test the resilience and performance of our internal APIs** under heavy loads. This will help identify bottlenecks, optimize infrastructure, and ensure system stability.

Also you can use it for overload phishing or fake websites.

⚠️ **This script should only be used on authorized endpoints. Unauthorized use on external systems may be illegal.**

## Target Endpoints  

This script is intended to be used on the following internal endpoints:  

- `https://internal-api.com/v1/status`
- `https://internal-api.com/v1/data`
- `https://internal-api.com/v1/users`
- Any other pre-approved internal API endpoints  

Ensure that the target URLs are **under our control** before running tests.

## Installation  

Before running the script, ensure you have the required dependencies installed:

```bash
python -m venv .venv
.\.venv\Scripts\activate #  In linux: source .venv/bin/activate
pip install .
```

## Usage

### Single url

Run the script using a single API endpoint:
```bash
python phishing_overload.py --url "https://internal-api.com/v1/status" 1000 10
```

*This will send 1000 requests using 10 concurrent threads.*

### Multiple urls

If you have multiple endpoints to test, create a .txt file listing them, one per line:

```text
https://internal-api.com/v1/status
https://internal-api.com/v1/data
https://internal-api.com/v1/users
```

Then, run:
```bash
python phishing_overload.py --file urls.txt 500 5
```
*Each URL in urls.txt will receive 500 requests using 5 concurrent threads.*

## Considerations

For test purposes:

* Use this script only on approved internal endpoints.
* Gradually increase the number of requests to prevent system crashes.
* Monitor server logs and performance metrics while running tests.
* Inform the team before executing high-load tests.

## Additional info

The script uses a random proxy from the following list:
```python
PROXIES = [
    "http://212.19.19.239:8080",
    "http://87.103.135.119:4444",
    "http://95.183.10.127:3128",
    ...
]
```
This helps simulate different network conditions and distribute the load.
>[!TIP]
> You can implement a way to get proxies dynamically and avoid this part in configuration.