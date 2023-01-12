在 cli 中登入 docker 除了直接在 cli 中輸入 docker login -u XXX，再輸入密碼外也可使用 `token` 的方式

這邊跳過說明 token 的申請方式，直接說重點

```
export DOCKER_REGISTRY_AUTH=$(cat credentials.json) docker login
```
```
{
    "auths": {
        "https://hub.docker.com/repository/docker/<user_name>/<image-repo>": {
            "auth": "docker_token"
        }
    }
}
```