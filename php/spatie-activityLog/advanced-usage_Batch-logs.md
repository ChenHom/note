# 批次記錄

批次記錄，最常用的到記錄方式。

因為有些操作記錄是有相關性，屬於同一組一起查看才能知道脈絡，就會需要一個 `uuid` 將相關的記錄串在一起

```php
use Spatie\Activitylog\Facades\LogBatch;
use Spatie\Activitylog\Models\Activity;

// start 後，會產生一組 uuid 
// 後續的所有操作在停止之前都會記錄同一組 uuid 跟 causer
LogBatch::startBatch();
$author = Author::create(['name' => 'Philip K. Dick']);
$book = Book::create(['name' => 'A Scanner Brightly', 'author_id' => $author->id]);
$book->update(['name' => 'A Scanner Darkly']);
$author->delete();
// 取得目前的 uuid 
$batchUuid = LogBatch::getUuid(); 
LogBatch::endBatch();

// 取得這一組的系列操作
$batchActivities = Activity::forBatch($batchUuid)->get();
```

在 batch 開始之後，就需注意不能再次 `startBatch()`，因為同時間只能存在一組 uuid

需 `endBatch()` 之後才能再次啟動 batch

```php
// 可檢查是否已啟動 batch
LogBatch::isOpen();
```

可使用 `LogBatch::setBatch($uuid)` 傳入 uuid 或是任何唯一、有辨識性的資料

## 在多個 job 或 request 中保持 LogBatch 的開啟

```php
use Spatie\Activitylog\Facades\LogBatch;
use Illuminate\Bus\Batch;
use Illuminate\Support\Str;

$uuid =  Str::uuid();

Bus::batch([
    // First job will open a batch
    new SomeJob('some value', $uuid), // pass uuid as a payload to the job
    new AnotherJob($uuid), // pass uuid as a payload to the job
    new WorkJob('work work work', $uuid), // pass uuid as a payload to the job
])->then(function (Batch $batch) {
    // All jobs completed successfully...
})->catch(function (Batch $batch, Throwable $e) {
    // First batch job failure detected...
})->finally(function (Batch $batch) use ($uuid) {
    // The batch has finished executing...
    LogBatch::getUuid() === $uuid // true
    LogBatch::endBatch();
})->dispatch();

// Later on..
Activity::forBatch($uuid)->get(); // all the activity that happend in the batch
```

```php
class SomeJob
{
    public function handle(string $value, string $batchUuid = null)
    {
        LogBatch::startBatch();
        if($batchUuid) LogBatch::setBatch($batchUuid);

        // other code ..
    }
}
```

## 使用 callback 執行 batch

```php
use Spatie\Activitylog\Facades\LogBatch;

LogBatch::withinBatch(function(string $uuid) {
    $uuid; // 5cce9cb3-3144-4d35-9015-830cf0f20691
    activity()->log('my message');
    $item = NewsItem::create(['name' => 'new batch']);
    $item->update(['name' => 'updated']);
    $item->delete();
});

Activity::latest()->get(); // batch_uuid: 5cce9cb3-3144-4d35-9015-830cf0f20691
```
