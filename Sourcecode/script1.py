import sys
import requests
import json

def main():
    # Validate input arguments
    if len(sys.argv) < 5:
        print("Usage: python trigger_sonarcloud.py <github_token> <owner> <repo> <branch> <sonar_token> [sonar_extra_params]")
        print("Example: python trigger_sonarcloud.py ghp_abc123 myorg myrepo main sq_123456 sonar.param1=value")
        sys.exit(1)

    # Parse arguments
    GITHUB_TOKEN = sys.argv[1]
    OWNER = sys.argv[2]
    REPO = sys.argv[3]
    BRANCH = sys.argv[4]
    SONAR_TOKEN = sys.argv[5]
    EXTRA_PARAMS = sys.argv[6:] if len(sys.argv) > 6 else []

    # Prepare SonarCloud parameters
    sonar_params = {
        'sonar.branch.name': BRANCH,
        'sonar.token': SONAR_TOKEN
    }
    
    # Add any extra parameters (format: key=value)
    for param in EXTRA_PARAMS:
        if '=' in param:
            key, value = param.split('=', 1)
            sonar_params[key] = value

    # Trigger the workflow
    response = trigger_sonarcloud_analysis(
        github_token=GITHUB_TOKEN,
        owner=OWNER,
        repo=REPO,
        sonar_params=sonar_params
    )

    # Handle response
    if response.status_code == 204:
        print(f"✅ Successfully triggered SonarCloud analysis for {OWNER}/{REPO} on branch {BRANCH}")
        print(f"View actions: https://github.com/{OWNER}/{REPO}/actions")
    else:
        print(f"❌ Failed to trigger analysis. Status: {response.status_code}")
        print("Response:", response.text)

def trigger_sonarcloud_analysis(github_token: str, owner: str, repo: str, sonar_params: dict) -> requests.Response:
    """
    Trigger a GitHub Actions workflow that runs SonarCloud analysis
    
    Args:
        github_token: GitHub personal access token with repo scope
        owner: Repository owner
        repo: Repository name
        sonar_params: Dictionary of SonarCloud parameters
        
    Returns:
        requests.Response: The response from GitHub API
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/dispatches"
    
    headers = {
        "Accept": "application/vnd.github.v3+json",
        "Authorization": f"token {github_token}",
    }
    
    payload = {
        "event_type": "run-sonarcloud-analysis",
        "client_payload": sonar_params
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        return response
    except requests.exceptions.RequestException as e:
        print(f"⚠️ Error making request: {e}")
        raise

if __name__ == "__main__":
    main()
