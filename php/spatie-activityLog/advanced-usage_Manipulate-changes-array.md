# 調整修正的陣列

在 v4 版本中，提供了新的方法來透過 `pipe` 達到調整與修正的能力

首先建立一個要放進 Pipe 的調整類別

在這類別在，會將 changes 裡的特定屬性移除

```php
// RemoveKeyFromLogChangesPipe.php

use Spatie\Activitylog\Contracts\LoggablePipe;
use Spatie\Activitylog\EventLogBag;

class RemoveKeyFromLogChangesPipe implements LoggablePipe
{
    public function __construct(protected string $field){}

    public function handle(EventLogBag $event, Closure $next): EventLogBag
    {
        Arr::forget($event->changes, ["attributes.{$this->field}", "old.{$this->field}"]);

        return $next($event);
    }
}
```

然後可以在 controller 或 job 或 middleware 中將上面的類別透過 `addLogChange` 塞進 pipe

```php
// ... in your controller/job/middleware

NewsItem::addLogChange(new RemoveKeyFromLogChangesPipe('name'));

$article = NewsItem::create(['name' => 'new article', 'text' => 'new article text']);
$article->update(['name' => 'update article', 'text' => 'update article text']);

Activity::all()->last()->changes();
/*
    'attributes' => [
        'text' => 'updated text',
    ],
    'old' => [
        'text' => 'original text',
    ]
*/
```
