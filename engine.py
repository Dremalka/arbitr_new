# -*- coding: utf-8 -*-
import subprocess
import sys
import configparser


class Engine(object):
    def __init__(self, mybot_cmd, enemybot_cmd):
        super(Engine, self).__init__()
        self.my_bot_cmd = mybot_cmd
        self.enemy_bot_cmd = enemybot_cmd

    def set_my_bot_standard_io(self):
        process = subprocess.Popen(self.my_bot_cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        self.mybot_stdin, self.mybot_stdout = process.stdin, process.stdout

    def set_enemy_bot_standard_io(self):
        process = subprocess.Popen(self.enemy_bot_cmd, shell=True, stdout=subprocess.PIPE, stdin=subprocess.PIPE)
        self.enemybot_stdin, self.enemybot_stdout = process.stdin, process.stdout

    def run(self):
        self.set_my_bot_standard_io()
        self.set_enemy_bot_standard_io()

        self.make_turn()

    def communicate_enemy_bot(self):
        self.enemybot_stdin.write(("go enemy\n").encode())
        self.enemybot_stdin.flush()
        enemy_orders = []

        line = self.enemybot_stdout.readline().decode().replace("\n", "")
        #enemy_orders.append(map(int, line.split(" ")))
        enemy_orders.append(line)

        return enemy_orders

    def communicate_my_bot(self):
        self.mybot_stdin.write(("go my bot\n").encode())
        self.mybot_stdin.flush()
        mybot_orders = []

        line = self.mybot_stdout.readline().decode().replace("\n", "")

        #mybot_orders.append(map(int, line.split(" ")))
        mybot_orders.append(line)

        return mybot_orders

    def make_turn(self):
        enemy_orders = self.communicate_enemy_bot()
        mybot_orders = self.communicate_my_bot()

        print(list(enemy_orders))
        print(list(mybot_orders))


class Runner(object):
    def __init__(self, mybot_cmd, enemybot_cmd):
        self.mybot_cmd = mybot_cmd
        self.enemybot_cmd = enemybot_cmd

    def play(self):
        engine = Engine(self.mybot_cmd, self.enemybot_cmd)
        engine.run()

    def run(self):
        self.play()
        print('End game')


class ConfigApp(object):
    def make_sample(self):
        '''make sample config'''
        conf = configparser.RawConfigParser()

        conf.set("", "name", "Name sample")

        conf.add_section("scene")
        conf.set("scene", "scene_cmd", "scenes\scene_sample.py")

        conf.add_section("mybot")
        conf.set("mybot", "mybot_cmd", "scenes\mybot\mybot_sample.py")

        conf.add_section("enemybot")
        conf.set("enemybot", "enemybot_cmd", "scenes\enemybot\enemybot_sample.py")

        conf.write(open("sample_config.conf", "w"))
        print("Make sample config. Name: sample_config.conf")

    def get_config(self, name_file):
        '''get config from file'''
        conf = configparser.RawConfigParser()
        conf.read(name_file)
        if not conf.has_option("", "name") or not conf.has_section("scene")\
                or not conf.has_section("mybot") or not conf.has_section("enemybot"):
            print("Wrong config file!")
            return False
        else:
            return True

    def get_usage(self):
        '''print usage command'''
        print('''usage:\n--make-sample-config  -  make sample config\n''')


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
            print("Config OK!")

#    try:
#        assert len(args) > 2
#        runner = Runner(*args[1:])
#        runner.run()
#    except KeyboardInterrupt:
#        return


if __name__ == "__main__":
    main()