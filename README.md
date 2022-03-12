# Timetable bot for my university
How to run:

``` docker-compose up --build ```

NOTE: использует модифицированный vk_wave

TODO: настроить секреты и перевести pickle в json


## Важно!!
- При добавлении новой модельки, её нужно импортнуть в refactor.base.binding
- При добавлении нового стейта, его надо импортнуть в __init__
