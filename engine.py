# -*- coding: utf-8 -*-
import subprocess
import sys
import configparser


class Engine(object):
    def __init__(self, rnr):
        super(Engine, self).__init__()
        self.logic_cmd = rnr.logic_cmd
        self.logic_wrkdr = rnr.logic_wrkdr
        self.my_bot_cmd = rnr.mybot_cmd
        self.my_bot_wrkdr = rnr.mybot_wrkdr
        self.enemy_bot_cmd = rnr.enemybot_cmd
        self.enemy_bot_wrkdr = rnr.enemybot_wrkdr

    def set_logic_standard_io(self):
        self.process_logic = subprocess.Popen(self.logic_cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, cwd=self.logic_wrkdr)
        self.logic_stdin, self.logic_stdout = self.process_logic.stdin, self.process_logic.stdout

    def set_my_bot_standard_io(self):
        self.process_mybot = subprocess.Popen(self.my_bot_cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, cwd=self.my_bot_wrkdr)
        self.mybot_stdin, self.mybot_stdout = self.process_mybot.stdin, self.process_mybot.stdout

    def set_enemy_bot_standard_io(self):
        self.process_enemybot = subprocess.Popen(self.enemy_bot_cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE, cwd=self.enemy_bot_wrkdr)
        self.enemybot_stdin, self.enemybot_stdout = self.process_enemybot.stdin, self.process_enemybot.stdout

    def run(self):
        self.set_logic_standard_io()
        self.set_my_bot_standard_io()
        self.set_enemy_bot_standard_io()

        do_turn = True
        while do_turn == True:
            do_turn = self.make_turn()

    def communicate_logic(self):
        self.logic_stdin.write(("go enemy\n").encode())
        self.logic_stdin.flush()
        logic_orders = []

        line = self.logic_stdout.readline().decode().replace("\n", "")
        #enemy_orders.append(map(int, line.split(" ")))
        logic_orders.append(line)

        return logic_orders

    def communicate_enemy_bot(self, logic_orders):
        self.enemybot_stdin.write((logic_orders + '\n').encode())
        self.enemybot_stdin.flush()
        enemy_orders = []

        line = self.enemybot_stdout.readline().decode().replace("\n", "")
        #enemy_orders.append(map(int, line.split(" ")))
        enemy_orders.append(line)

        return enemy_orders

    def communicate_my_bot(self, logic_orders):
        self.mybot_stdin.write((logic_orders + '\n').encode())
        self.mybot_stdin.flush()
        mybot_orders = []

        line = self.mybot_stdout.readline().decode().replace("\n", "")

        #mybot_orders.append(map(int, line.split(" ")))
        mybot_orders.append(line)

        return mybot_orders

    def make_turn(self):
        logic_orders = self.communicate_logic()
        if str(logic_orders) == 'cmd stop':
            self.process_mybot.kill()
            self.process_enemybot.kill()
            self.process_logic.kill()
            print('stop')
            return False

        print(list(logic_orders))
        enemy_orders = self.communicate_enemy_bot(''.join(logic_orders))
        print(list(enemy_orders))
        mybot_orders = self.communicate_my_bot(''.join(logic_orders))
        print(list(mybot_orders))

        return True


class Runner(object):
    def __init__(self, cfg):
        self.logic_cmd = cfg.get_option('scene', 'scene_cmd')
        self.logic_wrkdr = cfg.get_option('scene', 'scene_wrkdr')
        self.mybot_cmd = cfg.get_option('mybot', 'mybot_cmd')
        self.mybot_wrkdr = cfg.get_option('mybot', 'mybot_wrkdr')
        self.enemybot_cmd = cfg.get_option('enemybot', 'enemybot_cmd')
        self.enemybot_wrkdr = cfg.get_option('enemybot', 'enemybot_wrkdr')

    def play(self):
        engine = Engine(self)
        engine.run()

    def run(self):
        self.play()
        print('End game')


class ConfigApp(object):
    def __init__(self):
        self.__name_config_file = ''
        self.__mybot_cmd = ''
        self.__enemybot_cmd = ''
        self.__conf = configparser.RawConfigParser()

    def make_sample(self):
        '''make sample config'''
        #conf = configparser.RawConfigParser()

        self.__conf.set("", "name", "Name sample")

        self.__conf.add_section("scene")
        self.__conf.set("scene", "scene_cmd", "scenes\scene_sample.py")

        self.__conf.add_section("mybot")
        self.__conf.set("mybot", "mybot_cmd", "scenes\mybot\mybot_sample.py")

        self.__conf.add_section("enemybot")
        self.__conf.set("enemybot", "enemybot_cmd", "scenes\enemybot\enemybot_sample.py")

        self.__conf.write(open("sample_config.conf", "w"))
        print("Make sample config. Name: sample_config.conf")

    def get_config(self, name_config):
        '''get config from file'''
        self.__name_config_file = name_config
        self.__conf.read(self.__name_config_file)
        if not self.__conf.has_option("", "name") or not self.__conf.has_section("scene")\
                or not self.__conf.has_section("mybot") or not self.__conf.has_section("enemybot"):
            print("Wrong config file!")
            return False
        else:
            return True

    def get_usage(self):
        '''print usage command'''
        print('''usage:\n--make-sample-config  -  make sample config\n''')

    def get_option(self, section, option):
        '''get option from config'''
        result = self.__conf.get(section, option)
        return result


def main():
    args = sys.argv
    cfg = ConfigApp()
    if len(args) == 1:  # запуск без аргументов. Вывести описание возможных аргументов.
        cfg.get_usage()
        return

    if args[1] == "--make-sample-config":   # пользователь попросил создать пример конфигурационного файла
        cfg.make_sample()
        return
    else:
        if cfg.get_config(args[1]):
            try:
                runner = Runner(cfg)
                runner.run()
            except KeyboardInterrupt:
                return


if __name__ == "__main__":
    main()