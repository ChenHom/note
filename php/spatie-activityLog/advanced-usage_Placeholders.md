## Using Placeholders
在設定上有 `:subject`、`:causer`、`:properties` 這三種參數能使用

然後這種設定方式`無法`在先前提到的 `LogActivity` 中使用
```
activity()
    ->performedOn($article)
    ->causedBy($user)
    ->withProperties(['laravel' => 'awesome'])
    ->log('The subject name is :subject.name, the causer name is :causer.name and Laravel is :properties.laravel');

$lastActivity = Activity::all()->last();
$lastActivity->description; //returns 'The subject name is article name, the causer name is user name and Laravel is awesome';
```
