## 紀錄模型的事件

在模型內引用 `Spatie\Activitylog\Traits\LogsActivity` 這個 trait, 讓套件自動在模型的 `created`、`updated`、`deleted` 的事件中做紀錄

同時可透過 `getActivitylogOptions` 函式來控制需要紀錄的屬性

```
use Illuminate\Database\Eloquent\Model;
use Spatie\Activitylog\Traits\LogsActivity;
use Spatie\Activitylog\LogOptions;

class NewsItem extends Model
{
    use LogsActivity;

    protected $fillable = ['name', 'text'];

    public function getActivitylogOptions(): LogOptions
    {
        return LogOptions::defaults()
        // 可用 "*" 來紀錄任何有修改的屬性
        // 設定之後，不管屬性內的資料是否有變更都會紀錄下來
        // Chain fluent methods for configuration options
        ->logOnly(['name', 'text']);
    }
}
```

### 紀錄的基本設定

`logFillable` 能紀錄所有設定在 $fillable 中的屬性
```
LogOptions::defaults()->logFillable();
```

或是使用 `logUnguarded` 來紀錄不在 $guarded 中的屬性
```
LogOptions::defaults()->logUnguarded();
```

### 記錄資料的基本樣式
當產生一筆記錄後，會出現以下資料
```
$newsItem = NewsItem::create([
   'name' => 'original name',
   'text' => 'Lorum'
]);

//creating the newsItem will cause an activity being logged
$activity = Activity::all()->last();

$activity->description; //returns 'created'
$activity->subject; //returns the instance of NewsItem that was created
$activity->changes; //returns ['attributes' => ['name' => 'original name', 'text' => 'Lorum']];
```
然後更改資料後
```
$newsItem->name = 'updated name';
$newsItem->save();

//updating the newsItem will cause an activity being logged
$activity = Activity::all()->last();

$activity->description; //returns 'updated'
$activity->subject; //returns the instance of NewsItem that was created
```
在呼叫 $activity->changes 時會得到這個陣列
```
[
   'attributes' => [
        'name' => 'updated name',
        'text' => 'Lorum',
    ],
    'old' => [
        'name' => 'original name',
        'text' => 'Lorum',
    ],
];
```

### 自定觸發的事件
可使用 `static $recordEvents` 設定觸發的事件
```
use Illuminate\Database\Eloquent\Model;
use Spatie\Activitylog\Traits\LogsActivity;

class NewsItem extends Model
{
    use LogsActivity;

    //only the `deleted` event will get logged automatically
    protected static $recordEvents = ['deleted'];
}
```

### 自定說明
在執行紀錄時，會自動產生記錄說明。也可透過 `->setDescriptionForEvent()` ，來自定想要產生的說明

但在 callback 中能拿到的只有 $eventName 而以，所以要怎麼用就看個人創意了
```
use Illuminate\Database\Eloquent\Model;
use Spatie\Activitylog\Traits\LogsActivity;
use Spatie\Activitylog\LogOptions;

class NewsItem extends Model
{
    use LogsActivity;

    protected $fillable = ['name', 'text'];

    public function getActivitylogOptions()
    {
        return LogOptions::defaults()
        ->setDescriptionForEvent(fn(string $eventName) => "This model has been {$eventName}");
    }
}
```

### 自定 log_name
使用 `useLogName` 能變更紀錄時的 log_name
```
use Illuminate\Database\Eloquent\Model;
use Spatie\Activitylog\Traits\LogsActivity;
use Spatie\Activitylog\LogOptions;

class NewsItem extends Model
{
    use LogsActivity;

    public function getActivitylogOptions()
    {
        return LogOptions::defaults()
        ->useLogName('system');
    }
}
```

### 略過某些屬性
`dontLogIfAttributesChangedOnly` 可用來設定要跳過不紀錄的屬性

預設 `updated_at` 是會紀錄的屬性，但會觸發紀錄的行為

所以可以把 `updated_at` 放進 `dontLogIfAttributesChangedOnly` 來避免觸發紀錄
```
use Illuminate\Database\Eloquent\Model;
use Spatie\Activitylog\Traits\LogsActivity;
use Spatie\Activitylog\LogOptions;

class NewsItem extends Model
{
    use LogsActivity;

    protected $fillable = ['name', 'text'];

    public function getActivitylogOptions()
    {
        return LogOptions::defaults()
        ->logOnly(['name', 'text'])
        ->dontLogIfAttributesChangedOnly(['text']);
    }
}
```

### 只紀錄有更改的屬性
`->logOnly()` 是會紀錄每個設定在裡面的屬性，而 `->logOnlyDirty()` 是只紀錄有變更的屬性

```
use Illuminate\Database\Eloquent\Model;
use Spatie\Activitylog\Traits\LogsActivity;
use Spatie\Activitylog\LogOptions;

class NewsItem extends Model
{
    use LogsActivity;

    protected $fillable = ['name', 'text'];

    public function getActivitylogOptions()
    {
        return LogOptions::defaults()
        ->logOnly(['name', 'text'])
        ->logOnlyDirty();
    }
}
```

### 紀錄關聯的模型或 json 資料
可以使用 `.` 來紀錄關聯的模型，或用 `->` 來紀錄 json 資料

```
use Illuminate\Database\Eloquent\Model;
use Spatie\Activitylog\Traits\LogsActivity;
use Spatie\Activitylog\LogOptions;

class NewsItem extends Model
{
    use LogsActivity;

    protected $fillable = ['name', 'text', 'user_id'];

    public function getActivitylogOptions()
    {
        return LogOptions::defaults()
        ->logOnly(['name', 'text', 'user.name']);
    }

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}
```
```
use Illuminate\Database\Eloquent\Model;
use Spatie\Activitylog\Traits\LogsActivity;

class NewsItem extends Model
{
    use LogsActivity;

    protected $fillable = ['preferences', 'name'];

    protected $casts = [
        'preferences' => 'collection' // casting the JSON database column
    ];

    public function getActivitylogOptions()
    {
        return LogOptions::defaults()
        ->logOnly(['preferences->notifications->status', 'preferences->hero_url']);
    }

}
```

### 防止存到空記錄
當執行完一堆略過的行為，要紀錄的屬性可能已經沒了，變成空記錄

這時可以使用 `dontSubmitEmptyLogs` 來結束後續的儲存，避免儲了一筆空記錄
```
use Illuminate\Database\Eloquent\Model;
use Spatie\Activitylog\Traits\LogsActivity;
use Spatie\Activitylog\LogOptions;

class NewsItem extends Model
{
    use LogsActivity;

    protected $fillable = ['name', 'text'];

   public function getActivitylogOptions()
    {
        return LogOptions::defaults()
        ->logOnly(['text'])
        ->logOnlyDirty()  // 略過或只要的行為是疊加上去的，所以可能產生空記錄
        ->dontSubmitEmptyLogs();
    }
}
```

### 使用者的行為

套件有提供 `CausesActivity` 讓 User 查詢之前的相關行為
```
\Auth::user()->actions;
```

### 停止/啟用記錄
```
$newsItem = NewsItem::create([
   'name' => 'original name',
   'text' => 'Lorum'
]);

// Updating with logging disabled
$newsItem->disableLogging();

$newsItem->update(['name' => 'The new name is not logged']);
```
然後可再呼叫 `enableLogging` 再次啟動記錄行為

也可以使用 `withoutLogs()`
```
activity()->withoutLogs(function () {
    // ...
});
```

### 完成記錄前的事件

建立 `tapActivity()` 函式，能在記錄完成之前再執行一些事情
```
use Illuminate\Database\Eloquent\Model;
use Spatie\Activitylog\Traits\LogsActivity;
use Spatie\Activitylog\Contracts\Activity;

class NewsItem extends Model
{
    use LogsActivity;

    public function tapActivity(Activity $activity, string $eventName)
    {
        // 在此調整記錄的說明
        // 比透過 setDescriptionForEvent() 能拿到更多的參數
        $activity->description = "activity.logs.message.{$eventName}";
    }
}
```

