import selenium as se
import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.chrome.options import Options
import io
import json
import base64
import re
from discord.ext import tasks

import sys
import os
import time
import random
import discord
import asyncio
from selenium import webdriver
import time
import re
from selenium.webdriver.common.by import By
from pyvirtualdisplay import Display
from selenium.webdriver.chrome.options import Options
from discord.ext import commands
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

driver = webdriver.Firefox()
display = Display(visible=0, size=(800, 600))
display.start()

client = discord.Client()

prev_game = ''
def read_last():
    with open("last_patch", "r") as f:
        last_message = f.read()
    f.close()
    return last_message

def write_last(message):
    with open("last_patch", "w") as f:
        f.write(message)
    f.close()


def steamdb_fetch():
    global prev_game
    driver.get("https://steamdb.info/patchnotes/")
    # Wait for the page to load
    time.sleep(2)
    # Finds the latest patch notes on SteamDB
    game = driver.find_element(By.CLASS_NAME, "app")
    patchnotes = game.find_element(By.XPATH, "//td[4]/a").get_attribute("href")
    patchtitle = game.find_element(By.XPATH, "//td[4]/a").text
    app = game.find_element(By.XPATH, "//td[3]/a").get_attribute("href")
    gametitle = game.find_element(By.XPATH, "//td[3]/a").text

    playercount = driver.get(app)
    playercount = driver.find_element(By.CLASS_NAME, "app").click()
    playercount = driver.find_element(By.CLASS_NAME, "header-thing.header-thing-poor").get_attribute("innerHTML")
    # Find class header-thing-number in the html of pnotes and print it
    playercount = re.findall(r'<div class="header-thing-number">(.*?)</div>', playercount)
    playercount = playercount[0]
    # Turn pnotes from an array to a string
    playercount = str(playercount)
    if int(playercount) != "" and prev_game != gametitle: #Edit this to change the minimum player count
        prev_game = gametitle
        string = "The latest patch notes for " + gametitle + " are: " + patchtitle + " " + patchnotes + " " + str(playercount) + " players"
        return string
    else:
        print("No new patch notes")
        return None


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))
    publish_patch.start()


@tasks.loop(seconds=30.0)
async def publish_patch():
    await client.wait_until_ready()
    channels = [931872099428098088, 931867043198812180]
    var = steamdb_fetch()
    for i in channels:
        channel = client.get_channel(i)
        if var:
            await channel.send(var)


@client.event

async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith('!about'):
        await message.channel.send('This bot is made by Pathegon#9079 for random stuff')


client.run('OTMxODQ3NjcxMjczMTE1NzQ4.YeKYxQ.U-x1lN-r6M2vBn2ltw7c8Rl_FXE')


