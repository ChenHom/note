這是個基本用法
```
activity()->log('I logged something');
```

儲存的記錄可透過 `Activity` 這個模型查看

```
$lastLogged = Activity::all()->last();  // returns the last logged

$lastLogged->description; // returns 'I logged something'
```

---

### 設定記錄的來源模型

```
activity()->performedOn($someContentObject)  // 可以使用 "on" 函式代替 "performedOn"
    ->log('edited');

Activity()->latest()->first()->subject;  // subject 是 `performedOn` 傳遞進來的
```

### 設定記錄的觸發者

```
activity()
    ->causedBy($userModel)  // 可以使用 "by" 函式代替 "causedBy"
    ->performedOn($someContentObject)
    ->log('edited');

Activity()->latest()->first()->caused;  // caused 是 `causedBy` 傳遞進來的
```
不過就算沒有設定 `causedBy` 的話，套件也會自動記錄操作者
除非是使用 `causedByAnonymous` 或 `byAnonymous` ，來設定匿名

### 設定客製屬性

```
activity()
    ->causedBy($userModel)
    ->performedOn($someContentObject)
    ->withProperties(['key' => 'value])
    ->log('edited');

$lastActivity = Activity()->latest()->first();
$lastActivity->getExtraProperty('key'); // 返回 "value"
$lastActivity->where('property->key', 'value'); // 取得所有 `property` 中有 `key` 這個鍵且值為 `value` 的資料
```

### 設定客製 created date

使用 `createdAt` 調整 `created_at` 的時間
```
activity()
    ->causedBy($userModel)
    ->performedOn($someContentModel)
    ->createdAt(now()->subDays(10))
    ->log('created');
```

### 設定事件

設定這筆記錄是屬於什麼事件的, 以利後續的再次使用
```
activity()
    ->causedBy($userModel)
    ->performedOn($someContentModel)
    ->event('verified')
    ->log('The user has verified the content model.');
```

### 儲存前的 Tap

在儲存之前能再對 `Activity` 做處理
```
use Spatie\Activitylog\Contracts\Activity;

activity()
   ->causedBy($userModel)
   ->performedOn($someContentModel)
   ->tap(function(Activity $activity) {
      $activity->my_custom_field = 'my special value';
   })
   ->log('edited');

$lastActivity = Activity::all()->last();

$lastActivity->my_custom_field; // returns 'my special value'
```

---

## 清除 Log

可以執行這個指令清除 log
```
php artisan activitylog:clean  // 在自動化流程中，可以加 --force 來防止系統出現確認訊息
```
然後會依照 config 檔裡的 `delete_records_older_than_days` 設定的保存期限來清除

也可以使用 kernel 中的 schedule 來定時清除
```
//app/Console/Kernel.php

protected function schedule(Schedule $schedule)
{
   $schedule->command('activitylog:clean')->daily();
}
```

### 參數說明

```
// 清除 log_name 中是 my_log_channel 的資料
php artisan activitylog:clean my_log_channel 
```

```
// 保留 7 天內的資料
php artisan activitylog:clean --days=7
```

### 資料庫的清除後處理

可以在清除後使用 `optimize` 或 `analyze` 來重整資料表的空間

但需資料庫有支援這些相關功能
```
// 可使用 optimize
OPTIMIZE TABLE activity_log;

or

// 或 analyze 
ANALYZE TABLE activity_log;
```

