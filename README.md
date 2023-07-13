# wargaming_test_task2

Solution for the test task. Used `pygame` library. Launch:

`python .\pathfinding.py -x 20 -y 20`

`x` and `y` is a width and height of the game map in game tiles. Default is 20 for both.

Change a position of the ship and the goal by dragging them with mouse

The task:

• Существует поле клеток размером M*N.

• Каждая клетка может быть либо сушей, либо водой.

• На поле находится плот размером в 1 клетку.

• Плот может двигаться только вверх, вниз, вправо и влево.

• Необходимо реализовать:

• Автогенерацию карты. Доля суши от площади поля - 30%.
Алгоритм генерации – произвольный.

• механизм поиска кратчайшего пути из точки A в точку B
на такой карте.

• Параметры M, N, и координаты точек A и B задаются
пользователем.