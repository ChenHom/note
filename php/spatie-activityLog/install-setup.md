# 安裝指令

```text
composer require spatie/laravel-activitylog
```

如果需透過別的資料庫連線寫紀錄的話

可在`.env`中指定連線方式

```text
ACTIVITY_LOGGER_DB_CONNECTION=another_connect
```

之後記得使用 `artisan config:clear` ，讓 config 的設定值重置

---

可以使用以下指令來公開 migration 檔案

```text
php artisan vendor:publish --provider="Spatie\Activitylog\ActivitylogServiceProvider" --tag="activitylog-migrations"
```

config 檔案則可用這個指令

```text
php artisan vendor:publish --provider="Spatie\Activitylog\ActivitylogServiceProvider" --tag="activitylog-config"
```

config 的內容可在這邊查詢

[config from Github](https://github.com/spatie/laravel-activitylog/blob/main/config/activitylog.php)
