# default log

預設 `log_name` 為 `default`

在呼叫 `activity()` 時可帶入參數做 log_name

```php
activity('other-log')->log("hi");

Activity::all()->last()->log_name; //returns 'other-log';
```

或是在 `LogsActivity` 的 trait 中，設定 `logName`

這個方式也可以在每個模型中都設定各自的 `logName` ，讓每個模型的記錄都有自己 logName

```php
protected static $logName = 'custom_log_name_for_this_model';
```

## 查 log_name

除了透過基本的查詢

```php
Activity::where('log_name' , 'other-log')->get(); //returns all activity from the 'other-log'
```

也可使用套件內名為 `inLog` 的 scope 查詢

```php
Activity::inLog('other-log')->get();

//you can pass multiple log names to the scope
Activity::inLog('default', 'other-log')->get();

//passing an array is just as good
Activity::inLog(['default', 'other-log'])->get();
```
