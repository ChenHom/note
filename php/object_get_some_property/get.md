# Simulate the Laravel's data_get retrieval method to extract a piece of data.

```php
function get(array $o, string|array $paths) {
 if (!$o) {
  return $o;
 }
 if (!is_array($paths)) {
  preg_match_all('/[\w$]+/', $paths, $match);
  $paths = $match[0];
 }

 $count = count($paths);

 [$k, $paths] = [array_shift($paths), $paths];

 switch ($count) {
  case 0:
   return $o;
  case 1:
   return $o[$k];
  default:
   return get($o[$k], $paths);
 }
}

$data = [
    "id" => 34344,
    "detail" =>[
        "img" => "111111",
        "img2" =>  "222222"
    ]
];

var_dump(get($data, 'detail.img')); // return the '111111'
```
