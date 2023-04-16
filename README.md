### ВОЙНА ВИРУСОВ

![alt text](https://github.com/SingularGamesStudio/VirusesPython/blob/dev/pictures/game_example.png?raw=true)

## Правила игры

В каждой клетке поля может находиться живой вирус одного из игроков или вирус, убитый одним из игроков (на начало игры у каждого игрока есть 1 живой вирус).

За ход игрок должен сделать 3 действия. Действием может быть либо убийство вируса противника в доступной клетке либо создание своего вируса в доступной клетке.

Клетка считается доступной для игрока А, если от неё до клетки с живым вирусом игрока А существует путь (возможно, пустой) из вирусов, убитых игроком А (клетки в пути соседствуют по вершине или ребру).

Игрок проигрывает, если он не может выполнить 3 действия в свой ход.

## Установка

* Выполнить './run.sh'

либо

* Установить библиотеки из 'requirements.txt' и выполнить 'python3 main.py'

## Интерфейс

Кнопки слева (сверху-вниз):

* Изменить число игроков
* Изменить размер поля
* Применить изменения игры
* Показать\скрыть доступные ходы

Кнопки справа (сверху-вниз):

* Изменить масштаб
* Отменить действие
* Сдаться
