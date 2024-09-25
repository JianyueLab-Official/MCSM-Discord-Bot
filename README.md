[![Color logo - no background.png](https://pic.awa.ms/f/1/65ed96d8606e6/65ed96d8606e6.png)](https://awa.ms)
# MCSM - Discord - Bot

## Usage & Development

### TO DO LIST:

- [ ] Instance List
- [ ] User Control
- [ ] Node Control & Details
- [ ] etc.

### Requirements:

- Python
- Discord Bot API
- MCSM Panel

### Run the project

```bash
// install requirements for running bot
pip3 install -r requirements.txt

python __init__.py
```

- Copy `.env.sample` to `.env` and fill all the blanks.

### Important

This bot DOES NOT PROVIDE ANY ROLE LIMITATION which EVERYONE in your server will have PERMISSION to send command. Please limit bot in your server's `server settins` -> `apps` -> `intergrations` -> `your bot name`, select roles and channel that allow for sending commands.


## How to create a discord bot and get api?
1. Go to [Discord Developer Panel](https://discord.com/developers), login your discord account.
![discord developer panel](/images/discord_dev_panel.png)
2. Press button at right-top to create a new bot.
3. Go to installation page, and change the installation link to `None`.
![Installation](/images/installation.png)
4. After create bot, go to bot page and reset the token, copy and save that key to your env file.
![oauth](/images/bot_page.png)
5. Scroll down on the same page, you need disable `public bot` and grant permission for `Presence Intent`, `Server Members Intent`, `Message Content Intent`.
![privileges](/images/privileges.png)
6. Go to oauth page, select `bot` and `Administrator`, then scroll down it will generate you a link. Copy and paste link to the browser.
![oauth](/images/oauth1.png)
![oauth](/images/oauth2.png)

## Developers

![contributors](https://contrib.rocks/image?repo=JianyueLab-Official/MCSM-Discord-Bot)