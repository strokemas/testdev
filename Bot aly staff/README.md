# bot-discord-yellow

https://levelup.gitconnected.com/how-to-gather-message-data-using-a-discord-bot-from-scratch-with-python-2fe239da3bcd

```bash
mkdir /root/bot-authorized-keys && cd /root/bot-authorized-keys
ssh-keygen
# enregister la clé dans ./

useradd -m -U bot
su bot
bash
cd /home/bot && mkdir .ssh && cd .ssh && touch authorized_keys
# ajouter la clé dans le authorized_keys

ssh-keygen
# générer une clé pour ce user, l'authorized en deploy_key read_only sur le projet github

git clone git clone git@github.com:plasmachauvire8/bot-discord-yellow

exit
exit

apt install libffi-dev libnacl-dev python3-devpip
pip3 install gspread oauth2client python-dotenv discord
```

/etc/systemd/system/bot-discord.service :

```
[Unit]
Description=Yellow jack discord bot
After=multi-user.target
[Service]
User=bot
Group=bot
Type=simple
Restart=always
ExecStart=/bin/sh -c '/usr/bin/python3 -u /home/bot/bot-discord-yellow/message_reader.py 1>> /var/log/bot/bot.log 2>&1'
[Install]
WantedBy=multi-user.target
```

/etc/sudoers.d/bot-discord :
```
Cmnd_Alias BOT_STATUS = /usr/sbin/service bot-discord status
Cmnd_Alias BOT_RESTART = /usr/sbin/service bot-discord restart
Cmnd_Alias BOT_STOP = /usr/sbin/service bot-discord stop
Cmnd_Alias BOT_START = /usr/sbin/service bot-discord start
Cmnd_Alias BOT_LOGS = /usr/bin/journalctl -xe -u bot-discord

bot ALL=(root) NOPASSWD: BOT_STATUS,BOT_RESTART,BOT_STOP,BOT_START,BOT_LOGS
```

```
root@server:~# mkdir /var/log/bot
root@server:~# touch /var/log/bot/bot.log
root@server:~# chown bot:bot /var/log/bot/bot.log
root@server:~# systemctl daemon-reload
root@server:~# su bot
$ bash
bot@bluesea:/root$ sudo service bot-discord restart
```

=> Logrotate

```
root@bluesea:~# cat /etc/logrotate.d/bot
/var/log/bot/bot.log
/var/log/bot/bot-romandy.log
{
        daily
        missingok
        rotate 14
        compress
        delaycompress
        notifempty
        create 644 bot bot
        sharedscripts
}

```

Test bot : https://discord.com/api/webhooks/1036721802501689415/bADdOTxsKuuuY0ervIQWNWwVnw0VB1H24bB15Qyv9HKPOqzk1cr8Z8oTWvc3pAF36lLi

Send webhook : https://discord.com/api/webhooks/1036721802501689415/bADdOTxsKuuuY0ervIQWNWwVnw0VB1H24bB15Qyv9HKPOqzk1cr8Z8oTWvc3pAF36lLi

