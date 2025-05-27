import requests
import time
import json
import sys

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

success_count = 0
error_count = 0

# 删除指定的包
for package_name in packages:
    try:
        print(f"Processing {package_name}...")

        # 获取包版本
        versions_response = requests.get(
            f"{base_url}/packages/{package_type}/{package_name}/versions?per_page=100",
            headers=headers
        )

        if versions_response.status_code != 200:
            print(f"  Failed to get versions: {versions_response.status_code}")
            print(f"  Response: {versions_response.text}")
            error_count += 1
            continue

        versions = versions_response.json()

        # 检查返回的是否为列表
        if not isinstance(versions, list):
            print(f"  Unexpected response format: {versions}")
            error_count += 1
            continue

        print(f"  Found {len(versions)} versions")

        # 删除所有版本
        version_errors = 0
        for version in versions:
            version_id = version["id"]
            delete_response = requests.delete(
                f"{base_url}/packages/{package_type}/{package_name}/versions/{version_id}",
                headers=headers
            )
            status = delete_response.status_code
            print(f"  Version {version_id} deletion status: {status}")

            if status not in [200, 204]:
                print(f"  Warning: Version deletion failed with status {status}")
                version_errors += 1

            time.sleep(0.5)

        # 删除整个包
        print(f"  Deleting package {package_name}...")
        package_delete_response = requests.delete(
            f"{base_url}/packages/{package_type}/{package_name}",
            headers=headers
        )
        pkg_status = package_delete_response.status_code
        print(f"  Package {package_name} deletion status: {pkg_status}")

        if pkg_status in [200, 204]:
            success_count += 1
            print(f"  ✅ Package {package_name} deleted successfully")
        else:
            error_count += 1
            print(f"  ❌ Package {package_name} deletion failed")

        time.sleep(1)

    except Exception as e:
        print(f"❌ Error processing package {package_name}: {e}")
        error_count += 1
        continue

print(f"\n=== 删除结果汇总 ===")
print(f"成功删除: {success_count} 个包")
print(f"删除失败: {error_count} 个包")
print(f"总计处理: {len(packages)} 个包")

if error_count > 0:
    print("❌ 删除过程中出现错误!")
    sys.exit(1)
else:
    print("✅ 所有包删除成功!")
    sys.exit(0)