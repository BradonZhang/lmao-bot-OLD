#NOTE: This is quite an old version of my code, and the bot does a lot more now.

import discord
import asyncio

client = discord.Client()
toggle_ass = True           # If this is enabled, lmao-bot responds to "lmao" and "lmfao" in chat.
custom_cmd_list = {}        # Associative array for storing custom commands.

#TO-DO LIST
#Make lmao-bot also do reactions
#Make lmao-bot send a random SFW booty pic (animated characters, probs from Smash or something)
#Make moon function for mooning other people on the server with a SFW booty pic
#Create the count function

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')
    await client.change_presence(game=discord.Game(name=r'lmao help'))

@client.event
async def on_message(message):
    if message.author != client.user:
        msg = message.content.lower()
        cmd = msg[5:] # The command that lmao bot responds to when called
        mention = message.author.mention
        replace_ass_msg = mention + ' You appear to have misplaced your ass while laughing. Here is a replacement: :peach:'
        async def replace_ass():    # Sends the ass substitution message
            tmp = await client.send_message(message.channel, replace_ass_msg)
        if msg.startswith("lmao "): # Bot reacts to lmao call
            async def cmd_switch(command):
                async def cmd_toggle_ass(): # Toggle whether automatic ass substitution happens or not
                    global toggle_ass
                    toggle_ass = not toggle_ass
                    if toggle_ass:
                        tmp = await client.send_message(message.channel, 'Automatic ass substitution has been enabled. Hold onto your buns.')
                    else:
                        tmp = await client.send_message(message.channel, 'Automatic ass substitution has been disabled. Don\'t do anything reckless.')
                    return 'toggle_ass'
                async def cmd_help():   # DMs list of commands
                    dm_help = """**Full list of lmao-bot commands:**
                                 \n
                                 \n**lmao help**: Returns a list of commands for lmao-bot (hey, that's meta).
                                 \n**lmao toggleass**: Toggles the automatic ass replacement after someone laughs their ass off. Default is on.
                                 \n**lmao asstoggle**: Does the same thing as lmao toggleass.
                                 \n**lmao count**: Counts the number of times you have used \"lmao\" or \"lmfao\". (This function is not yet available.)
                                 \n**lmao ping**: Returns \"pong\".
                                 \n
                                 \n**rofl add** *command_name* *command_text*: Adds *command_name* (you can make the name something else) as a custom command, which reads *command_text* when executed.
                                 \n**rofl edit** *command_name* *command_text*: Edits a certain command, *command_name*, to instead print *command_text* when executed.
                                 \n**rofl delete** *command_name*: Deletes a certain command, *command_name*.
                                 \n**rofl list**: Lists all custom commands.
                                 \n**rofl** *command_name*: Prints the message associated with the custom command *command_name*."""
                    tmp = await client.send_message(message.author, dm_help)
                    tmp = await client.send_message(message.channel, 'A full list of lmao-bot commands has been slid into your DMs. :mailbox_with_mail:')
                    return 'help'
                async def cmd_count():  # Not built yet, but will count number of times someone says lmao
                    tmp = await client.send_message(message.channel, 'The count function is not yet available.')
                    return 'count'
                async def cmd_ping():   # Ping-Pong
                    tmp = await client.send_message(message.channel, ':ping_pong: Pong')
                    return 'ping'
                async def cmd_default():    # If the message isn't a command but just a regular "lmao" statement
                    if toggle_ass:
                        await replace_ass()
                    return 'default'
                cmd_case = {    # Dictionary for commmands
                    "help": cmd_help,
                    "toggleass": cmd_toggle_ass,
                    "asstoggle": cmd_toggle_ass,
                    "count": cmd_count,
                    "ping": cmd_ping,
                    "default": cmd_default
                }
                #cmd_msg = await cmd_case[cmd]()
                cmd_call = cmd_case.get(cmd, cmd_case.get('default'))
                #cmd_call = cmd_case.get(cmd, lambda: cmd_msg('default'))
                #cmd_msg = await cmd_case[cmd_call]()
                #tmp = await client.send_message(message.channel, await cmd_call())
                await cmd_call()
            await cmd_switch(cmd)
        elif msg.startswith("rofl "):   # Custom command functions
            #tmp = await client.send_message(message.channel, "Clean that floor once you're done.")
            msg_raw = message.content
            rofl_cmd_full = msg_raw[5:]
            first_space_ind = rofl_cmd_full.find(' ') # separate main command from command parameters
            #tmp = await client.send_message(message.channel, first_space_ind)
            if (first_space_ind == -1):
                rofl_cmd = rofl_cmd_full
            else:
                rofl_cmd = rofl_cmd_full[:first_space_ind]
            #tmp = await client.send_message(message.channel, "rofl_cmd equals " + rofl_cmd)
            async def rofl_switch(command):
                global custom_cmd_list
                async def rofl_add():   #adds custom command
                    custom_cmd = rofl_cmd_full[4:]
                    space_ind = custom_cmd.find(' ')
                    if (space_ind == -1):
                        tmp = await client.send_message(message.channel, "You must include the following components to the command: lmao add command_name command_text")
                    else:
                        custom_cmd_name = custom_cmd[:space_ind]
                        custom_cmd_text = custom_cmd[space_ind + 1:]
                        #tmp = await client.send_message(message.channel, space_ind)
                        #tmp = await client.send_message(message.channel, "Your command name: " + custom_cmd_name)
                        #tmp = await client.send_message(message.channel, "Your command text: " + custom_cmd_text)
                        #tmp = await client.send_message(message.channel, 'Add is not yet available.')
                        if custom_cmd_name in custom_cmd_list:
                            tmp = await client.send_message(message.channel, custom_cmd_name + " already exists as a command.")
                        else:
                            custom_cmd_list[custom_cmd_name] = custom_cmd_text
                            tmp = await client.send_message(message.channel, custom_cmd_name + " added as a custom command.")
                        #custom_cmd_list[custom_cmd]
                    return 'rofl_add'
                async def rofl_edit():  #edits existing custom command
                    custom_cmd = rofl_cmd_full[5:]
                    space_ind = custom_cmd.find(' ')
                    if (space_ind == -1):
                        tmp = await client.send_message(message.channel, "You must include the following components to the command: lmao edit command_name new_command_text")
                    else:
                        custom_cmd_name = custom_cmd[:space_ind]
                        custom_cmd_text = custom_cmd[space_ind + 1:]
                        if custom_cmd_name in custom_cmd_list:
                            custom_cmd_list[custom_cmd_name] = custom_cmd_text
                            tmp = await client.send_message(message.channel, custom_cmd_name + " custom command updated.")
                        else:
                            tmp = await client.send_message(message.channel, custom_cmd_name + " does not exist as a command.")
                    #tmp = await client.send_message(message.channel, 'Edit is not yet available.')
                    return 'rofl_edit'
                async def rofl_delete():    #deletes existing custom command
                    custom_cmd = rofl_cmd_full[7:]
                    if custom_cmd in custom_cmd_list:
                        deleted_cmd_text = custom_cmd_list[custom_cmd]
                        del custom_cmd_list[custom_cmd]
                        tmp = await client.send_message(message.channel, custom_cmd + " custom command deleted. It originally printed: " + deleted_cmd_text)
                    else:
                        tmp = await client.send_message(message.channel, custom_cmd + " does not exist as a command.")
                    #tmp = await client.send_message(message.channel, 'Delete is not yet available.')
                    return 'rofl_delete'
                async def rofl_list():  # lists all custom commands
                    custom_cmd_list_text = "**Full list of custom commands:**\n"
                    #tmp = await client.send_message(message.channel, "**Full list of custom commands:**")
                    for custom_cmd_key in custom_cmd_list.keys():
                        custom_cmd_list_text += "\n**" + custom_cmd_key + ":** " + custom_cmd_list[custom_cmd_key]
                    tmp = await client.send_message(message.channel, custom_cmd_list_text)
                    #tmp = await client.send_message(message.channel, 'List is not yet available.')
                    return 'rofl_list'
                async def rofl_custom():    # triggers custom command
                    #tmp = await client.send_message(message.channel, 'Custom is not yet available.')
                    tmp = await client.send_message(message.channel, custom_cmd_list[rofl_cmd])
                    return 'rofl_custom'
                rofl_case = {   # dictionary for rofl commands
                    "add": rofl_add,
                    "edit": rofl_edit,
                    "delete": rofl_delete,
                    "list": rofl_list,
                    "custom": rofl_custom
                }
                rofl_call = rofl_case.get(rofl_cmd, rofl_case.get('custom'))
                await rofl_call()
            await rofl_switch(rofl_cmd)
        elif ('lmao' in msg or 'lmfao' in msg) and toggle_ass: #generic ass substitution
            await replace_ass()

#INSERT YOUR BOT'S TOKEN IN THE QUOTATION MARKS BELOW
token = ""
client.run(token)
