## 在執行時期定義觸發者
```
// in a queue job or controller

use Spatie\Activitylog\Facades\CauserResolver;

// ... other code

$product = Product::first(1);
$causer = $product->owner;

CauserResolver::setCauser($causer);

$product->update(['name' => 'New name']);

Activity::all()->last()->causer; // Product Model
Activity::all()->last()->causer->id; // Product#1 Owner
```
或是透過 `resolver`
```
CauserResolver::resolve(fn() => User::find(2))
```
