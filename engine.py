# -*- coding: utf-8 -*-
import subprocess
import sys


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


def main():
    try:
        args = sys.argv
        assert len(args) > 2
        runner = Runner(*args[1:])
        runner.run()
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()