import instaloader
import logging
import os
import telegram
from telegram.ext import CommandHandler, Updater

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s," 
)
logger = logging.getLogger()

logger.info('Getting connection with instaloader')
L = instaloader.Instaloader(download_comments=False, max_connection_attempts=9, post_metadata_txt_pattern=None, save_metadata=False, download_video_thumbnails=False, download_geotags=False, filename_pattern="{shortcode}")

logger.info('Connected successfully')

PROFILES = ["checkandplay", "instantgaminges", "levelupcom", "3djuegos"]

TOKEN = os.getenv("TOKEN") #get bot token

def getStart(update, context):
    bot = context.bot
    chatId = update.message.chat_id

    try:
        for PROFILE in PROFILES:
            logger.info(f'Profile = {PROFILE}')                                
            profile = instaloader.Profile.from_username(L.context, PROFILE) #connect with the profile
            logger.info('Profile loaded')
            i = 0
            for post in profile.get_posts(): #get posts of the profile                          
                #time.sleep(5)                
                i+=1
                download = L.download_post(post,PROFILE)#download post
                if download==True: #the download has been successfully
                    video = post.is_video #verify if the post is a video                    
                    if video==True:                        
                        try:
                            with open(post.owner_username+'/'+post.shortcode+'.mp4' , 'rb') as f: #read the file with post
                                bot.send_video(chat_id=chatId, video=f) #send the video to the chat
                                if post.caption == None: #if the post has no description
                                    bot.sendMessage(chat_id=chatId, parse_mode='HTML', text=f'<b>{post.owner_username}:</b> None')
                                else: #send message with post description
                                    bot.sendMessage(chat_id=chatId, parse_mode='HTML', text=f'<b>{post.owner_username}:</b> {post.caption}')                                
                        except:
                            pass   
                    else: #the post is an image
                        try:
                            with open(post.owner_username+'/'+post.shortcode+'.jpg' , 'rb') as f:
                                bot.send_photo(chat_id=chatId, photo=f) #send image
                                if post.caption == None:
                                    bot.sendMessage(chat_id=chatId, parse_mode='HTML', text=f'<b>{post.owner_username}:</b> None')
                                else: #send post description
                                    bot.sendMessage(chat_id=chatId, parse_mode='HTML', text=f'<b>{post.owner_username}:</b> {post.caption}')                                
                        except:
                            pass    
                if i == 2:
                    break                

            logger.info('Next profile')                    

    except:
        pass
        

def pong(update,context):
    bot = context.bot
    chatId = update.message.chat_id

    bot.sendMessage(chat_id=chatId, text="pong")



if __name__ == "__main__":
    myBot = telegram.Bot(token=TOKEN) #connect with telegram bot

updater = Updater(myBot.token, use_context=True) #to get info sent to the bot
dp = updater.dispatcher

dp.add_handler(CommandHandler("start", getStart)) #set command
dp.add_handler(CommandHandler("ping", pong)) #set command

updater.start_polling()
print('BOT RUNNING')
updater.idle()

