import requests
import time
import json

# 从github.json读取配置
with open('github.json', 'r') as f:
    config = json.load(f)

token = config['token']
username = config['username']
package_type = "container"
is_org = config.get('is_org', False)

headers = {
    "Authorization": f"token {token}",
    "Accept": "application/vnd.github.v3+json"
}

# 构建API URL
if is_org:
    base_url = f"https://api.github.com/orgs/{username}"
else:
    base_url = f"https://api.github.com/users/{username}"

# 获取要删除的包列表
packages = config['packages']

print(f"Will delete {len(packages)} packages: {packages}")

# 删除指定的包
for package_name in packages:
    try:
        print(f"Processing {package_name}...")

        # 获取并删除所有版本
        versions_response = requests.get(
            f"{base_url}/packages/{package_type}/{package_name}/versions?per_page=100",
            headers=headers
        )
        versions = versions_response.json()
        print(f"  Found {len(versions)} versions")

        # 删除所有版本
        for version in versions:
            version_id = version["id"]
            delete_response = requests.delete(
                f"{base_url}/packages/{package_type}/{package_name}/versions/{version_id}",
                headers=headers
            )
            print(f"  Version {version_id} deletion status: {delete_response.status_code}")
            time.sleep(0.5)

        # 删除整个包
        print(f"  Deleting package {package_name}...")
        package_delete_response = requests.delete(
            f"{base_url}/packages/{package_type}/{package_name}",
            headers=headers
        )
        print(f"  Package {package_name} deletion status: {package_delete_response.status_code}")
        time.sleep(1)

    except Exception as e:
        print(f"Error processing package: {e}")
        continue

print("Deletion process completed.")