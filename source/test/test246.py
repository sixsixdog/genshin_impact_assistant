from source.map.map import genshin_map
from source.funclib import movement
from source.interaction.interaction_core import itt
from source.util import *

# movement.change_view_to_angle(50)
def test(x):
    time.sleep(0.1)
    a1 = genshin_map.get_rotation()
    itt.move_to(x,0,relative=True)
    time.sleep(0.1)
    a2 = genshin_map.get_rotation()
    return diff_angle(a2,a1)

def sometest(x):
    a=test(x)
    b=test(x)
    c=test(x)
    logger.critical(f"{x},{a},{b},{c},{(a + b + c) / 3}")

for i in range(1,200):
    sometest(i*10)