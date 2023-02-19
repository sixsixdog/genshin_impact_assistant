
# from source.interaction import *

from source.util import *
from source.common import character
from source.funclib import combat_lib
from source.manager import asset
from source.operator.aim_operator import AimOperator
from source.common.base_threading import BaseThreading
from source.interaction.interaction_core import itt
from source.operator.switch_character_operator import SwitchCharacterOperator
from source.path_lib import CONFIG_PATH_SETTING

CHARACTER_DIED = 1

def sort_flag_1(x: character.Character):
    return x.priority


def stop_func_example():  # True:stop;False:continue
    return False


def get_chara_list(team_name='team.json'):
    team_name = load_json("auto_combat.json",CONFIG_PATH_SETTING)["teamfile"]
    d_path = "config\\tactic"
    
    team = load_json(team_name, default_path=d_path)
    characters = load_json("character.json", default_path=d_path)
    chara_list = []
    for team_name in team:
        team_item = team[team_name]
        if team_item["autofill"]:
            c_character = characters[team_item["name"]]
            c_position = c_character["position"]
            cE_short_cd_time = c_character["E_short_cd_time"]
            cE_long_cd_time = c_character["E_long_cd_time"]
            cElast_time = c_character["Elast_time"]
            cEcd_float_time = c_character["Ecd_float_time"]
            try:
                c_tactic_group = c_character["tactic_group"]
            except:
                c_tactic_group = c_character["tastic_group"]
                logger.warning(t2t("请将配对文件中的tastic_group更名为tactic_group. 已自动识别。"))
            cEpress_time = c_character["Epress_time"]
            cQlast_time = c_character["Qlast_time"]
            cQcd_time = c_character["Qcd_time"]
        else:
            c_position = team_item["position"]
            c_priority = team_item["priority"]
            cE_short_cd_time = team_item["E_short_cd_time"]
            cE_long_cd_time = team_item["E_long_cd_time"]
            cElast_time = team_item["Elast_time"]
            cEcd_float_time = team_item["Ecd_float_time"]
            try:
                c_tactic_group = team_item["tactic_group"]
            except:
                c_tactic_group = team_item["tastic_group"]
                logger.warning(t2t("请将配对文件中的tastic_group更名为tactic_group. 已自动识别。"))
            c_trigger = team_item["trigger"]
            cEpress_time = team_item["Epress_time"]
            cQlast_time = team_item["Qlast_time"]
            cQcd_time = team_item["Qcd_time"]

        cn = team_item["n"]
        cname = team_item['name']
        c_priority = team_item["priority"]
        c_trigger = team_item["trigger"]

        if cEcd_float_time > 0:
            logger.info(t2t("角色 ") + cname + t2t(" 的Ecd_float_time大于0，请确定该角色不是多段e技能角色。"))

        chara_list.append(
            character.Character(
                name=cname, position=c_position, n=cn, priority=c_priority,
                E_short_cd_time=cE_short_cd_time, E_long_cd_time=cE_long_cd_time, Elast_time=cElast_time,
                Ecd_float_time=cEcd_float_time, tactic_group=c_tactic_group, trigger=c_trigger,
                Epress_time=cEpress_time, Qlast_time=cQlast_time, Qcd_time=cQcd_time
            )
        )
    return chara_list


class Combat_Controller(BaseThreading):
    def __init__(self, chara_list=None):
        super().__init__()
        if chara_list is None:
            chara_list = get_chara_list()
        self.setName('Combat_Controller')

        self.chara_list = chara_list
        self.pause_threading_flag = False
        self.itt = itt

        self.sco = SwitchCharacterOperator(self.chara_list)
        self.sco.pause_threading()
        self.sco.add_stop_func(self.checkup_stop_func)
        self.sco.setDaemon(True)
        self.sco.start()

        self.ao = AimOperator()
        self.ao.pause_threading()
        self.ao.add_stop_func(self.checkup_stop_func)
        self.ao.setDaemon(True)
        self.ao.start()

        self.is_check_died = False
        
        # self.super_stop_func=super_stop_func

    def run(self) -> None:
        while 1:
            time.sleep(0.2)
            if self.checkup_stop_threading():
                self.ao.stop_threading()
                self.sco.stop_threading()
                return
            
            if self.is_check_died:
                if self.itt.get_img_existence(asset.character_died):
                    logger.info(t2t('有人嘎了，停止自动战斗'))
                    self.last_err_code = CHARACTER_DIED
                    while 1:
                        time.sleep(0.5)
                        r = self.itt.appear_then_click(asset.button_ui_cancel)
                        if r:
                            break
                    self.pause_threading()
            
            if not self.pause_threading_flag:
                if self.checkup_stop_func():
                    break

                if not self.sco.get_working_statement():
                    self.sco.continue_threading()
                    time.sleep(1)
                else:
                    time.sleep(0.2)

                if not self.ao.get_working_statement():
                    self.ao.continue_threading()
                else:
                    pass

            else:
                if self.sco.get_working_statement():
                    self.sco.pause_threading()
                    time.sleep(1)

                if self.ao.get_working_statement():
                    self.ao.pause_threading()
                    time.sleep(1)
                
                continue
                
            if self.checkup_stop_func():
                self.pause_threading_flag = True
                continue
            # print('6')
            # time.sleep(1)

    def checkup_stop_func(self):
        if self.pause_threading_flag or self.stop_threading_flag:
            logger.info(t2t('停止自动战斗'))
            return True
        
        
    def checkup_stop_threading(self):
        if self.stop_threading_flag:
            logger.info(t2t('停止自动战斗'))
            return True

    def continue_threading(self):
        if self.pause_threading_flag != False:
            self.current_num = combat_lib.get_current_chara_num(self.itt, self.checkup_stop_func)
            # self.current_num = 1
            self.pause_threading_flag = False
            self.sco.continue_threading()
            self.ao.continue_threading()

    def pause_threading(self):
        if self.pause_threading_flag != True:
            self.pause_threading_flag = True
            self.sco.pause_threading()
            self.ao.pause_threading()

    def checkup_trapped(self):
        pass
        # if self.itt.capture(posi=posiM)

    def stop_threading(self):
        self.stop_threading_flag = True


if __name__ == '__main__':
    cl = Combat_Controller()
    cl.start()
    # a = get_chara_list()
    # print()
