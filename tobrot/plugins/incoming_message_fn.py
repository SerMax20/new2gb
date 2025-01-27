#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# (c) Shrimadhav U K | gautamajay52 | Akshay C

# the logging things
import logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
LOGGER = logging.getLogger(__name__)


import os

from tobrot import (
    DOWNLOAD_LOCATION
)


import time
import aria2p
import asyncio
from tobrot.helper_funcs.extract_link_from_message import extract_link
from tobrot.helper_funcs.download_aria_p_n import call_apropriate_function, call_apropriate_function_g, aria_start
from tobrot.helper_funcs.download_from_link import request_download
from tobrot.helper_funcs.display_progress import progress_for_pyrogram
from tobrot.helper_funcs.youtube_dl_extractor import extract_youtube_dl_formats
from tobrot.helper_funcs.admin_check import AdminCheck
        
async def incoming_purge_message_f(client, message):
    """/purge command"""
    i_m_sefg2 = await message.reply_text("Purging...", quote=True)
    if await AdminCheck(client, message.chat.id, message.from_user.id):
        aria_i_p = await aria_start()
        # Show All Downloads
        downloads = aria_i_p.get_downloads()
        for download in downloads:
            LOGGER.info(download.remove(force=True))
    await i_m_sefg2.delete()

async def incoming_message_f(client, message):
    """/leech command"""
    i_m_sefg = await message.reply_text("processing", quote=True)
    is_zip = False
    is_unzip = False
    is_unrar = False
    is_untar = False
    if len(message.command) > 1:
        if message.command[1] == "archive":
            is_zip = True
        elif message.command[1] == "unzip":
            is_unzip = True
        elif message.command[1] == "unrar":
            is_unrar = True
        elif message.command[1] == "untar":
            is_untar = True
    # get link from the incoming message
    dl_url, cf_name, _, _ = await extract_link(message.reply_to_message, "LEECH")
    LOGGER.info(dl_url)
    LOGGER.info(cf_name)
    if dl_url is not None:
        await i_m_sefg.edit_text("extracting links")
        # start the aria2c daemon
        aria_i_p = await aria_start()
        LOGGER.info(aria_i_p)
        current_user_id = message.from_user.id
        # create an unique directory
        new_download_location = os.path.join(
            DOWNLOAD_LOCATION,
            str(current_user_id),
            str(time.time())
        )
        # create download directory, if not exist
        if not os.path.isdir(new_download_location):
            os.makedirs(new_download_location)
        await i_m_sefg.edit_text("trying to download")
        # try to download the "link"
        sagtus, err_message = await call_apropriate_function(
            aria_i_p,
            dl_url,
            new_download_location,
            i_m_sefg,
            is_zip,
            cf_name,
            is_unzip,
            is_unrar,
            is_untar
        )
        if not sagtus:
            # if FAILED, display the error message
            await i_m_sefg.edit_text(err_message)
    else:
        await i_m_sefg.edit_text(
            "You Had Entered Wrong Way\nFor Downloading On Telegram,\nYou Can Use Following Command But All Command Should as Reply To Direct Download Link or Magnet Link 🧲 or .torrent File. \n● Download\n/leech - To Download File On Telegram.\n\n● Download With Compression\n<code>/leech archive<code/> - To Get Single Compressed File (Max Size:- 1.95GB).\n\n● Download With Decompression\n<code>/leech unzip<code/> - To Extract Files From .zip File.\n<code>/leech unrar<code/> - To Extract Files From .rar File.\n<code>/leech untar<code/> - To Extract Files From .tar File. \n"
            f"<b>API Error</b>: {cf_name}"
        )
#
async def incoming_gdrive_message_f(client, message):
    """/gleech command"""
    i_m_sefg = await message.reply_text("processing", quote=True)
    is_zip = False
    is_unzip = False
    is_unrar = False
    is_untar = False
    if len(message.command) > 1:
        if message.command[1] == "archive":
            is_zip = True
        elif message.command[1] == "unzip":
            is_unzip = True
        elif message.command[1] == "unrar":
            is_unrar = True
        elif message.command[1] == "untar":
            is_untar = True
    # get link from the incoming message
    dl_url, cf_name, _, _ = await extract_link(message.reply_to_message, "GLEECH")
    LOGGER.info(dl_url)
    LOGGER.info(cf_name)
    if dl_url is not None:
        await i_m_sefg.edit_text("extracting links")
        # start the aria2c daemon
        aria_i_p = await aria_start()
        LOGGER.info(aria_i_p)
        current_user_id = message.from_user.id
        # create an unique directory
        new_download_location = os.path.join(
            DOWNLOAD_LOCATION,
            str(current_user_id),
            str(time.time())
        )
        # create download directory, if not exist
        if not os.path.isdir(new_download_location):
            os.makedirs(new_download_location)
        await i_m_sefg.edit_text("trying to download")
        # try to download the "link"
        await call_apropriate_function_g(
            aria_i_p,
            dl_url,
            new_download_location,
            i_m_sefg,
            is_zip,
            cf_name,
            is_unzip,
            is_unrar,
            is_untar,
            message
        )
    else:
        await i_m_sefg.edit_text(
            "You Had Entered Wrong Way\nFor Uploading On G-Drive,\nYou Can Use Following Command But All Command Should as Reply To Direct Download Link or Magnet Link 🧲 or .torrent File. \n● Upload\n/gleech - To Download File On Telegram.\n\n● Upload With Compression\n<code>/gleech archive<code/> - To Get Single Compressed File (Max Size:- 1.95GB).\n\n● Upload With Decompression\n<code>/gleech unzip<code/> - To Extract Files From .zip File.\n<code>/gleech unrar<code/> - To Extract Files From .rar File.\n<code>/gleech untar<code/> - To Extract Files From .tar File. \n"
            f"<b>API Error</b>: {cf_name}"
        )


async def incoming_youtube_dl_f(client, message):
    """ /ytdl command """
    i_m_sefg = await message.reply_text("processing", quote=True)
    # LOGGER.info(message)
    # extract link from message
    dl_url, cf_name, yt_dl_user_name, yt_dl_pass_word = await extract_link(
        message.reply_to_message, "YTDL"
    )
    LOGGER.info(dl_url)
    if len(message.command) > 1:
        if message.command[1] == "gdrive":
            with open('blame_my_knowledge.txt', 'w+') as gg:
                gg.write("I am noob and don't know what to do that's why I have did this")
    LOGGER.info(cf_name)
    if dl_url is not None:
        await i_m_sefg.edit_text("extracting links")
        current_user_id = message.from_user.id
        # create an unique directory
        user_working_dir = os.path.join(DOWNLOAD_LOCATION, str(current_user_id))
        # create download directory, if not exist
        if not os.path.isdir(user_working_dir):
            os.makedirs(user_working_dir)
        # list the formats, and display in button markup formats
        thumb_image, text_message, reply_markup = await extract_youtube_dl_formats(
            dl_url,
            # cf_name,
            yt_dl_user_name,
            yt_dl_pass_word,
            user_working_dir
        )
        if thumb_image is not None:
            await message.reply_photo(
                photo=thumb_image,
                quote=True,
                caption=text_message,
                reply_markup=reply_markup
            )
            await i_m_sefg.delete()
        else:
            await i_m_sefg.edit_text(
                text=text_message,
                reply_markup=reply_markup
            )
    else:
        await i_m_sefg.edit_text(
            "You Entered Wrong Way\n Use Following Command To Download or Upload Video From Streaming Site.\n**But Command Should Be as Reply To Video Link.** Playlists Link Not Supported.\n\n● For Download On Telegram Use/stream\n● For Uploading On G-Drive Use <code>/stream gdrive<code/>\n\nYouTube And Hotstar Link Works Fabulously. \n"
            f"<b>API Error</b>: {cf_name}"
        )
