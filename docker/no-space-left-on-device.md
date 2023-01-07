在建立新專案時，docker 一直跳出這個訊息
```
docker: write /var/lib/docker/tmp/GetImageBlob1707749401: no space left on device.
```

但查看 containers、images、volumes 時均為清空狀態，一時之間不知該怎辦

於是上網查看解答

[Docker no space left on device](https://forums.docker.com/t/docker-no-space-left-on-device/69205/3)

除了 containers、images、volumes外，還有 system 也是會佔空間的

```
docker system prune
```

還我乾坤大地！
